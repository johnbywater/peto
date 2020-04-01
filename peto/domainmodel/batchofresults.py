from peto.domainmodel.base import PetoAggregateRoot


class BatchOfResults(PetoAggregateRoot):
    def __init__(self, lab_id, results, **kwargs):
        super(BatchOfResults, self).__init__(**kwargs)
        self.lab_id = lab_id
        self.results = results
