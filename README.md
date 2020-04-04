# Peto

[![Build Status](https://travis-ci.org/johnbywater/peto.svg?branch=master)](https://travis-ci.org/johnbywater/peto)
[![Coverage Status](https://coveralls.io/repos/github/johnbywater/peto/badge.svg?branch=master#)](https://coveralls.io/github/johnbywater/peto)

System to support mass periodic testing for infectious disease.

This system is motivated by the occurrence of the Cononavirus (COVID-19) pandemic.


## Abstract

Peto is a reliable, scalable, event-sourced, open source software system designed to support
periodic mass testing for novel infectious diseases such as Coronavirus. It has been written
to support an expression of requirements from Julian Peto FRS, who proposed the periodic mass
testing strategy in the British Medical Journal [BMJ 2020;368:m1163] as an effective way to
avoid both the mass quarantine ("lockdown") strategy and the mass deaths ("herd immunity") strategy.
Periodic mass testing supports a selective quarantine strategy that detects infected
individuals regardless of whether or not they have or will develop symptoms. Periodic mass
testing is an alternative to enforced mass tracking with self reporting by those who
have developed symptoms. This is an important difference in the case of Coronavirus because
individuals with Coronavirus are known to become infectious before they develop symptoms, with
some infectious individuals remaining asymptomatic. Whilst mass tracking has worked for example
in China to support contact tracing,  mass tracking may be a poor cultural fit in open democratic
societies, and low adoption or avoidance of location tracking apps may impact on effectiveness.
This software is designed to be integrated with existing patient record systems, dispatching
of sample tubes from test kit distributors to households, submission of results from sample testing
labs, and checking of quarantine status by national health service, police and public health authorities.


## Motivation

Coronavirus (COVID-19) is a novel human respiratory virus.
The respiratory aspect means the virus is transmitted during
the course of physical social interaction, which is unavoidable
for many human activities on which society depends. Its novelty
means there is no vaccine (and the responsible view seems to be
the none is expected for at least one year, perhaps two).

The virus causes no symptoms in some people. But of those people who
do develop symptoms, some will recover and some will die. The dispositions
to different outcomes are not very well understood, but age seems to be a
strong factor, with older individuals being more at risk than younger ones.
If the number of infected people reaches the point where more people
develop severe symptoms than a health service has capacity to care for, the
proportion of infected people who die (the case fatality rate) may increase.

Respiratory viruses are relatively easily transmitted from person to person
through exhalation of droplets (including aerosol) that are subsequently
inhaled by another person. This can happen by coughing and sneezing but heavy
breathing and during conversations. Virus can also be transmitted indirectly
by touching contaminated surfaces and then touching parts of the face such as
eyes, mouth, and nose. Surface contamination may result from exhaled droplets
landing, from fecal smears, and from contact with other contaminated surfaces.

The average number of people that become infected by an infected person can vary.
If the number of people who are infected by an infectious person is greater than one,
then over time the number of cases tends to increase exponentially. However, if
the number of people who are infected by an infectious person is less than one, then
over time the number of cases tends to decrease exponentially. This number is sometimes
referred to as the "reproduction number" and varies according to the period of
infectiousness, the degree of physical interaction, the modes of transmission,
and the proportion of susceptible individuals in the population. The number of
susceptible individuals can vary as infected people recover, and also through mass
vaccination, if a vaccine is available.

Since the period of infectiousness is perhaps a function of the virus itself,
attempts may be made to reduce the reproduction number. It is possible to try
inhibiting modes of transmission through public health campaigns ("catch it,
kill it, bin it", "wash your hands") and use of personal protective equipment
(masks, respirators, eye shields, etc), to attempt a reduction in the degree
of physical interaction ("stay at home", physical distancing). Quarantines
prevent infected people from infecting other people by physical isolation
for the period during which they are thought to be infectious ("stay at home").
Quarantines may be universal if infectious individuals cannot be distinguished
from non-infectious individuals, or selective if infectious individuals can be
distinguished from non-infectious individuals. Quarantines can be voluntary
(self-isolation at home) or enforced (house arrest, incarceration). Quarantines
may be organised in cohorts to avoid infecting other members of a household,
prison, or hospital.

There are therefore policy choices to be made. When the reproduction number is
great enough to cause a mass epidemic, without implementing a quarantine strategy,
most people will eventually become infected. This option may over time lead to "herd
immunity" if the individuals that recover sustain resistance to reinfection. However
this "do nothing" approach may lead to mass deaths, and it may take some time for all the
individuals susceptible to developing severe symptoms to die. And any herd immunity
may fade away, or be deprecated by mutation of the virus. A public reaction may
follow from these consequences, unless this strategy is disguised, by for example
pretending or promising to adopt a different strategy without actually doing so.

The alternatives to the "mass deaths" strategy are the various quarantine strategies.
Infected individuals can be quarantined either by mass quarantine ("lockdown") or by
selective quarantine. Selective quarantine can be implemented either with "periodic
mass testing" to detect infected individuals whether they have developed
symptoms or not, or with "mass tracking" so that when a person develops symptoms
and feels unwell they can be tested and their contacts can be traced and tested.

The "mass deaths" strategy may cause severe detriment to well-being, through direct
loss of life ("mass deaths") impacting on mental health through bereavement,
whilst also impacting on economic activity through trauma, organisational disruption,
and damage to the health of those who recover, and the health of those who are not
infected but unable able to access the medical they need and would otherwise recieve.

The "lockdown" strategy may cause severe detriment to well-being, through direct
damage to livelihoods and education, whilst also impacting on mental
health through isolation ("quarantine for all") causing long term damage or
even death in some individuals.

The "mass tracking" strategy avoids mass deaths and severe damage to the
economy and the health of those who recover, but involves enforced mass tracking
of all individuals so that those who crossed the path of the infected individual
can be identified, traced, and tested. By waiting until an infected individual
develops symptoms, infected individuals have a greater duration of being infectious.
In countries where this is not a good cultural fit, the effectiveness of mass
tracking may be compromised.

The "periodic testing" strategy also avoids mass deaths and severe damage to the
economy, and it also avoids mass tracking. It involves repeat mass testing of a
high proportion of individuals, so that infected individuals are detected regardless
of whether or not they develop symptoms later. The period can be adjusted according
to prevalence of infection, and would be expected to decline exponentially as the
incidence of infection falls away. This strategy has precedents, for example testing
for TB in children in the 1950s.

This software is designed to support selective quarantining with regular testing-for-all,
by recording testing results and establishing the test status of individuals. The period
can increase as the level of infection in the population decreases. This approach to
responding to Coronavirus was proposed by Julian Peto FRS, and has been promoted by
Jeremy Hunt MP, by Tony Blair, and by others such as Bill Gates.


## Proposal

From https://www.bmj.com/content/368/bmj.m1163

In Editor’s Choice of 19 March Godlee mentions the urgent need for increased capacity to test frontline healthcare workers serologically to verify their immunity to the covid-19 virus.[1] Even more urgent is capacity for weekly viral detection in the whole UK population. This, together with intensive contact tracing, could enable the country to resume normal life immediately. The virus could only survive in those who are untested, and contact tracing would often lead to them. Within the tested population anyone infected would be detected within about a week (0 to 7 days plus sample transport and testing) of becoming infectious.

Centrally organised facilities with the capacity to test the entire UK population weekly (in 6 days at 10 million tests per day) can be made available much more quickly and cheaply than a vaccine, probably within weeks. This heroic but straightforward national effort would involve a crash programme to enlist all existing PCR (polymerase chain reaction) facilities, acquire or manufacture the PCR reagents, and agree protocols including a laptop program for barcode reading in smaller laboratories. The US Food and Drug Administration (FDA) has just authorised a test kit for detecting the covid-19 virus that can be run on machines used in the NHS for HPV screening. Only laboratories that do PCR routinely would participate, subject to central quality control and at cost price. The Wellcome Sanger Institute, UK Biocentre, and smaller academic laboratories, together with all commercial facilities, should have enough machines or can get more immediately from the manufacturers. The 24-hour extra staffing to run their machines continuously would be bioscience students, graduates, and postgraduates familiar with PCR who already work in or near the laboratory. Processing capacity equivalent to 4000 Roche COBAS 8800 systems is needed, and the UK may already have both the machines and the trained staff in post or immediately available.

All patients registered with a GP would be sent a test kit (a swab for throat and nasal self-sample, and a transport tube labelled with their name, NHS number, and a barcode). Homeless people and other disadvantaged groups would be served by charities already in contact with them. The Post Office, Amazon, and other companies already have the capacity to collect swabs from everyone with an address. Swabs might go to central facilities for preparation and arraying before dispatch to local laboratories for PCR.

Everyone should be tested weekly. All households and care homes would return self-taken swabs from all residents together. In most homes all residents would test negative and they could resume normal life immediately. An identification card certifying date and result of latest test (positive, negative, negative contact of a positive case) might be useful for policing arrangements. By the time the first test is done there may be more than a million infected people who must be treated or remain quarantined at home or in care until all residents at the address test negative. That unavoidable crisis for the NHS would be ameliorated by earlier diagnosis and treatment, and hence reduced pressure on intensive care, and by having all staff as well as patients tested regularly. Contacts of positive people who test negative could choose continued home quarantine or, at little extra risk, choose to join a group of up to 10 test-negative contacts (usually with other family members). Subsequent weekly national testing, together with behavioural changes and efficient contact tracing, would find progressively fewer infections and might soon be extended to a month. This emergency system would only be needed for about 2 months but could be rapidly reintroduced to control any future epidemic caused by a new virus.

## Requirements overview

The national master file (separately for England, Wales, Scotland and N Ireland) is everyone's name, date of birth, NHS no. and (if recorded) tel and email for those registered at each household address, based on current GP practice records. That is created by downloading centrally from the servers of the companies (EMIS and TPP) who provide almost all GP databases. Barcoded sample tubes with preprinted name and date of birth are delivered and collected weekly from each household and distributed to labs for testing. A direct access facility for authorised people to submit changes of address is needed. Each testing lab creates a new Excel file of samples received and test results for each run of 96 or 48 samples (depending on PCR machine capacity) and uploads it after each run. The national master file is thus always up to date and labs retain complete records of their work. All scheduling of sample deliveries and collections, together with household status on all residents (all negative, all negative or untested, any positive) and hence quarantine status is also on the file, together with free fields for other info. A facility for adding people with no NHS number or address for samples distributed by outreach workers is also needed, plus a mobile app for them to enter the tube ID no. and add name, DoB and any further info on such samples. Results would go back to the outreach worker if no address is recorded.

It would be a mistake to have more complex IT. It can all be managed through one simple master file by giving NHS, police and public health full access to the master database and limited access for other users.