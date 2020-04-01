from eventsourcing.application.simple import SimpleApplication
from eventsourcing.exceptions import RepositoryKeyError

from peto.domainmodel import PetoAggregateRoot, Person, create_person_id, PersonNotFound, ResultsBatch


class PetoCore(SimpleApplication):
    persist_event_type = PetoAggregateRoot.Event

    def register_person(self, name, dob, nhs_num, tel_num, email, postcode, house_num):
        person = Person.__create__(
            originator_id=create_person_id(nhs_num),
            name=name,
            dob=dob,
            nhs_num=nhs_num,
            tel_num=tel_num,
            email=email,
            postcode=postcode,
            house_num=house_num
        )
        person.__save__()

    def change_address(self, nhs_num, new_postcode, new_house_num):
        person = self.get_person_by_nhs_num(nhs_num)
        person.change_address(new_postcode, new_house_num)
        person.__save__()

    def get_person_by_nhs_num(self, nhs_num) -> Person:
        person_id = create_person_id(nhs_num)
        try:
            person = self.repository[person_id]
        except RepositoryKeyError:
            raise PersonNotFound
        else:
            assert isinstance(person, Person)
            return person

    def register_batch_of_results(self, lab_id, results):
        ResultsBatch.__create__(
            lab_id=lab_id,
            results=results,
        )
