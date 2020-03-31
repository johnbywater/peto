from unittest import TestCase

from eventsourcing.application.sqlalchemy import SQLAlchemyApplication

from peto.application import PetoApplication


class TestApplication(TestCase):
    def test_application(self):
        # Construct application.
        with PetoApplication.mixin(SQLAlchemyApplication)() as app:
            assert isinstance(app, PetoApplication)
