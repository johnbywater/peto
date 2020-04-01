from eventsourcing.application.decorators import applicationpolicy
from eventsourcing.application.process import ProcessApplication

from peto.domainmodel.batchofresults import BatchOfResults
from peto.domainmodel.sample import Sample


class BatchesApplication(ProcessApplication):
    persist_event_type = BatchOfResults.Event

    def register_batch_of_results(self, lab_id, results):
        batch = BatchOfResults.__create__(lab_id=lab_id, results=results,)
        batch.__save__()


class SamplesApplication(ProcessApplication):
    persist_event_type = Sample.Event

    def register_sample(self, sample_id, name, dob, nhs_num):
        sample = Sample.__create__(
            originator_id=sample_id, name=name, dob=dob, nhs_num=nhs_num,
        )
        sample.__save__()

    @applicationpolicy
    def policy(self, repository, event):
        pass

    @policy.register(BatchOfResults.Created)
    def _(self, repository, event):
        for result in event.results:
            sample: Sample = self._get_sample(repository, result[0])
            sample.record_result(result[1])

    def get_sample(self, sample_id):
        return self._get_sample(self.repository, sample_id)

    def _get_sample(self, repository, sample_id):
        return repository[sample_id]
