from uuid import uuid5, NAMESPACE_URL

from eventsourcing.application.decorators import applicationpolicy
from eventsourcing.application.process import ProcessApplication, WrappedRepository
from eventsourcing.domain.model.aggregate import TAggregate, TAggregateEvent
from eventsourcing.exceptions import RepositoryKeyError

from peto.domainmodel.exceptions import HouseholdNotFound
from peto.domainmodel.household import Household
from peto.domainmodel.person import Person


class HouseholdsApplication(ProcessApplication):
    persist_event_type = Household.Event

    def get_household_by_address(self, postcode, house_num) -> Household:
        return self._get_household_by_address(self.repository, postcode, house_num)

    def _get_household_by_address(self, repository, postcode, house_num) -> Household:
        household_id = create_household_id(postcode=postcode, house_num=house_num)
        return self._get_household_by_id(repository, household_id)

    def get_household_by_id(self, household_id) -> Household:
        return self._get_household_by_id(self.repository, household_id)

    def _get_household_by_id(self, repository, household_id):
        try:
            household = repository[household_id]
        except RepositoryKeyError:
            raise HouseholdNotFound
        else:
            assert isinstance(household, Household)
        return household

    @applicationpolicy
    def policy(self, repository, event):
        pass

    @policy.register(Person.Created)
    def _(self, repository, event):
        postcode = event.postcode
        house_num = event.house_num
        try:
            household = self._get_household_by_address(repository, postcode, house_num)
        except HouseholdNotFound:
            household = self.register_household(postcode=postcode, house_num=house_num)
        household.add_person(event.nhs_num)
        return household

    @policy.register(Person.AddressChanged)
    def _(self, repository, event):
        nhs_num = event.nhs_num
        old_postcode = event.old_postcode
        old_house_num = event.old_house_num
        new_postcode = event.new_postcode
        new_house_num = event.new_house_num
        old_household = self._get_household_by_address(
            repository, old_postcode, old_house_num
        )
        old_household.remove_person(nhs_num)

        try:
            household = self._get_household_by_address(
                repository, new_postcode, new_house_num
            )
        except HouseholdNotFound:
            household = self.register_household(
                postcode=new_postcode, house_num=new_house_num
            )

        household.add_person(event.nhs_num)
        return household

    def register_household(self, postcode, house_num):
        household = Household.__create__(
            originator_id=create_household_id(postcode, house_num),
            postcode=postcode,
            house_num=house_num,
        )
        return household

    def select_household_ids(self, slot, cycle):
        selection = []
        for (
            household_id
        ) in self.repository.event_store.record_manager.all_sequence_ids():
            if (household_id.int % cycle) == slot:
                selection.append(household_id)
        return selection


def create_household_id(postcode, house_num):
    return uuid5(NAMESPACE_URL, f"/household/{postcode}/{house_num}")
