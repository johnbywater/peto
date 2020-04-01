from eventsourcing.domain.model.aggregate import BaseAggregateRoot


class PetoAggregateRoot(BaseAggregateRoot):
    __subclassevents__ = True