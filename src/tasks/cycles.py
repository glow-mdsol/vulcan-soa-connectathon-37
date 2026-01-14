"""
Helper functions for working with cycle-based protocols.
Supports analysis and management of repeatable treatment cycles.
"""

from typing import Dict, List, Optional, Tuple, Any
import json
import datetime
from pathlib import Path
from fhirsdk import PlanDefinition
from tasks.common import TransitionGraph


def load_plan_definition_from_json(file_path: str) -> PlanDefinition:
    """
    Load a PlanDefinition from a JSON file.
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        PlanDefinition resource
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return PlanDefinition.model_validate(data)


def identify_cycle_actions(graph: TransitionGraph) -> Dict[str, List[str]]:
    """
    Identify cycle-based actions in a protocol.
    Groups actions by cycle patterns (e.g., C1, C2, C3).
    
    Args:
        graph: TransitionGraph instance
    
    Returns:
        Dictionary mapping cycle identifiers to action IDs
    """
    cycles = {}
    
    for action_id in graph.get_all_action_ids():
        details = graph.get_action_details(action_id)
        title = details.get("title", "")
        
        # Extract cycle identifier from title (e.g., "C1D1" -> "C1", "Cycle 2" -> "C2")
        if "C" in title and "D" in title:
            # Format: C1D1, C2D15, etc.
            parts = title.split("D")
            if parts[0].startswith("C"):
                cycle_id = parts[0]
                if cycle_id not in cycles:
                    cycles[cycle_id] = []
                cycles[cycle_id].append(action_id)
        elif title.lower().startswith("cycle"):
            # Format: "Cycle 1", "Cycle 2", etc.
            parts = title.split()
            if len(parts) >= 2:
                cycle_id = f"C{parts[1]}"
                if cycle_id not in cycles:
                    cycles[cycle_id] = []
                cycles[cycle_id].append(action_id)
    
    return cycles


def get_repeatable_cycles(graph: TransitionGraph) -> List[Dict[str, Any]]:
    """
    Get all repeatable cycle actions from the protocol.
    
    Args:
        graph: TransitionGraph instance
    
    Returns:
        List of dictionaries with cycle information
    """
    repeatable = []
    
    for action_id in graph.get_all_action_ids():
        if graph.is_repeatable(action_id):
            details = graph.get_action_details(action_id)
            repeat_interval = graph.get_repeat_interval(action_id)
            timepoint = graph.get_timepoint_info(action_id)
            
            cycle_info = {
                "action_id": action_id,
                "title": details.get("title"),
                "definition": details.get("definition"),
                "repeat_interval": repeat_interval,
                "timepoint": timepoint
            }
            repeatable.append(cycle_info)
    
    return repeatable


def calculate_cycle_schedule(
    graph: TransitionGraph,
    cycle_action_id: str,
    start_date: datetime.date,
    number_of_cycles: int
) -> List[Dict[str, Any]]:
    """
    Calculate a complete schedule for a repeatable cycle.
    
    Args:
        graph: TransitionGraph instance
        cycle_action_id: Action ID of the cycle to schedule
        start_date: Start date for the first cycle
        number_of_cycles: Number of cycles to schedule
    
    Returns:
        List of dictionaries with cycle schedule information
    """
    schedule = []
    
    for cycle_num in range(number_of_cycles):
        suggested_date, window_start, window_end = graph.calculate_suggested_visit_date(
            cycle_action_id,
            start_date,
            cycle_num
        )
        
        if suggested_date:
            details = graph.get_action_details(cycle_action_id)
            schedule.append({
                "cycle_number": cycle_num + 1,
                "action_id": cycle_action_id,
                "title": details.get("title"),
                "suggested_date": suggested_date,
                "window_start": window_start,
                "window_end": window_end
            })
    
    return schedule


def analyze_cycle_dependencies(
    graph: TransitionGraph,
    cycle_actions: Dict[str, List[str]]
) -> Dict[str, Dict[str, Any]]:
    """
    Analyze dependencies between cycle actions.
    Identifies which cycles must complete before others can start.
    
    Args:
        graph: TransitionGraph instance
        cycle_actions: Dictionary mapping cycle IDs to action IDs
    
    Returns:
        Dictionary with dependency analysis
    """
    dependencies = {}
    
    for cycle_id, action_ids in cycle_actions.items():
        cycle_deps = {
            "cycle_id": cycle_id,
            "actions": action_ids,
            "depends_on": [],
            "enables": []
        }
        
        for action_id in action_ids:
            # Check what this action enables
            transitions = graph.get_next_transitions(action_id)
            for transition in transitions:
                target_id = transition["targetId"]
                # Find which cycle this target belongs to
                for other_cycle_id, other_actions in cycle_actions.items():
                    if target_id in other_actions and other_cycle_id != cycle_id:
                        if other_cycle_id not in cycle_deps["enables"]:
                            cycle_deps["enables"].append(other_cycle_id)
            
            # Check what enables this action
            for other_action_id in graph.get_all_action_ids():
                transitions = graph.get_next_transitions(other_action_id)
                for transition in transitions:
                    if transition["targetId"] == action_id:
                        # Find which cycle this source belongs to
                        for other_cycle_id, other_actions in cycle_actions.items():
                            if other_action_id in other_actions and other_cycle_id != cycle_id:
                                if other_cycle_id not in cycle_deps["depends_on"]:
                                    cycle_deps["depends_on"].append(other_cycle_id)
        
        dependencies[cycle_id] = cycle_deps
    
    return dependencies


def get_cycle_timeline(
    graph: TransitionGraph,
    start_date: datetime.date,
    max_cycles: int = 10
) -> List[Dict[str, Any]]:
    """
    Generate a complete timeline for all cycle-based actions.
    
    Args:
        graph: TransitionGraph instance
        start_date: Protocol start date
        max_cycles: Maximum number of cycles to project
    
    Returns:
        List of timeline events sorted by date
    """
    timeline = []
    cycles = identify_cycle_actions(graph)
    
    for cycle_id, action_ids in cycles.items():
        for action_id in action_ids:
            if graph.is_repeatable(action_id):
                # Calculate schedule for repeatable cycles
                cycle_schedule = calculate_cycle_schedule(
                    graph,
                    action_id,
                    start_date,
                    max_cycles
                )
                timeline.extend(cycle_schedule)
            else:
                # Single occurrence
                suggested_date, window_start, window_end = graph.calculate_suggested_visit_date(
                    action_id,
                    start_date,
                    0
                )
                
                if suggested_date:
                    details = graph.get_action_details(action_id)
                    timeline.append({
                        "cycle_number": 1,
                        "action_id": action_id,
                        "title": details.get("title"),
                        "suggested_date": suggested_date,
                        "window_start": window_start,
                        "window_end": window_end
                    })
    
    # Sort by suggested date
    timeline.sort(key=lambda x: x["suggested_date"])
    
    return timeline


def print_cycle_analysis(graph: TransitionGraph):
    """
    Print a comprehensive analysis of cycle-based protocol.
    
    Args:
        graph: TransitionGraph instance
    """
    print("=" * 80)
    print("CYCLE-BASED PROTOCOL ANALYSIS")
    print("=" * 80)
    
    # Identify cycles
    cycles = identify_cycle_actions(graph)
    print(f"\nIdentified Cycles: {len(cycles)}")
    for cycle_id, action_ids in sorted(cycles.items()):
        print(f"\n  {cycle_id}:")
        for action_id in action_ids:
            details = graph.get_action_details(action_id)
            repeatable = " (REPEATABLE)" if graph.is_repeatable(action_id) else ""
            print(f"    - {action_id}: {details['title']}{repeatable}")
    
    # Repeatable cycles
    repeatable_cycles = get_repeatable_cycles(graph)
    print(f"\n{'─' * 80}")
    print(f"REPEATABLE CYCLES: {len(repeatable_cycles)}")
    print(f"{'─' * 80}")
    
    for cycle in repeatable_cycles:
        print(f"\n  {cycle['action_id']}: {cycle['title']}")
        if cycle['repeat_interval']:
            print(f"    Repeat Interval: {cycle['repeat_interval']['value']} {cycle['repeat_interval']['unit']}")
        if cycle['timepoint']:
            tp = cycle['timepoint']
            if tp.get('soaPlannedTimePoint'):
                point = tp['soaPlannedTimePoint']
                print(f"    Planned Timepoint: {point['value']} {point['unit']}")
    
    # Dependencies
    if cycles:
        print(f"\n{'─' * 80}")
        print("CYCLE DEPENDENCIES")
        print(f"{'─' * 80}")
        
        deps = analyze_cycle_dependencies(graph, cycles)
        for cycle_id, dep_info in sorted(deps.items()):
            print(f"\n  {cycle_id}:")
            if dep_info['depends_on']:
                print(f"    Depends on: {', '.join(dep_info['depends_on'])}")
            if dep_info['enables']:
                print(f"    Enables: {', '.join(dep_info['enables'])}")
            if not dep_info['depends_on'] and not dep_info['enables']:
                print(f"    No dependencies")
    
    print("\n" + "=" * 80)


def export_cycle_schedule_to_csv(
    timeline: List[Dict[str, Any]],
    output_path: str
):
    """
    Export cycle schedule to CSV file.
    
    Args:
        timeline: List of timeline events
        output_path: Path to output CSV file
    """
    import csv
    
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['cycle_number', 'action_id', 'title', 'suggested_date', 
                     'window_start', 'window_end']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for event in timeline:
            writer.writerow(event)
    
    print(f"Schedule exported to {output_path}")
