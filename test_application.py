import datetime
from unittest import TestCase
from uuid import uuid4

from eventsourcing.application.sqlalchemy import SQLAlchemyApplication

from peto.application import PetoCore
from peto.domainmodel import Person, PersonNotFound


class TestApplication(TestCase):
    def test_application(self):
        # Construct application.
        with PetoCore.mixin(SQLAlchemyApplication)() as core:
            assert isinstance(core, PetoCore)

            # The national master file (separately for England, Wales, Scotland
            # and N Ireland) is everyone's name, date of birth, NHS no. and (if
            # recorded) tel and email for those registered at each household
            # address, based on current GP practice records.

            # Register person.
            with self.assertRaises(PersonNotFound):
                core.get_person_by_nhs_num('450 557 7104')

            core.register_person(
                name="Example Name Only",
                dob=datetime.date(year=2000, month=1, day=1),
                nhs_num='450 557 7104',  # Example number only.
                tel_num='01234567890',
                email='example@example.com',
                postcode='AA1 1AA',
                house_num='11a',
            )

            person = core.get_person_by_nhs_num('450 557 7104')
            self.assertIsInstance(person, Person)
            self.assertEqual(person.name, "Example Name Only")
            self.assertEqual(person.postcode, "AA1 1AA")
            self.assertEqual(person.house_num, "11a")

            # A direct access facility for authorised people to submit changes of address is needed.
            core.change_address(
                nhs_num='450 557 7104',
                new_postcode='BB2 2BB',
                new_house_num='22b'
            )

            person = core.get_person_by_nhs_num('450 557 7104')
            self.assertIsInstance(person, Person)
            self.assertEqual(person.name, "Example Name Only")
            self.assertEqual(person.postcode, "BB2 2BB")
            self.assertEqual(person.house_num, "22b")

            # Barcoded sample tubes with preprinted name and date of birth are
            # delivered and collected weekly from each household and distributed
            # to labs for testing.
            # Todo: Projection into households view.
            # Todo: For each household,



            # Each testing lab creates a new Excel file of samples received and test results for each run of 96 or
            # 48 samples (depending on PCR machine capacity) and uploads it after each run.

            lab1_id = uuid4()
            core.register_batch_of_results(
                lab_id=lab1_id,
                results=[
                    ('barcode0', 0),
                    ('barcode1', 0),
                    ('barcode2', 1),
                    ('barcode3', 0),
                ]
            )

