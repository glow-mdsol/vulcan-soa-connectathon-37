"""
Report on the patient journey
* Identify the steps taken from enrolment to treatment
* Look at the decisions made at each step
"""

from typing import Dict, List, Any, Optional
from fhirsdk.client import Client, Auth, AuthCredentials
from fhirsdk import ResearchSubject, ResearchStudy, PlanDefinition, Reference, CarePlan
from tasks.common import TransitionGraph
from tasks.config import Config
from tasks.evaluate import get_careplans_for_patient, is_care_plan_completed
try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Warning: graphviz not available. Visual representations will be disabled.")


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
    action_repeat_counters = {}  # Track repeat numbers
    
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
                    # Track repeat number
                    if action_id not in action_repeat_counters:
                        action_repeat_counters[action_id] = 0
                    action_repeat_counters[action_id] += 1
                    repeat_number = action_repeat_counters[action_id]
                    
                    care_plan_by_action[action_id] = cp_data
                    
                    # Build journey entry
                    journey_entry = {
                        "action_id": action_id,
                        "action_title": action_details["title"],
                        "plan_definition_id": plan_def_id,
                        "care_plan_id": cp_data["care_plan_id"],
                        "status": care_plan.status,
                        "is_completed": is_care_plan_completed(care_plan),
                        "repeat_number": repeat_number,
                        "is_repeatable": graph.is_repeatable(action_id)
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
        repeat_num = entry.get('repeat_number', 1)
        is_repeatable = entry.get('is_repeatable', False)
        cycle_label = f" (C{repeat_num})" if repeat_num > 1 or is_repeatable else ""
        print(f"{i}. {status_icon} {entry['action_title']}{cycle_label}")
        print(f"   Action ID: {entry['action_id']}")
        print(f"   PlanDefinition: {entry['plan_definition_id']}")
        print(f"   CarePlan: {entry['care_plan_id']}")
        print(f"   Status: {entry['status']}")
        if is_repeatable:
            print(f"   Cycle: {repeat_num}")
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


def visualize_patient_journey(report: Dict[str, Any], output_path: Optional[str] = None, view: bool = True) -> Optional[str]:
    """
    Create a visual representation of the patient journey using graphviz.
    
    Args:
        report: Report dictionary from generate_research_subject_report
        output_path: Optional path to save the visualization (without extension)
        view: Whether to automatically open the visualization (default: True)
    
    Returns:
        Path to the generated file, or None if graphviz is not available
    """
    if not GRAPHVIZ_AVAILABLE:
        print("Error: graphviz library not available. Install with: pip install graphviz")
        return None
    
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Patient Journey', format='png')
    dot.attr(rankdir='TB')  # Top to bottom layout
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    dot.attr('edge', fontname='Arial', fontsize='10')
    
    # Create sets for quick lookup and map journey entries by action_id
    completed_actions = {j['action_id'] for j in report['patient_journey'] if j['is_completed']}
    active_actions = {j['action_id'] for j in report['patient_journey'] if j['status'] in ['active', 'on-hold']}
    
    # Build map of action_id to journey entries (for cycle numbers)
    action_journey_map = {}
    for journey_entry in report['patient_journey']:
        action_id = journey_entry['action_id']
        if action_id not in action_journey_map:
            action_journey_map[action_id] = []
        action_journey_map[action_id].append(journey_entry)
    
    # Track which actions are decision points and their outcomes
    decision_outcomes = {}
    for decision in report['decision_points']:
        if decision['decision_made']:
            taken_options = [opt for opt in decision['options'] if opt['was_taken']]
            if taken_options:
                decision_outcomes[decision['action_id']] = taken_options
    
    # Add all nodes (or node instances for repeated actions)
    node_instances = {}  # Track created node IDs for repeated actions
    
    for action in report['protocol_structure']['all_actions']:
        action_id = action['action_id']
        title = action['title']
        
        # Check if this action has been performed and how many times
        journey_entries = action_journey_map.get(action_id, [])
        
        if not journey_entries:
            # Action not yet performed - create single node
            # Determine node color and style based on status
            fillcolor = '#E8E8E8'  # Light gray for not started
            color = '#808080'  # Gray border
            label_suffix = ''
            
            # Check if this is a common event
            if action.get('is_common_event'):
                fillcolor = '#ADD8E6'  # Light blue for common events
                label_suffix += '\n(Common Event)'
            
            # Create node label
            node_label = f"{title}{label_suffix}"
            
            # Use diamond shape for decision points
            if action_id in decision_outcomes:
                dot.node(action_id, label=node_label, fillcolor=fillcolor, color=color, shape='diamond', style='filled')
            else:
                dot.node(action_id, label=node_label, fillcolor=fillcolor, color=color)
            
            node_instances[action_id] = [action_id]
        else:
            # Action has been performed - create node(s) with cycle numbers
            node_instances[action_id] = []
            
            for journey_entry in journey_entries:
                repeat_num = journey_entry.get('repeat_number', 1)
                is_repeatable = journey_entry.get('is_repeatable', False)
                
                # Create unique node ID for this instance
                node_id = f"{action_id}_C{repeat_num}" if is_repeatable or repeat_num > 1 else action_id
                node_instances[action_id].append(node_id)
                
                # Determine node color and style based on status
                if journey_entry['is_completed']:
                    fillcolor = '#90EE90'  # Light green for completed
                    color = '#228B22'  # Dark green border
                    label_suffix = f'\n✓ Completed'
                elif journey_entry['status'] in ['active', 'on-hold']:
                    fillcolor = '#FFD700'  # Gold for active
                    color = '#FF8C00'  # Dark orange border
                    label_suffix = f'\n→ Active'
                else:
                    fillcolor = '#E8E8E8'  # Light gray
                    color = '#808080'  # Gray border
                    label_suffix = ''
                
                # Add cycle number to label if repeatable
                cycle_label = f" (C{repeat_num})" if is_repeatable or repeat_num > 1 else ""
                
                # Check if this is a common event
                if action.get('is_common_event'):
                    fillcolor = '#ADD8E6'  # Light blue for common events
                    label_suffix += '\n(Common Event)'
                
                # Create node label
                node_label = f"{title}{cycle_label}{label_suffix}"
                
                # Use diamond shape for decision points
                if action_id in decision_outcomes and journey_entry == journey_entries[-1]:
                    dot.node(node_id, label=node_label, fillcolor=fillcolor, color=color, shape='diamond', style='filled')
                else:
                    dot.node(node_id, label=node_label, fillcolor=fillcolor, color=color)
    
    # Add decision annotation boxes
    for action_id, taken_options in decision_outcomes.items():
        # Find the last node instance for this decision
        if action_id in node_instances:
            decision_node_id = node_instances[action_id][-1]
            
            # Create annotation node for the decision
            annotation_id = f"{decision_node_id}_decision_info"
            decision_text = "Decision Made:\n"
            for opt in taken_options:
                decision_text += f"→ {opt['target_title']}\n"
            
            # Create a note-style box for the decision
            dot.node(
                annotation_id,
                label=decision_text.strip(),
                shape='note',
                style='filled',
                fillcolor='#FFFACD',  # Light yellow
                color='#DAA520',       # Goldenrod border
                fontsize='10'
            )
            
            # Connect decision node to annotation with invisible edge to position it
            dot.edge(
                decision_node_id,
                annotation_id,
                style='dashed',
                color='#DAA520',
                arrowhead='none',
                constraint='false'  # Don't affect layout
            )
    
    # Add edges based on the protocol structure
    # We'll track which transitions were actually taken
    taken_transitions = set()
    for decision in report['decision_points']:
        for opt in decision['options']:
            if opt['was_taken']:
                taken_transitions.add((decision['action_id'], opt['target_action_id']))
    
    # Build edges from patient journey (actual path taken)
    # Use the actual node IDs including cycle numbers
    for i in range(len(report['patient_journey']) - 1):
        from_entry = report['patient_journey'][i]
        to_entry = report['patient_journey'][i + 1]
        
        from_action = from_entry['action_id']
        to_action = to_entry['action_id']
        
        # Get the actual node IDs (with cycle numbers if applicable)
        from_repeat = from_entry.get('repeat_number', 1)
        to_repeat = to_entry.get('repeat_number', 1)
        from_repeatable = from_entry.get('is_repeatable', False)
        to_repeatable = to_entry.get('is_repeatable', False)
        
        from_node_id = f"{from_action}_C{from_repeat}" if from_repeatable or from_repeat > 1 else from_action
        to_node_id = f"{to_action}_C{to_repeat}" if to_repeatable or to_repeat > 1 else to_action
        
        # Highlight taken path
        dot.edge(from_node_id, to_node_id, color='#228B22', penwidth='2.5', label='')
    
    # Add other possible transitions (not taken) as dashed lines
    for decision in report['decision_points']:
        decision_action = decision['action_id']
        
        # Find the last instance of this decision action
        if decision_action in node_instances:
            last_node_id = node_instances[decision_action][-1]
            
            for opt in decision['options']:
                if not opt['was_taken']:
                    target_action = opt['target_action_id']
                    # Get the node ID for the target (first instance or the not-yet-created node)
                    if target_action in node_instances:
                        target_node_id = node_instances[target_action][0]
                    else:
                        target_node_id = target_action
                    
                    # Show alternative paths as dashed lines
                    dot.edge(
                        last_node_id, 
                        target_node_id, 
                        style='dashed', 
                        color='#808080',
                        label='Not taken'
                    )
    
    # Add a legend
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', style='filled', color='lightgray')
        legend.node('legend_completed', '✓ Completed', fillcolor='#90EE90', shape='box', style='rounded,filled')
        legend.node('legend_active', '→ Active', fillcolor='#FFD700', shape='box', style='rounded,filled')
        legend.node('legend_not_started', 'Not Started', fillcolor='#E8E8E8', shape='box', style='rounded,filled')
        legend.node('legend_common', 'Common Event', fillcolor='#ADD8E6', shape='box', style='rounded,filled')
        legend.node('legend_decision', 'Decision Point', fillcolor='#90EE90', shape='diamond', style='filled')
    
    # Save and/or view
    if output_path:
        file_path = dot.render(output_path, view=view, cleanup=True)
        print(f"\nVisualization saved to: {file_path}")
        return file_path
    elif view:
        # Create a temporary file
        import tempfile
        import os
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"patient_journey_{report['research_subject_id']}")
        file_path = dot.render(temp_path, view=True, cleanup=True)
        print(f"\nVisualization opened: {file_path}")
        return file_path
    else:
        return dot.source


def report_patient_journey(research_subject_id: str, config: Config, visualize: bool = True, output_path: Optional[str] = None):
    """
    Generate and print a research subject report with optional visualization.
    
    Args:
        research_subject_id: The ID of the research subject
        config: Configuration object with FHIR server connection details
        visualize: Whether to create a visual representation (default: True)
        output_path: Optional path to save visualization (without extension)
    
    Returns:
        Tuple of (report dict, visualization path or None)
    """
    report = generate_research_subject_report(research_subject_id, config)
    print_research_subject_report(report)
    
    viz_path = None
    if visualize:
        viz_path = visualize_patient_journey(report, output_path=output_path, view=True)
    
    return report, viz_path
