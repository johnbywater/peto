from peto.domainmodel.base import PetoAggregateRoot


class Sample(PetoAggregateRoot):
    def __init__(self, *, name, dob, nhs_num, **kwargs):
        super(Sample, self).__init__(**kwargs)
        self.name = name
        self.dob = dob
        self.nhs_num = nhs_num
        self.result = None

    def record_result(self, result):
        self.__trigger_event__(self.ResultRecorded, result=result)

    class ResultRecorded(PetoAggregateRoot.Event):
        @property
        def result(self):
            return self.__dict__['result']

        def mutate(self, obj):
            obj.result = self.result
