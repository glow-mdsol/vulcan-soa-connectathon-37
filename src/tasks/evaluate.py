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
from fhirsdk import RequestOrchestration

from tasks.common import TransitionGraph
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
        # iterate through care plans
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
                # We have the plan definition ID, no need to load it
                _cp["plan_definition_id"] = plan_definition_id
            results.append(_cp)
    # sort the care plans by last updated
    results.sort(key=lambda x: x["care_plan"].meta.last_updated if x["care_plan"].meta and x["care_plan"].meta.last_updated else "")
    return results

"""
Fix: 
* e
"""

def evaluate(research_subject_id: str, config: Config, is_withdrawing: Optional[bool] = False, ):
    """
    Evaluate a research subject's data using event-based model.
    
    Each CarePlan represents an event (instantiation) of a protocol action.
    Multiple events can exist for the same action (repeatable cycles).

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
    # get the events (CarePlans) for the patient
    care_plans = get_careplans_for_patient(research_subject.subject.reference.split("/")[-1], config)
    
    # Build the transition graph
    graph = TransitionGraph(parent_plan, client)
    
    # Map CarePlans (events) to action IDs
    # events_by_action: action_id -> list of events (CarePlans)
    events_by_action = {}
    active_events_by_action = {}
    
    # Track repeat numbers for each action as we process care plans
    action_repeat_counters = {}
    
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
                    # Increment repeat counter for this action
                    if action_id not in action_repeat_counters:
                        action_repeat_counters[action_id] = 0
                    action_repeat_counters[action_id] += 1
                    
                    # Add repeat number to the event data
                    cp_data["repeat_number"] = action_repeat_counters[action_id]
                    
                    # Add event to the appropriate list
                    if is_care_plan_completed(care_plan):
                        if action_id not in events_by_action:
                            events_by_action[action_id] = []
                        events_by_action[action_id].append(cp_data)
                    elif care_plan.status in ["active", "on-hold"]:
                        if action_id not in active_events_by_action:
                            active_events_by_action[action_id] = []
                        active_events_by_action[action_id].append(cp_data)
                    break
    
    # Determine available next actions based on events
    available_actions = []
    next_recommended_actions = []
    
    # Get actions that have at least one completed event
    actions_with_completed_events = set(events_by_action.keys())
    actions_with_active_events = set(active_events_by_action.keys())
    
    # Start from the beginning if no events exist
    if not actions_with_completed_events:
        # If nothing is started, the starting actions are available
        starting_actions = graph.get_starting_actions()
        for action_id in starting_actions:
            if action_id not in actions_with_active_events:
                available_actions.append({
                    "action_id": action_id,
                    "condition": None,
                    "event_count": 0
                })
                next_recommended_actions.append({
                    "action_id": action_id,
                    "condition": None,
                    "event_count": 0
                })
    else:
        # Track decision points where a choice has been made
        decision_points_taken = {}
        
        for action_id in actions_with_completed_events:
            transitions = graph.get_next_transitions(action_id)
            
            # Check if any transition from this action has been taken
            taken_targets = set()
            for transition in transitions:
                target_id = transition["targetId"]
                if target_id in actions_with_completed_events or target_id in actions_with_active_events:
                    taken_targets.add(target_id)
            
            if taken_targets:
                decision_points_taken[action_id] = taken_targets
        
        # Helper function to recursively find available actions
        def find_available_from_action(action_id, visited=None):
            """Recursively find available actions from completed events."""
            if visited is None:
                visited = set()
            
            if action_id in visited:
                return []
            
            visited.add(action_id)
            found_actions = []
            
            transitions = graph.get_next_transitions(action_id)
            
            # Check if this is a decision point with an already-taken path
            if action_id in decision_points_taken:
                # Only traverse the path(s) that were actually taken
                taken_paths = decision_points_taken[action_id]
                for transition in transitions:
                    target_id = transition["targetId"]
                    if target_id not in taken_paths:
                        # This path was not taken, skip it
                        continue
                    
                    # This path was taken, continue traversing
                    if target_id in actions_with_completed_events:
                        # Recursively find available actions beyond this action
                        found_actions.extend(find_available_from_action(target_id, visited.copy()))
                    elif target_id not in actions_with_active_events:
                        # This action has no events yet, it's available
                        found_actions.append({
                            "action_id": target_id,
                            "condition": transition.get("condition"),
                            "from_action": action_id,
                            "event_count": 0
                        })
            else:
                # Not a decision point or no decision made yet
                for transition in transitions:
                    target_id = transition["targetId"]
                    condition = transition.get("condition")
                    
                    if target_id not in actions_with_active_events:
                        # Check if this is transitioning back to an action with events (cycle)
                        if target_id in actions_with_completed_events:
                            # This is a cycle - action can be repeated
                            event_count = len(events_by_action[target_id])
                            found_actions.append({
                                "action_id": target_id,
                                "condition": condition,
                                "from_action": action_id,
                                "is_cycle": True,
                                "event_count": event_count
                            })
                            # Also traverse through to find subsequent actions
                            found_actions.extend(find_available_from_action(target_id, visited.copy()))
                        else:
                            # This action has no events yet, it's available
                            found_actions.append({
                                "action_id": target_id,
                                "condition": condition,
                                "from_action": action_id,
                                "event_count": 0
                            })
            
            return found_actions
        
        # Find next actions based on actions with completed events
        for action_id in actions_with_completed_events:
            found = find_available_from_action(action_id)
            for action_info in found:
                # Check if not already in available_actions
                if not any(a["action_id"] == action_info["action_id"] for a in available_actions):
                    available_actions.append(action_info)
                    
                    # Add to recommendations (prioritize non-common events)
                    if not graph.is_common_event(action_info["action_id"]):
                        next_recommended_actions.append(action_info)
    
    # Create ordered list of all events by date for display
    all_events = []
    for action_id, event_list in events_by_action.items():
        for event_data in event_list:
            care_plan = event_data["care_plan"]
            # Get date for sorting
            sort_date = None
            if care_plan.period and care_plan.period.start:
                sort_date = care_plan.period.start
            elif care_plan.created:
                sort_date = care_plan.created
            elif care_plan.meta and care_plan.meta.last_updated:
                sort_date = care_plan.meta.last_updated
            
            all_events.append({
                "action_id": action_id,
                "care_plan_id": event_data["care_plan_id"],
                "date": sort_date,
                "status": "completed",
                "repeat_number": event_data.get("repeat_number", 1)
            })
    
    # Add active events
    for action_id, event_list in active_events_by_action.items():
        for event_data in event_list:
            care_plan = event_data["care_plan"]
            # Get date for sorting
            sort_date = None
            if care_plan.period and care_plan.period.start:
                sort_date = care_plan.period.start
            elif care_plan.created:
                sort_date = care_plan.created
            elif care_plan.meta and care_plan.meta.last_updated:
                sort_date = care_plan.meta.last_updated
            
            all_events.append({
                "action_id": action_id,
                "care_plan_id": event_data["care_plan_id"],
                "date": sort_date,
                "status": "active",
                "repeat_number": event_data.get("repeat_number", 1)
            })
    
    # Sort events by date
    all_events.sort(key=lambda x: (x["date"] is None, x["date"] if x["date"] else ""))
    
    # Find the most recent completed event and add its transitions as available actions
    last_planned_activity = None
    if all_events:
        # Get the most recent completed event (active events are in progress, not last completed)
        completed_events = [e for e in all_events if e["status"] == "completed"]
        if completed_events:
            last_planned_activity = completed_events[-1]  # Last in sorted list
            last_action_id = last_planned_activity["action_id"]
            
            # Get transitions from this last activity
            transitions = graph.get_next_transitions(last_action_id)
            for transition in transitions:
                target_id = transition["targetId"]
                condition = transition.get("condition")
                
                # Check if not already in available_actions
                if not any(a["action_id"] == target_id for a in available_actions):
                    # Check if this action already has events
                    event_count = len(events_by_action.get(target_id, []))
                    is_cycle = target_id in events_by_action
                    
                    # Don't add if it's already active
                    if target_id not in active_events_by_action:
                        action_info = {
                            "action_id": target_id,
                            "condition": condition,
                            "from_action": last_action_id,
                            "event_count": event_count,
                            "is_cycle": is_cycle,
                            "from_last_activity": True
                        }
                        available_actions.append(action_info)
                        
                        # Add to recommendations if not common
                        if not graph.is_common_event(target_id):
                            next_recommended_actions.append(action_info)
    
    # Build result
    result = {
        "research_subject_id": research_subject_id,
        "patient_id": research_subject.subject.reference.split("/")[-1],
        "study_id": research_subject.study.reference,
        "events": all_events,
        "events_by_action": events_by_action,
        "active_events_by_action": active_events_by_action,
        "available_actions": available_actions,
        "next_recommended_actions": next_recommended_actions,
        "care_plans": care_plans,
        "last_planned_activity": last_planned_activity
    }
    
    # Print summary
    print(f"\n=== Evaluation for Research Subject: {research_subject_id} ===")
    print(f"\nCompleted Events ({len([e for e in all_events if e['status'] == 'completed'])}):")
    for event in all_events:
        if event["status"] == "completed":
            details = graph.get_action_details(event["action_id"])
            event_date = event["date"] if event["date"] else "N/A"
            repeat_num = event.get("repeat_number", 1)
            cycle_label = f" (C{repeat_num})" if repeat_num > 1 or graph.is_repeatable(event["action_id"]) else ""
            print(f"  ✓ {event['action_id']}: {details['title']}{cycle_label} (CarePlan: {event['care_plan_id']})")
            print(f"     Date: {event_date}")
    
    print(f"\nActive Events ({len([e for e in all_events if e['status'] == 'active'])}):")
    for event in all_events:
        if event["status"] == "active":
            details = graph.get_action_details(event["action_id"])
            event_date = event["date"].strftime("%Y-%m-%d") if event["date"] else "N/A"
            repeat_num = event.get("repeat_number", 1)
            cycle_label = f" (C{repeat_num})" if repeat_num > 1 or graph.is_repeatable(event["action_id"]) else ""
            print(f"  → {event['action_id']}: {details['title']}{cycle_label} (CarePlan: {event['care_plan_id']})")
            print(f"     Date: {event_date}")
    
    print(f"\nAvailable Next Actions ({len(available_actions)}):")
    import datetime
    
    # Show last planned activity context
    if last_planned_activity:
        last_details = graph.get_action_details(last_planned_activity["action_id"])
        last_date = last_planned_activity["date"]
        print(f"\n  Last Planned Activity: {last_planned_activity['action_id']} - {last_details['title']}")
        print(f"  Date: {last_date}")
        print(f"  CarePlan: {last_planned_activity['care_plan_id']}")
        print()
    
    for action_info in available_actions:
        action_id = action_info["action_id"]
        condition = action_info.get("condition")
        is_cycle = action_info.get("is_cycle", False)
        event_count = action_info.get("event_count", 0)
        from_last = action_info.get("from_last_activity", False)
        details = graph.get_action_details(action_id)
        plan_def_id = details['definition'].split('/')[-1] if details.get('definition') else "N/A"
        is_common = " (common event)" if graph.is_common_event(action_id) else ""
        cycle_marker = f" (CYCLE - completed {event_count}x)" if is_cycle else ""
        last_marker = " ← from last activity" if from_last else ""
        print(f"  • {action_id}: {details['title']}{is_common}{cycle_marker}{last_marker}")
        print(f"     PlanDefinition ID: {plan_def_id}")
        
        # Calculate and show suggested visit date
        suggested_date, window_start, window_end = graph.calculate_suggested_visit_date(
            action_id, 
            datetime.date.today(),  # TODO: Use actual reference date (e.g., study start or last visit)
            event_count
        )
        if suggested_date:
            print(f"     Suggested Visit Date: {suggested_date}")
            if window_start != window_end:
                print(f"     Visit Window: {window_start} to {window_end}")
        
        if event_count > 0:
            print(f"     Previous events: {event_count}")
        
        if condition:
            print(f"     Condition: [{condition['kind']}] {condition['expression'] or 'no expression'}")
        if action_info.get("from_action"):
            print(f"     (follows: {action_info['from_action']})")
    
    print(f"\nRecommended Next Actions ({len(next_recommended_actions)}):")
    for action_info in next_recommended_actions:
        action_id = action_info["action_id"]
        condition = action_info.get("condition")
        is_cycle = action_info.get("is_cycle", False)
        event_count = action_info.get("event_count", 0)
        details = graph.get_action_details(action_id)
        plan_def_id = details['definition'].split('/')[-1] if details.get('definition') else "N/A"
        plan_def = graph.get_plan_definition(action_id)
        plan_title = plan_def.title if plan_def else "N/A"
        cycle_marker = f" (CYCLE #{event_count + 1})" if is_cycle else ""
        print(f"  ⭐ {action_id}: {details['title']}{cycle_marker}")
        print(f"     PlanDefinition ID: {plan_def_id}")
        print(f"     PlanDefinition Title: {plan_title}")
        
        # Calculate and show suggested visit date
        suggested_date, window_start, window_end = graph.calculate_suggested_visit_date(
            action_id, 
            datetime.date.today(),  # TODO: Use actual reference date
            event_count
        )
        if suggested_date:
            print(f"     Suggested Visit Date: {suggested_date}")
            if window_start != window_end:
                print(f"     Visit Window: {window_start} to {window_end}")
        
        if event_count > 0:
            print(f"     Previous events: {event_count}")
        
        if condition:
            print(f"     Condition: [{condition['kind']}] {condition['expression'] or 'no expression'}")
    
    return result
