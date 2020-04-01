from peto.domainmodel.base import PetoAggregateRoot


class Household(PetoAggregateRoot):
    def __init__(self, *, postcode, house_num, **kwargs):
        super(Household, self).__init__(**kwargs)
        self.postcode = postcode
        self.house_num = house_num
        self.people = set()

    def add_person(self, nhs_num):
        self.__trigger_event__(self.PersonAdded, nhs_num=nhs_num)

    class PersonAdded(PetoAggregateRoot.Event):
        @property
        def nhs_num(self):
            return self.__dict__["nhs_num"]

        def mutate(self, obj: "Household"):
            obj.people.add(self.nhs_num)

    def remove_person(self, nhs_num):
        self.__trigger_event__(self.PersonRemoved, nhs_num=nhs_num)

    class PersonRemoved(PetoAggregateRoot.Event):
        @property
        def nhs_num(self):
            return self.__dict__["nhs_num"]

        def mutate(self, obj: "Household"):
            obj.people.remove(self.nhs_num)
