from typing import Optional, Union
from typing import List, Optional
import datetime
from config import Config
import fhirsdk
from fhirsdk.client import Client, Auth, AuthCredentials
from fhirsdk import (
    PlanDefinitionAction,
    ResearchStudy,
    Patient,
    ResearchSubject,
    CarePlan,
    Task,
    Reference,
    BundleEntry,
    Bundle,
    ActivityDefinition,
    PlanDefinition,
    ServiceRequest,
    Encounter,
    Identifier,
    RequestOrchestration,
    CodeableConcept,
    Coding,
)
import logging
import yaml

logger = logging.getLogger(__name__)


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
        based_on=[Reference(reference=f"CarePlan/{care_plan.id}", type="CarePlan")],
        description=action.description,
        for_=Reference(reference=f"Patient/{research_subject.subject.reference.split('/')[-1]}", type="Patient"),
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


def create_bundle_from_execution(
    request_orchestration: RequestOrchestration,
    care_plan: CarePlan,
    service_request: ServiceRequest,
    encounter: Encounter,
    tasks: List[Task],
) -> Bundle:
    """
    Create a FHIR Bundle containing all resources created during execution.
    
    Args:
        request_orchestration: RequestOrchestration resource
        care_plan: CarePlan resource
        service_request: ServiceRequest resource
        encounter: Encounter resource
        tasks: List of Task resources
    
    Returns:
        Bundle containing all resources
    """
    entries = []
    
    # Add RequestOrchestration
    entries.append(
        BundleEntry(
            fullUrl=f"RequestOrchestration/{request_orchestration.id}",
            resource=request_orchestration,
            request={"method": "PUT", "url": f"RequestOrchestration/{request_orchestration.id}"}
        )
    )
    
    # Add CarePlan
    entries.append(
        BundleEntry(
            fullUrl=f"CarePlan/{care_plan.id}",
            resource=care_plan,
            request={"method": "PUT", "url": f"CarePlan/{care_plan.id}"}
        )
    )
    
    # Add ServiceRequest
    entries.append(
        BundleEntry(
            fullUrl=f"ServiceRequest/{service_request.id}",
            resource=service_request,
            request={"method": "PUT", "url": f"ServiceRequest/{service_request.id}"}
        )
    )
    
    # Add Encounter
    entries.append(
        BundleEntry(
            fullUrl=f"Encounter/{encounter.id}",
            resource=encounter,
            request={"method": "PUT", "url": f"Encounter/{encounter.id}"}
        )
    )
    
    # Add all Tasks
    for task in tasks:
        entries.append(
            BundleEntry(
                fullUrl=f"Task/{task.id}",
                resource=task,
                request={"method": "PUT", "url": f"Task/{task.id}"}
            )
        )
    
    # Create Bundle
    bundle = Bundle(
        type="transaction",
        entry=entries
    )
    
    return bundle


