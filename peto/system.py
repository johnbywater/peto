from eventsourcing.system.definition import System

from peto.application.households import HouseholdsApplication
from peto.application.people import PeopleApplication
from peto.application.quanrantines import QuarantinesApplication
from peto.application.samples import BatchesApplication, SamplesApplication

system = System(
    PeopleApplication | HouseholdsApplication,
    BatchesApplication | SamplesApplication | QuarantinesApplication,
)
