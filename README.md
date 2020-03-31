# Peto

System to record mass periodic swab tests results using eventsourcing library

## Motivation

Coronavirus (COVID-19) is a novel human respiratory virus.
The respiratory aspect means the virus is transmitted during
the course of physical social interaction, which is unavoidable
for many human activities on which society depends. Its novelty
means there is no vaccine (and none expected for at least one year,
perhaps two).

The virus causes no symptoms in some people. But of those people who
do develop symptoms, some people will recover and some people will die.
The dispositions to different outcomes are not very well understood, but
age seems to be a strong factor, with older individuals being more at risk
than younger ones. The outcome depends upon individual biological reaction
to being infected, partly their immune system response but also other
factors that are not fully understood. If the number of infected people
reaches the point where more people develop severe symptoms than a health
service has capacity to care for, the proportion of infected people who die
(the case fatality rate) may increase.

Respiratory viruses are relatively easily transmitted from person to person,
through exhalation of droplets containing the virus into air that is subsequently
breathed in by another person, and through contact with contaminated surfaces
and areas of the face such as eyes, mouth, and nose.

The average number of people that become infected by an infected person can vary.
If the number of people who are infected by an infected person is greater than one,
then over time the number of cases of tends to increase exponentially. However, if
the number of people who are infected by an infected person is less than one, then
over time the number of cases tends to decrease exponentially. This number is sometimes
referred to as the "reproduction number" and varies according to the period of
infectiousness, the degree of physical interaction, and the modes of transmission.
Since the period of infectiousness is more or less a property of the the virus itself,
attempts to reduce the reproduction number consider changing the degree of physical
interaction ("stay at home") and the modes of transmission ("catch it, kill it, bin it",
"wash your hands"). 

Because there is no vaccine, if personal hygiene measures (e.g. "wash your hands", or
everybody wearing a mask) are insufficient to reduce the reproduction number below the
critical level of one, the response to the existence of a novel respiratory virus becomes
a choice regarding whether or not to implement quarantining of infected individuals.
Quarantines prevent infected people from infecting other people by physical isolation
for the period in which they are infectious ("stay at home").

Without implementing quarantine, most people will eventually become infected. This
option may lead to "herd immunity" if the individuals that recover sustain resistance
to reinfection. However this approach will lead to a large number deaths, and may take
some time for all the individuals susceptible to developing severe symptoms to die. And
any herd immunity may fade away, or be deprecated by mutation of the virus. This is the
"let rip" or "mass deaths" strategy.

The alternatives to the "mass deaths" strategy are the various quarantine strategies.
Infected individuals can be quarantined either by mass quarantine ("lockdown") or by
selective quarantine. Selective quarantine can be implemented: either with "periodic
mass testing" to detect infected individuals whether they have developed
symptoms or not; or with "mass tracking" so that when a person develops symptoms
and feels unwell they can be tested and their contacts can be traced and tested.

The "mass deaths" strategy causes severe detriment to well-being, through direct
loss of life ("mass deaths", impacting on mental health through bereavement,
whilst also impacting on economic activity through trauma and organisational disruption.

The "lockdown" strategy causes severe detriment to well-being, through direct
damage to livelihoods and education, whilst also impacting on mental
health through isolation ("quarantine for all").

The "mass tracking" strategy avoids mass deaths and severe damage to the
economy, but involves enforced mass tracking of all individuals so that those
who crossed the path of the infected individual can be identified, traced,
and tested. By waiting until an infected individual develops symptoms, infected
individuals have a greater duration of being infectious.

The "periodic testing" strategy also avoids mass deaths and severe damage to the
economy, and it also avoids mass tracking. It involves repeat mass testing of a
high proportion of individuals, so that infected individuals are detected regardless
of whether or not they develop symptoms later. The period can be adjusted according
to prevalence of infection, and would be expected to decline exponentially as the
incidence of infection falls away.

This software is designed to support periodic mass testing, by recording testing
results and establishing the test status of individuals. 

The approach was conceived by Julian Peto FRS.


