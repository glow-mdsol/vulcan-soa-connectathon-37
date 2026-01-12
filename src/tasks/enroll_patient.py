import random

from config import Config
import datetime
from typing import Optional
import fhirsdk
from fhirsdk.client import Client, Auth, AuthCredentials
from fhirsdk import (
    Patient,
    ResearchStudy,
    Reference,
    ResearchSubject,
    ResearchSubjectSubjectMilestone,
    ResearchSubjectSubjectState,
    CodeableConcept,
    Identifier,
    Coding,
)

STATUSES = [
    "candidate",
    "in-prescreening",
    "in-screening",
    "eligible",
    "ineligible",
    "on-study",
    "on-study-intervention",
    "in-follow-up",
    "off-study",
]


def enrol_patient(
    subject_id: str,
    patient_id: str,
    research_study_id: str,
    config: Config,
    enrolment_date: Optional[str] = None,
):
    """
    Enroll a patient into a research study.

    Args:
        patient_id (str): The ID of the patient to enroll.
        subject_id (str): The assigned subject ID .
        research_study_id (str): The ID of the research study to enroll the patient in.
    """
    # get the the patient
    client = Client(
        config.endpoint_url,
        auth=Auth(
            method="basic",
            credentials=AuthCredentials(
                username=config.fhir_username, password=config.fhir_password
            ),
        ),
    )
    patient = client.read(Patient, patient_id)
    if not patient:
        raise ValueError(f"Patient with ID {patient_id} not found.")
    # get the research study
    research_study = client.read(ResearchStudy, research_study_id)
    if not research_study:
        raise ValueError(f"ResearchStudy with ID {research_study_id} not found.")
    if enrolment_date:
        _enrolment_date = datetime.datetime.strptime(enrolment_date, "%Y-%m-%d").date()
    else:
        _enrolment_date = (
            datetime.datetime.now() - datetime.timedelta(days=random.randint(30, 180))
        ).date()
    # Use the documentation: https://build.fhir.org/researchsubject.html
    # create the enrollment
    subject = ResearchSubject(
        identifier=[
            Identifier(
                system="https://example.com/patient-identifier", value=subject_id
            )
        ],
        study=Reference(reference=f"ResearchStudy/{research_study_id}"),
        subject=Reference(reference=f"Patient/{patient_id}"),
        status="active",
        subject_milestone=[
            ResearchSubjectSubjectMilestone(
                date=_enrolment_date.isoformat(),
                milestone=[
                    CodeableConcept(
                        text="Informed Consent",
                        coding=[
                            Coding(
                                system="http://terminology.hl7.org/ValueSet/research-subject-milestones",
                                code="C16735",
                            )
                        ],
                    ),
                    CodeableConcept(
                        text="Subject Entered Into Trial",
                        coding=[
                            Coding(
                                system="http://terminology.hl7.org/ValueSet/research-subject-milestones",
                                code="C161417",
                            )
                        ],
                    ),
                ],
            ),
        ],
        subject_state=[
            ResearchSubjectSubjectState(
                code=CodeableConcept(
                    text="Screening",
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/research-subject-state",
                            code="screening",
                        )
                    ],
                ),
                start_date=_enrolment_date.isoformat(),
                end_date=_enrolment_date.isoformat(),
            ),
            ResearchSubjectSubjectState(
                code=CodeableConcept(
                    text="On-study",
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/research-subject-state",
                            code="on-study",
                        )
                    ],
                ),
                start_date=_enrolment_date.isoformat(),
            ),
        ],
    )
    # save the enrollment
    created_enrollment = client.create(subject)
    return created_enrollment


def update_subject_status(
    research_subject_id: str, status: str, event_date: datetime.date, config: Config
):
    assert status in STATUSES, f"Invalid status: {status}"
    client = Client(
        config.endpoint_url,
        auth=Auth(
            method="basic",
            credentials=AuthCredentials(
                username=config.fhir_username, password=config.fhir_password
            ),
        ),
    )
    # get the subject
    subject = client.read(ResearchSubject, research_subject_id)
    if not subject:
        raise ValueError(f"ResearchSubject with ID {research_subject_id} not found.")
    current_state = subject.subject_state[-1]
    # if the current state is the same as the new state, return
    if current_state.code.text == status:
        return
    # close the previous state
    subject.subject_state[-1].end_date = event_date.isoformat()
    subject.subject_state.append(
        ResearchSubjectSubjectState(
            code=CodeableConcept(
                text=status,
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/research-subject-state",
                        code=status,
                    )
                ],
            ),
            start_date=event_date.isoformat(),
        )
    )
    # update the subject
    subject.subject_state = [
        ResearchSubjectSubjectState(
            code=CodeableConcept(
                text=status,
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/research-subject-state",
                        code=status,
                    )
                ],
            ),
            start_date=event_date.isoformat(),
        )
    ]
    # save the subject
    client.update(subject)
    return subject
