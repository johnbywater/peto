from eventsourcing.system.definition import System

from peto.application.people import PeopleApplication
from peto.application.households import HouseholdsApplication
from peto.application.quanrantines import QuarantinesApplication
from peto.application.samples import SamplesApplication, BatchesApplication

system = System(
    PeopleApplication | HouseholdsApplication,
    BatchesApplication | SamplesApplication | QuarantinesApplication
)
