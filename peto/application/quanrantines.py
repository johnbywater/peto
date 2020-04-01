from eventsourcing.application.decorators import applicationpolicy
from eventsourcing.application.process import ProcessApplication
from eventsourcing.exceptions import RepositoryKeyError

from peto.domainmodel.exceptions import PersonalQuarantineStatusNotFound
from peto.domainmodel.person import create_person_id
from peto.domainmodel.quarantine import PersonalQuarantineStatus
from peto.domainmodel.sample import Sample


class QuarantinesApplication(ProcessApplication):
    persist_event_type = PersonalQuarantineStatus.Event

    def check_personal_status(self, nhs_num):
        quarantine_status_id = create_person_id(nhs_num)

        try:
            quarantine_status = self._get_quarantine_status(
                self.repository, quarantine_status_id
            )
        except PersonalQuarantineStatusNotFound:
            return False
        else:
            return quarantine_status.is_required

    def _get_quarantine_status(
        self, repository, quarantine_status_id
    ) -> PersonalQuarantineStatus:
        try:
            return repository[quarantine_status_id]
        except RepositoryKeyError:
            raise PersonalQuarantineStatusNotFound

    @applicationpolicy
    def policy(self, repository, event):
        pass

    @policy.register(Sample.ResultRecorded)
    def _(self, repository, event: Sample.ResultRecorded):
        nhs_num = event.nhs_num
        status = bool(event.result)
        quarantine_status_id = create_person_id(nhs_num)
        try:
            quarantine_status = self._get_quarantine_status(
                repository, quarantine_status_id
            )
        except PersonalQuarantineStatusNotFound:
            if status is True:
                quarantine_status = PersonalQuarantineStatus.__create__(
                    originator_id=quarantine_status_id
                )
                quarantine_status.set_is_required()
                return quarantine_status
        else:
            if status is False and quarantine_status.is_required:
                quarantine_status.set_not_required()
