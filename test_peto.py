import datetime
from unittest import TestCase
from uuid import uuid4, UUID

from eventsourcing.system.definition import AbstractSystemRunner

from peto.application.people import PeopleApplication
from peto.application.households import HouseholdsApplication
from peto.application.quanrantines import QuarantinesApplication
from peto.application.samples import SamplesApplication, BatchesApplication
from peto.system import system
from peto.domainmodel.person import Person
from peto.domainmodel.exceptions import PersonNotFound


def generate_household_sample_specs(slot, cycle, people: PeopleApplication, households: HouseholdsApplication):
    all_samples_spec = []
    for household_id in households.select_household_ids(slot=slot, cycle=cycle):
        household = households.get_household_by_id(household_id)
        samples_spec = []
        household_sample_spec = {
            'postcode': household.postcode,
            'house_num': household.house_num,
            'samples_spec': samples_spec
        }
        all_samples_spec.append(household_sample_spec)
        for nhs_num in household.people:
            person = people.get_person_by_nhs_num(nhs_num)
            sample_id = uuid4()
            samples_spec.append(
                {
                    'name': person.name,
                    'dob': person.dob,
                    'nhs_num': person.nhs_num,
                    'sample_id': sample_id
                }
            )
    return all_samples_spec


class TestPeto(TestCase):
    def test_peto(self):
        # Construct application.
        with system as runner:
            assert isinstance(runner, AbstractSystemRunner)

            people = runner.get(PeopleApplication)
            assert isinstance(people, PeopleApplication)

            households = runner.get(HouseholdsApplication)
            assert isinstance(households, HouseholdsApplication)

            batches = runner.get(BatchesApplication)
            assert isinstance(batches, BatchesApplication)

            samples = runner.get(SamplesApplication)
            assert isinstance(samples, SamplesApplication)

            quarantines = runner.get(QuarantinesApplication)
            assert isinstance(quarantines, QuarantinesApplication)

            # The national master file (separately for England, Wales, Scotland
            # and N Ireland) is everyone's name, date of birth, NHS no. and (if
            # recorded) tel and email for those registered at each household
            # address, based on current GP practice records.

            # That is created by downloading centrally from the servers of the
            # companies (EMIS and TPP) who provide almost all GP databases.
            # Todo: Pull data from GP databases.

            # Register person.
            with self.assertRaises(PersonNotFound):
                people.get_person_by_nhs_num("450 557 7104")

            people.register_person(
                name="Example Name Only",
                dob=datetime.date(year=2000, month=1, day=1),
                nhs_num="450 557 7104",  # Example number only.
                tel_num="01234567890",
                email="example@example.com",
                postcode="AA1 1AA",
                house_num="11a",
            )

            person = people.get_person_by_nhs_num("450 557 7104")
            self.assertIsInstance(person, Person)
            self.assertEqual(person.name, "Example Name Only")
            self.assertEqual(person.postcode, "AA1 1AA")
            self.assertEqual(person.house_num, "11a")

            household1 = households.get_household_by_address(postcode="AA1 1AA", house_num="11a")
            self.assertEqual(household1.people, {"450 557 7104"})

            # Check quarantine status for person.
            status = quarantines.check_personal_status(nhs_num="450 557 7104")
            self.assertEqual(status, False)


            # A direct access facility for authorised people to submit changes of address is needed.
            people.change_address(
                nhs_num="450 557 7104", new_postcode="BB2 2BB", new_house_num="22b"
            )

            person = people.get_person_by_nhs_num("450 557 7104")
            self.assertIsInstance(person, Person)
            self.assertEqual(person.name, "Example Name Only")
            self.assertEqual(person.postcode, "BB2 2BB")
            self.assertEqual(person.house_num, "22b")

            household1 = households.get_household_by_address(postcode="AA1 1AA", house_num="11a")
            self.assertEqual(household1.people, set())

            household2 = households.get_household_by_address(postcode="BB2 2BB", house_num="22b")
            self.assertEqual(household2.people, {"450 557 7104"})

            # Barcoded sample tubes with preprinted name and date of birth are
            # delivered and collected weekly from each household and distributed
            # to labs for testing.

            households_day1 = households.select_household_ids(slot=1, cycle=6)
            households_day2 = households.select_household_ids(slot=2, cycle=6)
            households_day3 = households.select_household_ids(slot=3, cycle=6)
            households_day4 = households.select_household_ids(slot=4, cycle=6)
            households_day5 = households.select_household_ids(slot=5, cycle=6)
            households_day6 = households.select_household_ids(slot=6, cycle=6)

            self.assertEqual(households_day1, [household2.id])
            self.assertEqual(households_day2, [household1.id])
            self.assertEqual(households_day3, [])
            self.assertEqual(households_day4, [])
            self.assertEqual(households_day5, [])
            self.assertEqual(households_day6, [])

            # Todo: Improve the reliability of generating the samples (in case of interruption).
            #  - save the all_sample_specs in a file, and then progress through it
            all_samples_spec = generate_household_sample_specs(
                slot=1, cycle=6, people=people, households=households
            )
            for household_samples in all_samples_spec:
                for sample_spec in household_samples['samples_spec']:
                    samples.register_sample(**sample_spec)

            self.assertEqual(len(all_samples_spec), 1)
            self.assertEqual(all_samples_spec[0]['postcode'], 'BB2 2BB')
            self.assertEqual(all_samples_spec[0]['house_num'], '22b')
            self.assertEqual(len(all_samples_spec[0]['samples_spec']), 1)
            self.assertEqual(all_samples_spec[0]['samples_spec'][0]['name'], 'Example Name Only')
            self.assertEqual(all_samples_spec[0]['samples_spec'][0]['dob'], datetime.date(2000, 1, 1))
            self.assertIsInstance(all_samples_spec[0]['samples_spec'][0]['sample_id'], UUID)


            # [Lab registration.]
            lab1_id = uuid4()

            # [Samples distributed, collected, taken to labs.]

            # Each testing lab creates a new Excel file of samples received and test
            # results for each run of 96 or 48 samples (depending on PCR machine
            # capacity) and uploads it after each run.
            lab_results_csv = [
                (all_samples_spec[0]['samples_spec'][0]['sample_id'], 1),  # Test positive.
            ]
            batches.register_batch_of_results(
                lab_id=lab1_id,
                results=lab_results_csv,
            )

            sample_id = all_samples_spec[0]['samples_spec'][0]['sample_id']
            self.assertEqual(samples.get_sample(sample_id).result, True)

            # All scheduling of sample deliveries and collections, together with
            # household status on all residents (all negative, all negative or
            # untested, any positive) and hence quarantine status is also on the
            # file, together with free fields for other info.

            # Check quarantine status for person.
            status = quarantines.check_personal_status(nhs_num="450 557 7104")
            self.assertEqual(status, True)

            lab_results_csv = [
                (all_samples_spec[0]['samples_spec'][0]['sample_id'], 0),  # Test negative.
            ]
            batches.register_batch_of_results(
                lab_id=lab1_id,
                results=lab_results_csv,
            )

            # Check quarantine status for person.
            status = quarantines.check_personal_status(nhs_num="450 557 7104")
            self.assertEqual(status, False)

            # Check quarantine status for household.
            # Question: Is is better to cohort those tested positive
            # rather than quarantining infected individuals in household?

            # A facility for adding people with no NHS number or address for
            # samples distributed by outreach workers is also needed, plus a
            # mobile app for them to enter the tube ID no. and add name, DoB
            # and any further info on such samples. Results would go back to
            # the outreach worker if no address is recorded.
            # Todo: Support for testing people with no NHS number or address.
            # Question: Where are swabs made? Where are the sample tubes
            # assembled and dispatched to households? Perhaps this could be
            # done in different places too, with different locations getting
            # access to subsets of the dispatching (sample) specifications.
            # Todo: Sample specifications need information about where they
            # will be sent so that they are received by the labs.

            # Who delivers the sample to the households? Postal delivery
            # system? Community based delivery?

            # Who collects the samples and sends them to the labs? Do people
            # do this themselves, or is this community based collection?

            # Who monitors quarantining? Is this voluntary? Are people provided
            # with what they need? Are people disallowed from transport etc.?
            # How would people be identified if they were unable to travel? Spot
            # checks with heavy penalties?

            # Question: Distribution of testing, so that all areas are covered
            # adequately. Labs are unevenly distributed, and their providing
            # tests to only local area means other areas will not be covered.
            # Sample tubes sent to households need to be collected and taken
            # to a nearby lab, in a way that minimises overall "tube miles".
            #
            # https://www.theguardian.com/world/2020/apr/02/small-laboratories-coronavirus-testing-time-wasted-dunkirk
            # 'Some experts expressed concerns that not all cities or regions had large universities or research
            # facilities that could contribute to local testing capacity, meaning regional disparities could emerge,
            # particularly in tests on healthcare workers.
            #
            # '“There is definitely a potential for inequality,” said Prof Ravi Gupta, who is leading the assessment
            # of the Samba testing at Cambridge. “That’s where government testing should be directed – that needs to
            # be factored in.”'
