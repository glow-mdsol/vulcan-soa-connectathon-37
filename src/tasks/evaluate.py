"""
Evaluate the next steps for a research subject
Should reflect:
* ResearchSubject.status
* ResearchStudy.protocol
"""
from typing import Optional
from fhirsdk.client import Client, Auth, AuthCredentials
from fhirsdk import ResearchSubject
from fhirsdk import ResearchStudy
from fhirsdk import PlanDefinition
from fhirsdk import Reference
from fhirsdk import CarePlan
from fhirsdk import Patient
from fhirsdk import RequestOrchestration

from tasks.common import build_transition_graph, TransitionGraph
from tasks.config import Config


def get_care_plan_status(care_plan: CarePlan) -> str:
    """
    Get the status of a care plan.
    
    Args:
        care_plan: CarePlan resource
    
    Returns:
        Status string (e.g., 'completed', 'active', 'draft')
    """
    return care_plan.status if care_plan.status else "unknown"


def is_care_plan_completed(care_plan: CarePlan) -> bool:
    """
    Check if a care plan is completed.
    
    Args:
        care_plan: CarePlan resource
    
    Returns:
        True if the care plan is completed
    """
    return care_plan.status == "completed"

def get_careplans_for_patient(patient_id: str, config: Config):
    """
    Retrieve care plans for a given patient.

    Args:
        patient_id (str): The ID of the patient.
    """
    results = []
    # get the the client
    client = Client(
        config.endpoint_url,
        auth=Auth(
            method="basic",
            credentials=AuthCredentials(
                username=config.fhir_username, password=config.fhir_password
            ),
        ),
    )
    care_plans = client.search(CarePlan, {"patient": f"Patient/{patient_id}"})
    if care_plans.total:
        for entry in care_plans.entry:
            _contained = entry.resource  # type: CarePlan
            _cp = {"care_plan_id": entry.resource.id, "care_plan": _contained}
            # Try to find the PlanDefinition used to create this CarePlan
            based_on = entry.resource.based_on[0]
            req = client.read(RequestOrchestration, based_on.reference.split("/")[-1])
            # This returns a string
            _pdef = req.instantiates_canonical[0]
            if _pdef.startswith("PlanDefinition/"):
                plan_definition_id = _pdef.split("/")[-1]
                plan_definition = client.read(PlanDefinition, plan_definition_id)
                _cp["plan_definition_id"] = plan_definition_id
            results.append(_cp)
    return results