def bundle_to_yaml(bundle: Bundle) -> str:
    """
    Convert a FHIR Bundle to YAML representation.
    
    Args:
        bundle: Bundle resource
    
    Returns:
        YAML string representation
    """
    # Convert to dict and exclude None values for cleaner YAML
    bundle_dict = bundle.model_dump(exclude_none=True, by_alias=True)
    
    # Convert to YAML
    yaml_str = yaml.dump(
        bundle_dict,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=120
    )
    
    return yaml_str


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
        assert (
            _research_subject is not None
        ), f"ResearchSubject with ID {research_subject} not found."
    else:
        _research_subject = research_subject
    # get the patient
    patient = client.read(Patient, _research_subject.subject.reference.split("/")[-1])

    # get the plan definition
    plan_definition = client.read(PlanDefinition, plan_definition_id)
    assert (
        plan_definition is not None
    ), f"PlanDefinition with ID {plan_definition_id} not found."
    # use the OID
    visit_oid = plan_definition.title
    # get the Visit OID from the plandefinition
    for identifier in plan_definition.identifier if plan_definition.identifier else []:
        if identifier.type == "OID":
            visit_oid = identifier.value
            break
    # check for existing request orchestration
    existing_ros = client.search(
        RequestOrchestration,
        {
            "subject": f"Patient/{patient.id}",
            "instantiates-canonical": f"PlanDefinition/{plan_definition_id}",
            "status": "active",
        },
    )
    if existing_ros.total and existing_ros.entry:
        logger.info(
            f"Existing active RequestOrchestration found for ResearchSubject {research_subject} and PlanDefinition {plan_definition_id}"
        )
        created_request_orchestration = existing_ros.entry[0].resource
    else:
        # Need a request orchestration to handle dependencies, conditions, etc.
        ro = RequestOrchestration(
            status="active",
            intent="plan",
            subject=Reference(reference=patient.id, type="Patient"),
            instantiates_canonical=[f"PlanDefinition/{plan_definition_id}"],
        )
        try:
            created_request_orchestration = client.create(ro)
        except Exception as exc:
            logger.error(f"Failed to create RequestOrchestration: {exc}")
            print(ro.model_dump_json(indent=2))
            raise
    # execute the plan definition
    # check for the careplan
    created_care_plan_q = client.search(
        CarePlan,
        {
            "subject": f"Patient/{patient.id}",
            "based-on": f"RequestOrchestration/{created_request_orchestration.id}"
        },
    )
    if created_care_plan_q.total and created_care_plan_q.entry:
        created_care_plan = created_care_plan_q.entry[0].resource
        logger.info(
            f"Existing active CarePlan found for ResearchSubject {research_subject} and "\
            f"PlanDefinition {plan_definition_id}: {created_care_plan.id}")
        if created_care_plan.status == "revoked":
            logger.info("CarePlan is revoked, no further action taken.")
            return
    else:
        if skipping:
            care_plan = CarePlan(
                status="revoked",
                intent="plan",
                based_on=[
                    Reference(
                        reference=f"RequestOrchestration/{created_request_orchestration.id}",
                        type="RequestOrchestration",
                    )
                ],
                subject=Reference(reference=f"Patient/{patient.id}", type="Patient"),
            )
            # save the care plan
            created_care_plan = client.create(care_plan)
            logger.info(f"CarePlan {created_care_plan.id} created with status 'revoked' due to skipping.")
            return
        else:
            care_plan = CarePlan(
                status="active",
                intent="plan",
                based_on=[
                    Reference(
                        reference=f"RequestOrchestration/{created_request_orchestration.id}",
                        type="RequestOrchestration",
                    )
                ],
                subject=Reference(reference=f"Patient/{patient.id}", type="Patient"),
            )
            created_care_plan = client.create(care_plan)
            logger.info(f"CarePlan {created_care_plan.id} created with status 'active'.")
    # search for existing service request
    existing_srs = client.search(
        ServiceRequest,
        {
            "subject": f"Patient/{patient.id}",
            "based-on": f"CarePlan/{created_care_plan.id}",
            "status": "active",
        },
    )
    if existing_srs.total and existing_srs.entry:
        logger.info(
            f"Existing active ServiceRequest found for ResearchSubject {research_subject} and CarePlan {created_care_plan.id}"
        )
        created_service_request = existing_srs.entry[0].resource
    else:
        # Create the ServiceRequest
        service_request = ServiceRequest(
            status="active",
            intent="order",
            based_on=[Reference(reference=f"CarePlan/{created_care_plan.id}", type="CarePlan")],
            subject=Reference(reference=f"Patient/{patient.id}", type="Patient"),
        )
        # save the service request
        try:
            created_service_request = client.create(service_request)
            logger.info(f"ServiceRequest {created_service_request.id} created with status 'active'.")
        except Exception as exc:
            logger.error(f"Failed to create ServiceRequest: {exc}")
            print(service_request.model_dump_json(indent=2))
            raise
    # search for existing encounter
    existing_encounters = client.search(
        Encounter,
        {
            "subject": f"Patient/{patient.id}",
            "based-on": f"ServiceRequest/{created_service_request.id}"
        },
    )
    if existing_encounters.total and existing_encounters.entry:
        logger.info(
            f"Existing Encounter found for ResearchSubject {research_subject} and ServiceRequest {created_service_request.id}"
        )
        created_encounter = existing_encounters.entry[0].resource
    else:       
        # create the Encounter
        encounter = Encounter(
            identifier=[
                Identifier(
                    system="http://example.com/encounters/oids", 
                    value=visit_oid,
                    use="secondary"
                )
            ],
            status="in-progress",
            based_on=[Reference(reference=f"ServiceRequest/{created_service_request.id}", type="ServiceRequest")],
            subject=Reference(reference=f"Patient/{patient.id}", type="Patient"),
        )
        # save the encounter
        try:
            created_encounter = client.create(encounter)
            logger.info(f"Encounter {created_encounter.id} created with status 'in-progress'.")
        except Exception as exc:
            logger.error(f"Failed to create Encounter: {exc}")
            print(encounter.model_dump_json(indent=2))
            raise
    # create the task (Revisit this later)
    tasks = []
    # for action in plan_definition.action if plan_definition.action else []:
    #     print(f"Creating task for action: {action.title}")
    #     # save the tasks
    #     task = create_task(
    #         action=action,
    #         research_subject=_research_subject,
    #         care_plan=created_care_plan,
    #         visit_date=visit_date,
    #         client=client,
    #     )
    #     tasks.append(task)
    # # COMPLETE
    # # complete the tasks
    # for task in tasks:
    #     task.status = "completed"
    #     client.update(task)
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
    
    # Create bundle with all created resources
    bundle = create_bundle_from_execution(
        request_orchestration=created_request_orchestration,
        care_plan=created_care_plan,
        service_request=created_service_request,
        encounter=created_encounter,
        tasks=tasks
    )
    
    # return the care plan and bundle
    return {
        "care_plan": created_care_plan,
        "bundle": bundle,
        "yaml": bundle_to_yaml(bundle)
    }


