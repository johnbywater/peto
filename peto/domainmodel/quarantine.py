from peto.domainmodel.base import PetoAggregateRoot


class PersonalQuarantineStatus(PetoAggregateRoot):
    def __init__(self, **kwargs):
        super(PersonalQuarantineStatus, self).__init__(**kwargs)
        self.is_required = False

    def set_is_required(self):
        self.__trigger_event__(self.QuarantineIsRequired)

    class QuarantineIsRequired(PetoAggregateRoot.Event):
        def mutate(self, obj: "PersonalQuarantineStatus"):
            obj.is_required = True

    def set_not_required(self):
        self.__trigger_event__(self.QuarantineNotRequired)

    class QuarantineNotRequired(PetoAggregateRoot.Event):
        def mutate(self, obj: "PersonalQuarantineStatus"):
            obj.is_required = False


