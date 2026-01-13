"""
Report on the patient journey
* Identify the steps taken from enrolment to treatment
* Look at the decisions made at each step
"""

from typing import Dict, List, Any
from fhirsdk.client import Client, Auth, AuthCredentials
from fhirsdk import ResearchSubject, ResearchStudy, PlanDefinition, Reference, CarePlan
from tasks.common import TransitionGraph
from tasks.config import Config
from tasks.evaluate import get_careplans_for_patient, is_care_plan_completed


def generate_research_subject_report(research_subject_id: str, config: Config) -> Dict[str, Any]:
    """
    Generate a comprehensive report for a research subject showing all activities,
    the protocol plan, and the decisions made throughout the study.
    
    Args:
        research_subject_id: The ID of the research subject to report on
        config: Configuration object with FHIR server connection details
    
    Returns:
        Dictionary containing the complete report structure
    """
    # Initialize FHIR client
    client = Client(
        config.endpoint_url,
        auth=Auth(
            method="basic",
            credentials=AuthCredentials(
                username=config.fhir_username, 
                password=config.fhir_password
            ),
        ),
    )
    
    # Get research subject
    research_subject = client.read(ResearchSubject, research_subject_id)
    assert research_subject is not None, f"ResearchSubject with ID {research_subject_id} not found."
    
    # Get study and protocol
    study = client.read(ResearchStudy, research_subject.study.reference.split("/")[-1])
    assert study is not None, f"ResearchStudy not found."
    assert study.protocol is not None, f"Protocol not found for ResearchStudy."
    
    protocol: Reference = study.protocol[0]
    parent_plan = client.read(PlanDefinition, protocol.reference.split("/")[-1])
    assert parent_plan is not None, f"Parent PlanDefinition not found."
    
    # Build transition graph
    graph = TransitionGraph(parent_plan, client)
    
    # Get all care plans
    patient_id = research_subject.subject.reference.split("/")[-1]
    care_plans = get_careplans_for_patient(patient_id, config)
    
    # Map care plans to actions and build journey
    action_journey = []
    care_plan_by_action = {}
    decision_points = []
    
    for cp_data in care_plans:
        care_plan = cp_data["care_plan"]
        plan_def_id = cp_data.get("plan_definition_id")
        
        if not plan_def_id:
            continue
        
        # Find which action this care plan corresponds to
        for action_id in graph.get_all_action_ids():
            action_details = graph.get_action_details(action_id)
            if action_details and action_details.get("definition"):
                referenced_plan_id = action_details["definition"].split("/")[-1]
                if referenced_plan_id == plan_def_id:
                    care_plan_by_action[action_id] = cp_data
                    
                    # Build journey entry
                    journey_entry = {
                        "action_id": action_id,
                        "action_title": action_details["title"],
                        "plan_definition_id": plan_def_id,
                        "care_plan_id": cp_data["care_plan_id"],
                        "status": care_plan.status,
                        "is_completed": is_care_plan_completed(care_plan)
                    }
                    action_journey.append(journey_entry)
                    break
    
    # Identify decision points in the protocol
    for action_id in graph.get_all_action_ids():
        transitions = graph.get_next_transitions(action_id)
        
        # A decision point has multiple transitions
        if len(transitions) > 1:
            action_details = graph.get_action_details(action_id)
            decision_entry = {
                "action_id": action_id,
                "action_title": action_details["title"],
                "options": []
            }
            
            # Check which path was taken
            for transition in transitions:
                target_id = transition["targetId"]
                target_details = graph.get_action_details(target_id)
                condition = transition.get("condition")
                
                was_taken = target_id in care_plan_by_action
                
                option_entry = {
                    "target_action_id": target_id,
                    "target_title": target_details["title"] if target_details else "Unknown",
                    "condition": condition,
                    "was_taken": was_taken
                }
                
                if was_taken:
                    option_entry["care_plan_id"] = care_plan_by_action[target_id]["care_plan_id"]
                    option_entry["status"] = care_plan_by_action[target_id]["care_plan"].status
                
                decision_entry["options"].append(option_entry)
            
            # Only add if a decision was actually made
            if any(opt["was_taken"] for opt in decision_entry["options"]):
                decision_entry["decision_made"] = True
            else:
                decision_entry["decision_made"] = False
            
            decision_points.append(decision_entry)
    
    # Build the complete protocol path
    starting_actions = graph.get_starting_actions()
    protocol_structure = {
        "starting_actions": [
            {
                "action_id": aid,
                "title": graph.get_action_details(aid)["title"]
            } for aid in starting_actions
        ],
        "all_actions": [
            {
                "action_id": aid,
                "title": details["title"],
                "definition": details.get("definition"),
                "has_multiple_transitions": len(graph.get_next_transitions(aid)) > 1,
                "is_common_event": graph.is_common_event(aid)
            } for aid, details in [(aid, graph.get_action_details(aid)) for aid in graph.get_all_action_ids()]
        ]
    }
    
    # Build final report
    report = {
        "research_subject_id": research_subject_id,
        "patient_id": patient_id,
        "study_id": research_subject.study.reference,
        "study_title": study.title if hasattr(study, 'title') else None,
        "protocol_plan_id": parent_plan.id,
        "protocol_plan_title": parent_plan.title,
        "protocol_structure": protocol_structure,
        "patient_journey": action_journey,
        "decision_points": decision_points,
        "total_activities": len(action_journey),
        "completed_activities": sum(1 for j in action_journey if j["is_completed"]),
        "active_activities": sum(1 for j in action_journey if j["status"] in ["active", "on-hold"]),
        "decisions_made": sum(1 for d in decision_points if d["decision_made"])
    }
    
    return report