# def complete_plan_definition(research_subject_id: str, plan_definition_id: str, config: Config):
#     """
#     Mark the CarePlan for the patient complete
#     """
#     client = Client(
#         config.endpoint_url,
#         auth=Auth(
#             method="basic",
#             credentials=AuthCredentials(
#                 username=config.fhir_username, password=config.fhir_password
#             ),
#         ),
#     )
#     # TODO: ensure plan definition is consistent with ResearchSubject
#     research_subject = client.read(ResearchSubject, research_subject_id)
#     assert research_subject is not None, f"ResearchSubject with ID {research_subject_id} not found."
#     plan_definition = client.read(PlanDefinition, plan_definition_id)
#     assert plan_definition is not None, f"PlanDefinition with ID {plan_definition_id} not found."
#     found = None
#     # search for careplan
#     for care_plan in client.search(CarePlan, dict(subject=Reference(reference=research_subject.subject.reference))):
#         if care_plan.based_on.reference != plan_definition.:
#             continue
#         if care_plan.status in ("active"):
#             found = care_plan
#             break
#     if found is None:
#         raise ValueError(f"No active CarePlan found for ResearchSubject {research_subject_id} and PlanDefinition {plan_definition_id}")
#     found.status = "completed"
#     client.update(found)


def execute(
    research_subject_id: str,
    plan_definition_ids: List[str],
    visit_date: datetime.date,
    config: Config,
):
    """
    Execute a plan definition for a research subject.
    
    Returns:
        List of dictionaries containing:
        - care_plan: CarePlan resource
        - bundle: Bundle resource with all created resources
        - yaml: YAML string representation of the bundle
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
    assert (
        research_subject is not None
    ), f"ResearchSubject with ID {research_subject_id} not found."
    results = []
    for plan_definition_id in plan_definition_ids:
        # TODO: timepoints, visit date should move up
        manifested = manifest_plan_definition(
            plan_definition_id=plan_definition_id,
            research_subject=research_subject,
            visit_date=visit_date,
            client=client,
        )
        assert (
            manifested is not None
        ), f"PlanDefinition with ID {plan_definition_id} not manifested."
        results.append(manifested)
    return results
