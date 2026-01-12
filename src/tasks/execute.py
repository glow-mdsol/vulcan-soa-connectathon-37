from typing import Optional, Union
from typing import List, Opt
import datetime
from config import Config
import logging

logger = logging.getLogger(__name__)
import fhirsdk
from fhirsdk.client import Client, Auth, AuthCredentials
from fhirsdk import PlanDefinitionAction, ResearchStudy, Patient, ResearchSubject, CarePlan, Task, Reference, BundleEntry, Bundle, ActivityDefinition, PlanDefinition, ServiceRequest, Encounter, Identifier, RequestOrchestration 

def create_task(
    action: PlanDefinitionAction,
    research_subject: ResearchSubject,
    care_plan: CarePlan,
    visit_date: datetime.date,
    client: Client,
) -> Task:
    """
    Create a task for a research subject.
    """
    task = Task(
        status="requested",
        intent="order",
        based_on=Reference(reference=care_plan.id),
        description=action.description,
        for_=Reference(reference=research_subject.subject.reference),
        authored_on=visit_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
    )
    if action.definition_canonical:
        concept_type, concept_id = action.definition_canonical.split("/")
        match concept_type:
            case "ActivityDefinition":
                _target = client.read(ActivityDefinition, action.definition_canonical)
                task.code = _target.code
            case "PlanDefinition":
                _target = client.read(PlanDefinition, action.definition_canonical)
            case _:
                logger.warning(f"Unknown concept type: {concept_type}")
    created_task = client.create(task)
    return created_task


def manifest_plan_definition(
    plan_definition_id: str,
    research_subject: Union[ResearchSubject, str],
    visit_date: datetime.date,
    client: Client,
    skipping: Optional[bool] = False,
):
    """
    Create a care plan for a research subject.
    """
    if isinstance(research_subject, str):
        _research_subject = client.read(ResearchSubject, research_subject)
        assert _research_subject is not None, (
            f"ResearchSubject with ID {research_subject} not found."
        )
    else:
        _research_subject = research_subject
    # get the patient
    patient = client.read(Patient, _research_subject.subject.reference.split("/")[-1])

    # get the plan definition
    plan_definition = client.read(PlanDefinition, plan_definition_id)
    assert plan_definition is not None, (
        f"PlanDefinition with ID {plan_definition_id} not found."
    )
    # use the OID
    visit_oid = plan_definition.title
    # get the Visit OID from the plandefinition
    for identifier in plan_definition.identifier if plan_definition.identifier else []:
        if identifier.type == "OID":
            visit_oid = identifier.value
            break
    # Need a request orchestration to handle dependencies, conditions, etc.
    ro = RequestOrchestration(
        status="active",
        intent="plan",
        subject=Reference(reference=patient.id, type="Patient"),
        authored_on=visit_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
        instantiates_canonical=Reference(reference=plan_definition_id, type="PlanDefinition"),
    )
    created_request_orchestration = client.create(ro)
    # execute the plan definition
    if skipping:
        care_plan = CarePlan(
            status="revoked",
            intent="plan",
            based_on=Reference(reference=created_request_orchestration.id, type="RequestOrchestration"),
            subject=Reference(reference=patient.id, type="Patient"),
        ) 
    else:
        care_plan = CarePlan(
            status="active",
            intent="plan",
            based_on=Reference(reference=created_request_orchestration.id, type="RequestOrchestration"),
            subject=Reference(reference=patient.id, type="Patient"),
        ) 
    # save the care plan
    created_care_plan = client.create(care_plan)
    # Create the ServiceRequest
    service_request = ServiceRequest(
        status="active",
        intent="order",
        based_on=Reference(reference=created_care_plan.id, type="CarePlan"  ),
        subject=Reference(reference=_research_subject.subject.id, type="Patient"),
    )
    # save the service request
    created_service_request = client.create(service_request)
    # create the Encounter
    encounter = Encounter(
        identifier=[
            Identifier(
                system="http://example.com/encounters", value=visit_oid, type="OID"
            )
        ],
        status="active",
        based_on=Reference(reference=created_service_request.id),
        subject=Reference(reference=_research_subject.subject.id),
    )
    # save the encounter
    created_encounter = client.create(encounter)
    # create the task
    tasks = []
    for action in plan_definition.action if plan_definition.action else []:
        # save the tasks
        task = create_task(
            action=action,
            research_subject=_research_subject,
            care_plan=created_care_plan,
            visit_date=visit_date,
            client=client,
        )
        tasks.append(task)
    # complete the tasks
    for task in tasks:
        task.status = "completed"
        client.update(task)
    # finish the encounter
    created_encounter.status = "completed"
    client.update(created_encounter)
    # close out the service request
    created_service_request.status = "completed"
    client.update(created_service_request)
    # close the CarePlan
    created_care_plan.status = "completed"
    client.update(created_care_plan)
    # close out the RequestOrchestration
    created_request_orchestration.status = "completed"
    client.update(created_request_orchestration)
    # return the care plan
    return created_care_plan


def complete_plan_definition(research_subject_id: str, plan_definition_id: str, config: Config):
    """
    Mark the CarePlan for the patient complete
    """
    client = Client(
        config.endpoint_url,
        auth=Auth(
            method="basic",
            credentials=AuthCredentials(
                username=config.fhir_username, password=config.fhir_password
            ),
        ),
    )
    # TODO: ensure plan definition is consistent with ResearchSubject
    research_subject = client.read(ResearchSubject, research_subject_id)
    assert research_subject is not None, f"ResearchSubject with ID {research_subject_id} not found."
    plan_definition = client.read(PlanDefinition, plan_definition_id)
    assert plan_definition is not None, f"PlanDefinition with ID {plan_definition_id} not found."
    found = None
    # search for careplan
    for care_plan in client.search(CarePlan, dict(subject=Reference(reference=research_subject.subject.reference))):
        if care_plan.based_on.reference != plan_definition.:
            continue
        if care_plan.status in ("active"):
            found = care_plan
            break
    if found is None:
        raise ValueError(f"No active CarePlan found for ResearchSubject {research_subject_id} and PlanDefinition {plan_definition_id}")
    found.status = "completed"
    client.update(found)
    
def execute(
    research_subject_id: str,
    plan_definition_ids: List[str],
    visit_date: datetime.date,
    config: Config,
):
    """
    Execute a plan definition for a research subject.
    """
    # get the research subject
    client = Client(
        config.endpoint_url,
        auth=Auth(
            method="basic",
            credentials=AuthCredentials(
                username=config.fhir_username, password=config.fhir_password
            ),
        ),
    )
    research_subject = client.read(ResearchSubject, research_subject_id)
    assert research_subject is not None, (
        f"ResearchSubject with ID {research_subject_id} not found."
    )
    bundles = []
    for plan_definition_id in plan_definition_ids:
        # TODO: timepoints, visit date should move up
        manifested = manifest_plan_definition(
            plan_definition_id=plan_definition_id,
            research_subject=research_subject,
            visit_date=visit_date,
            client=client,
        )
        assert manifested is not None, (
            f"PlanDefinition with ID {plan_definition_id} not manifested."
        )
        bundles.append(manifested)
    return bundles