def print_research_subject_report(report: Dict[str, Any]):
    """
    Pretty print a research subject report.
    
    Args:
        report: Report dictionary from generate_research_subject_report
    """
    print("=" * 80)
    print(f"RESEARCH SUBJECT REPORT")
    print("=" * 80)
    print(f"\nResearch Subject ID: {report['research_subject_id']}")
    print(f"Patient ID: {report['patient_id']}")
    print(f"Study: {report['study_title'] or report['study_id']}")
    print(f"Protocol: {report['protocol_plan_title']} ({report['protocol_plan_id']})")
    
    print(f"\n{'─' * 80}")
    print("SUMMARY")
    print(f"{'─' * 80}")
    print(f"Total Activities: {report['total_activities']}")
    print(f"  Completed: {report['completed_activities']}")
    print(f"  Active: {report['active_activities']}")
    print(f"Decisions Made: {report['decisions_made']}")
    
    print(f"\n{'─' * 80}")
    print("PATIENT JOURNEY")
    print(f"{'─' * 80}")
    for i, entry in enumerate(report['patient_journey'], 1):
        status_icon = "✓" if entry['is_completed'] else "→" if entry['status'] == "active" else "○"
        print(f"{i}. {status_icon} {entry['action_title']}")
        print(f"   Action ID: {entry['action_id']}")
        print(f"   PlanDefinition: {entry['plan_definition_id']}")
        print(f"   CarePlan: {entry['care_plan_id']}")
        print(f"   Status: {entry['status']}")
        print()
    
    if report['decision_points']:
        print(f"{'─' * 80}")
        print("DECISION POINTS")
        print(f"{'─' * 80}")
        for i, decision in enumerate(report['decision_points'], 1):
            decision_status = "✓ Decision Made" if decision['decision_made'] else "○ Pending"
            print(f"{i}. {decision_status}: {decision['action_title']}")
            print(f"   Action ID: {decision['action_id']}")
            print(f"   Options:")
            for opt in decision['options']:
                taken_marker = "  ➜ TAKEN" if opt['was_taken'] else "  ○ Not taken"
                print(f"     {taken_marker}: {opt['target_title']}")
                if opt.get('condition'):
                    cond = opt['condition']
                    print(f"        Condition: [{cond['kind']}] {cond['expression'] or 'no expression'}")
                if opt['was_taken']:
                    print(f"        CarePlan: {opt['care_plan_id']}")
                    print(f"        Status: {opt['status']}")
            print()
    
    print("=" * 80)


def report_patient_journey(research_subject_id: str, config: Config):
    """
    Generate and print a research subject report.
    
    Args:
        research_subject_id: The ID of the research subject
        config: Configuration object with FHIR server connection details
    """
    report = generate_research_subject_report(research_subject_id, config)
    print_research_subject_report(report)
    return report