def evaluate(research_subject_id: str, config: Config, is_withdrawing: Optional[bool] = False, ):
    """
    Evaluate a research subject's data.

    Args:
        research_subject_id (str): The ID of the research subject to evaluate.
    """
    # get the research subject
    client = Client(config.endpoint_url, auth=Auth(method="basic", credentials=AuthCredentials(username=config.fhir_username, password=config.fhir_password)))
    research_subject = client.read(ResearchSubject, research_subject_id)
    assert research_subject is not None, f"ResearchSubject with ID {research_subject_id} not found."
    # Get the ResearchStudy associated with the ResearchSubject
    study = client.read(ResearchStudy, research_subject.study.reference.split("/")[-1])
    assert study is not None, f"ResearchStudy with ID {research_subject.study.reference} not found."
    assert study.protocol is not None, f"Protocol not found for ResearchStudy with ID {research_subject.study.reference}."
    protocol: Reference = study.protocol[0]
    # Get the PlanDefinition referenced by the ResearchStudy protocol
    parent_plan = client.read(PlanDefinition, protocol.reference.split("/")[-1])
    assert parent_plan is not None, f"Parent PlanDefinition with ID {protocol.reference} not found."
    assert parent_plan.action is not None, f"Actions not found for PlanDefinition with ID {protocol.reference}."
    # get the events for the patient
    care_plans = get_careplans_for_patient(research_subject.subject.reference.split("/")[-1], config)
    
    # Build the transition graph
    graph = TransitionGraph(parent_plan, client)
    
    # Map care plans to action IDs (based on their plan definition)
    completed_actions = set()
    active_actions = set()
    care_plan_by_action = {}
    
    for cp_data in care_plans:
        care_plan = cp_data["care_plan"]
        plan_def_id = cp_data.get("plan_definition_id")
        
        if not plan_def_id:
            continue
        
        # Find which action in the parent plan references this plan definition
        for action_id in graph.get_all_action_ids():
            action_details = graph.get_action_details(action_id)
            if action_details and action_details.get("definition"):
                # Extract plan ID from canonical URL
                referenced_plan_id = action_details["definition"].split("/")[-1]
                if referenced_plan_id == plan_def_id:
                    care_plan_by_action[action_id] = cp_data
                    
                    # Track status
                    if is_care_plan_completed(care_plan):
                        completed_actions.add(action_id)
                    elif care_plan.status in ["active", "on-hold"]:
                        active_actions.add(action_id)
                    break
    
    # Determine available next actions
    available_actions = []
    next_recommended_actions = []
    
    # Start from the beginning if nothing is completed
    if not completed_actions:
        # If nothing is started, the starting actions are available
        starting_actions = graph.get_starting_actions()
        for action_id in starting_actions:
            if action_id not in active_actions:
                available_actions.append({
                    "action_id": action_id,
                    "condition": None
                })
                next_recommended_actions.append({
                    "action_id": action_id,
                    "condition": None
                })
    else:
        # Find next actions based on completed ones
        for completed_action_id in completed_actions:
            transitions = graph.get_next_transitions(completed_action_id)
            
            for transition in transitions:
                target_id = transition["targetId"]
                condition = transition.get("condition")
                
                # Check if this action is already completed or active
                if target_id not in completed_actions and target_id not in active_actions:
                    # Check if not already in available_actions
                    if not any(a["action_id"] == target_id for a in available_actions):
                        action_info = {
                            "action_id": target_id,
                            "condition": condition,
                            "from_action": completed_action_id
                        }
                        available_actions.append(action_info)
                        
                        # Recommend non-common events first
                        if not graph.is_common_event(target_id):
                            next_recommended_actions.append(action_info)
    
    # Build result
    result = {
        "research_subject_id": research_subject_id,
        "patient_id": research_subject.subject.reference.split("/")[-1],
        "study_id": research_subject.study.reference,
        "completed_actions": list(completed_actions),
        "active_actions": list(active_actions),
        "available_actions": available_actions,
        "next_recommended_actions": next_recommended_actions,
        "care_plans": care_plans,
        "care_plan_by_action": care_plan_by_action
    }
    
    # Print summary
    print(f"\n=== Evaluation for Research Subject: {research_subject_id} ===")
    print(f"\nCompleted Actions ({len(completed_actions)}):")
    for action_id in completed_actions:
        details = graph.get_action_details(action_id)
        cp_data = care_plan_by_action.get(action_id)
        cp_id = cp_data["care_plan_id"] if cp_data else "N/A"
        print(f"  ✓ {action_id}: {details['title']}")
        print(f"     CarePlan: {cp_id}")
    
    print(f"\nActive Actions ({len(active_actions)}):")
    for action_id in active_actions:
        details = graph.get_action_details(action_id)
        cp_data = care_plan_by_action.get(action_id)
        cp_id = cp_data["care_plan_id"] if cp_data else "N/A"
        print(f"  → {action_id}: {details['title']}")
        print(f"     CarePlan: {cp_id}")
    
    print(f"\nAvailable Next Actions ({len(available_actions)}):")
    for action_info in available_actions:
        action_id = action_info["action_id"]
        condition = action_info.get("condition")
        details = graph.get_action_details(action_id)
        plan_def_id = details['definition'].split('/')[-1] if details.get('definition') else "N/A"
        is_common = " (common event)" if graph.is_common_event(action_id) else ""
        print(f"  • {action_id}: {details['title']}{is_common}")
        print(f"     PlanDefinition ID: {plan_def_id}")
        if condition:
            print(f"     Condition: [{condition['kind']}] {condition['expression'] or 'no expression'}")
        if action_info.get("from_action"):
            print(f"     (follows: {action_info['from_action']})")
    
    print(f"\nRecommended Next Actions ({len(next_recommended_actions)}):")
    for action_info in next_recommended_actions:
        action_id = action_info["action_id"]
        condition = action_info.get("condition")
        details = graph.get_action_details(action_id)
        plan_def_id = details['definition'].split('/')[-1] if details.get('definition') else "N/A"
        plan_def = graph.get_plan_definition(action_id)
        plan_title = plan_def.title if plan_def else "N/A"
        print(f"  ⭐ {action_id}: {details['title']}")
        print(f"     PlanDefinition ID: {plan_def_id}")
        print(f"     PlanDefinition Title: {plan_title}")
        if condition:
            print(f"     Condition: [{condition['kind']}] {condition['expression'] or 'no expression'}")
    
    return result
