from fhirsdk.client import Client, Auth, AuthCredentials
from typing import List, Dict, Set, Optional
from fhirsdk import CarePlan, ResearchStudy, PlanDefinition, Reference, Extension

import logging
logger = logging.getLogger(__name__)


def get_plan_definitions_for_study(study_id: str, config):
    """
    Retrieve the plan definitions associated with a given research study.

    Args:
        study_id (str): The ID of the research study.
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
    research_study = client.read(ResearchStudy, study_id)
    assert research_study, f"ResearchStudy with ID {study_id} not found"
    assert research_study.protocol, (
        f"No protocol associated with ResearchStudy ID {study_id}"
    )
    plan_definitions = {}

    for plan_reference in research_study.protocol:
        assert plan_reference, f"No plan associated with ResearchStudy ID {study_id}"
        logger.info(f"Loading Study Plan from reference: {plan_reference.reference}")
        plan_id = plan_reference.reference.split("/")[-1]
        study_plan = client.read(PlanDefinition, plan_id)
        assert study_plan, f"PlanDefinition with ID {plan_id} not found"
        for act in study_plan.action:
            if act.definition_canonical:
                plan_def_id = act.definition_canonical.split("/")[-1]
                plan = client.read(PlanDefinition, plan_def_id)
                assert plan, f"PlanDefinition with ID {plan_def_id} not found"
                plan_definitions.setdefault(study_plan.id, []).append(plan)
        plan_definitions[plan_id] = study_plan
    return plan_definitions

def get_plan_for_study(study_id: str, config):
    """
    Retrieve the plan associated with a given research study.

    Args:
        study_id (str): The ID of the research study.
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
    research_study = client.read(ResearchStudy, study_id)
    assert research_study, f"ResearchStudy with ID {study_id} not found"
    assert research_study.protocol, (
        f"No protocol associated with ResearchStudy ID {study_id}"
    )
    plan_reference = research_study.protocol[0].reference
    assert plan_reference, f"No plan associated with ResearchStudy ID {study_id}"
    plan_id = plan_reference.split("/")[-1]
    plan = client.read(PlanDefinition, plan_id)
    assert plan, f"PlanDefinition with ID {plan_id} not found"
    return plan

def process_study_plan(plan: PlanDefinition):
    """
    Process the study plan to extract relevant information.
    
    :param plan: Description
    :type plan: PlanDefinition
    """
    study_plan = {}
    for action in plan.action:
        action_dict = {
            "id": action.id,
            "title": action.title,
            "description": action.description,
            "definition": action.definition_canonical,
            "extensions": {},
            "next": [],
            "actions": []
        }
        if action.extension:
            for ext in action.extension:
                action_dict["extensions"][ext.url] = unpack_extension(ext)
        if action.action:
            for sub_action in action.action:
                sub_action_dict = {
                    "id": sub_action.id,
                    "title": sub_action.title,
                    "description": sub_action.description,
                    "definition": sub_action.definition_canonical,
                    "conditions": sub_action.condition,
                    "extensions": {}
                }
                if sub_action.extension:
                    for ext in sub_action.extension:
                        _extension = unpack_extension(ext)
                        sub_action_dict["extensions"][_extension["type"]] = _extension
                        if _extension["type"] == "soaTransition":
                            transition = {
                                "targetId": _extension["soaTargetId"],
                                "condition": sub_action.condition
                            }
                            action_dict["next"].append(transition)
                action_dict["actions"].append(sub_action_dict)
        study_plan[action.id] = action_dict       
    # need to work out what the 
    for planned_id, planned_action in study_plan.items():
        if planned_action["definition"]:
            for possible_next_id, possible_next_action in study_plan.items():
                if possible_next_id != planned_id:
                    if possible_next_action["definition"] == planned_action["definition"]:
                        study_plan[planned_id]["next"].append(possible_next_id)
    return study_plan


class TransitionGraph:
    """
    Object-oriented wrapper for the transition graph that provides
    convenient methods for querying transitions and accessing PlanDefinitions.
    """
    
    def __init__(self, plan: PlanDefinition, client: Optional[Client] = None):
        """
        Initialize the transition graph from a PlanDefinition.
        
        :param plan: PlanDefinition resource
        :param client: Optional FHIR client for fetching referenced PlanDefinitions
        """
        self.plan = plan
        self.client = client
        self._graph = {}  # action.id -> list of transitions
        self._actions = {}  # action.id -> action details
        self._incoming_refs = set()
        self._incoming_count = {}
        self._plan_cache = {}  # Cache for loaded PlanDefinitions
        
        self._build_graph()
    
    def _build_graph(self):
        """Build the internal graph structure."""
        for action in self.plan.action:
            action_id = action.id
            self._graph[action_id] = []
            
            # Extract timepoint and repeat information
            timepoint_info = None
            repeat_allowed = False
            repeat_interval = None
            
            _extensions = {}
            if action.extension:
                for ext in action.extension:
                    _extension = unpack_extension(ext)
                    if _extension["type"] == "soaPlannedTimepoint":
                        timepoint_info = _extension
                        repeat_allowed = _extension.get("soaRepeatAllowed", False)
                        repeat_interval = _extension.get("soaRepeatInterval")
                    _extensions[_extension["type"]] = _extension

            self._actions[action_id] = {
                "id": action.id,
                "title": action.title,
                "description": action.description,
                "definition": action.definition_canonical,
                "type": "action",
                "timepoint": timepoint_info,
                "repeat_allowed": repeat_allowed,
                "repeat_interval": repeat_interval,
                "extensions": _extensions
            }
            
            # Process sub-actions to find soaTransition extensions
            if action.action:
                for sub_action in action.action:
                    if sub_action.extension:
                        for ext in sub_action.extension:
                            _extension = unpack_extension(ext)
                            if _extension["type"] == "soaTransition":
                                target_id = _extension.get("soaTargetId")
                                if target_id:
                                    condition_info = None
                                    if sub_action.condition:
                                        condition_info = {
                                            "kind": sub_action.condition[0].kind if sub_action.condition else None,
                                            "expression": sub_action.condition[0].expression.expression if sub_action.condition and sub_action.condition[0].expression else None
                                        }
                                    transition = {
                                        "targetId": target_id,
                                        "condition": condition_info
                                    }
                                    self._graph[action_id].append(transition)
                                    self._incoming_refs.add(target_id)
        
        # Count incoming edges (to identify the starting actions and common events)
        for action_id in self._graph.keys():
            self._incoming_count[action_id] = 0
        for transitions in self._graph.values():
            for transition in transitions:
                target_id = transition["targetId"]
                if target_id in self._incoming_count:
                    self._incoming_count[target_id] += 1
    
    def get_starting_actions(self) -> List[str]:
        """Get list of action IDs with no incoming references."""
        return [action_id for action_id in self._graph.keys() 
                if action_id not in self._incoming_refs]
    
    def get_next_transitions(self, action_id: str) -> List[Dict]:
        """
        Get all transitions from the given action.
        
        :param action_id: The action ID to query
        :return: List of transition dictionaries with targetId and condition
        """
        return self._graph.get(action_id, [])
    
    def get_action_details(self, action_id: str) -> Optional[Dict]:
        """
        Get details for a specific action.
        
        :param action_id: The action ID to query
        :return: Dictionary with action details or None if not found
        """
        return self._actions.get(action_id)
    
    def get_plan_definition(self, action_id: str) -> Optional[PlanDefinition]:
        """
        Get the PlanDefinition referenced by the action's definition_canonical.
        Uses the client to fetch if available, caches results.
        
        :param action_id: The action ID to query
        :return: PlanDefinition or None if not available or no client provided
        """
        if not self.client:
            return None
        
        action = self._actions.get(action_id)
        if not action or not action.get("definition"):
            return None
        
        definition_url = action["definition"]
        
        # Check cache first
        if definition_url in self._plan_cache:
            return self._plan_cache[definition_url]
        
        # Extract plan ID from canonical URL
        plan_id = definition_url.split("/")[-1]
        
        try:
            plan_def = self.client.read(PlanDefinition, plan_id)
            self._plan_cache[definition_url] = plan_def
            return plan_def
        except Exception as e:
            print(f"Error fetching PlanDefinition {plan_id}: {e}")
            return None
    
    def is_common_event(self, action_id: str) -> bool:
        """
        Check if an action is a common event (has multiple incoming edges).
        
        :param action_id: The action ID to check
        :return: True if the action has more than one incoming edge
        """
        return self._incoming_count.get(action_id, 0) > 1
    
    def get_incoming_count(self, action_id: str) -> int:
        """
        Get the number of incoming edges for an action.
        
        :param action_id: The action ID to check
        :return: Number of incoming edges
        """
        return self._incoming_count.get(action_id, 0)
    
    def is_repeatable(self, action_id: str) -> bool:
        """
        Check if an action can be repeated.
        
        :param action_id: The action ID to check
        :return: True if the action has soaRepeatAllowed=true
        """
        action = self._actions.get(action_id)
        return action.get("repeat_allowed", False) if action else False
    
    def get_repeat_interval(self, action_id: str) -> Optional[Dict]:
        """
        Get the repeat interval for an action.
        
        :param action_id: The action ID to check
        :return: Dictionary with repeat interval info or None
        """
        action = self._actions.get(action_id)
        return action.get("repeat_interval") if action else None
    
    def get_timepoint_info(self, action_id: str) -> Optional[Dict]:
        """
        Get the timepoint information for an action.
        
        :param action_id: The action ID to check
        :return: Dictionary with timepoint info or None
        """
        action = self._actions.get(action_id)
        return action.get("timepoint") if action else None
    
    def calculate_suggested_visit_date(self, action_id: str, reference_date, completed_count: int = 0):
        """
        Calculate suggested visit date based on soaPlannedTimepoint.
        
        :param action_id: The action ID to calculate for
        :param reference_date: Reference date (e.g., study start date or last visit date)
        :param completed_count: Number of times this action has been completed (for repeatable actions)
        :return: Tuple of (suggested_date, window_start, window_end) or (None, None, None)
        """
        import datetime
        
        timepoint = self.get_timepoint_info(action_id)
        if not timepoint:
            return None, None, None
        
        # Base offset from reference date
        planned_timepoint = timepoint.get("soaPlannedTimePoint")
        if planned_timepoint:
            value = planned_timepoint["value"]
            unit = planned_timepoint["unit"]
            
            # Add repeat interval if this is a repeat
            if completed_count > 0:
                repeat_interval = self.get_repeat_interval(action_id)
                if repeat_interval:
                    value += repeat_interval["value"] * completed_count
            
            # Convert to days (simplified - assumes units are in days or weeks)
            if unit in ["d", "day", "days"]:
                days_offset = value
            elif unit in ["wk", "week", "weeks"]:
                days_offset = value * 7
            elif unit in ["mo", "month", "months"]:
                days_offset = value * 30  # Approximate
            else:
                days_offset = value  # Fallback
            
            suggested_date = reference_date + datetime.timedelta(days=days_offset)
            
            # Calculate window if range is provided
            planned_range = timepoint.get("soaPlannedRange")
            if planned_range:
                low_value = planned_range["low"]["value"]
                high_value = planned_range["high"]["value"]
                range_unit = planned_range["low"]["unit"]
                
                # Convert range to days
                if range_unit in ["d", "day", "days"]:
                    low_days = low_value
                    high_days = high_value
                elif range_unit in ["wk", "week", "weeks"]:
                    low_days = low_value * 7
                    high_days = high_value * 7
                else:
                    low_days = low_value
                    high_days = high_value
                
                window_start = reference_date + datetime.timedelta(days=low_days)
                window_end = reference_date + datetime.timedelta(days=high_days)
            else:
                # Use duration if available
                planned_duration = timepoint.get("soaPlannedDuration")
                if planned_duration:
                    duration_value = planned_duration["value"]
                    duration_unit = planned_duration["unit"]
                    
                    if duration_unit in ["d", "day", "days"]:
                        duration_days = duration_value
                    else:
                        duration_days = duration_value
                    
                    window_start = suggested_date - datetime.timedelta(days=duration_days/2)
                    window_end = suggested_date + datetime.timedelta(days=duration_days/2)
                else:
                    window_start = suggested_date
                    window_end = suggested_date
            
            return suggested_date, window_start, window_end
        
        return None, None, None
    
    def get_all_action_ids(self) -> List[str]:
        """Get list of all action IDs in the graph."""
        return list(self._graph.keys())
    
    def traverse_from(self, start_action_id: str, exclude_common_events: bool = True) -> List[str]:
        """
        Traverse the graph from a starting action, returning actions in order.
        
        :param start_action_id: The action ID to start from
        :param exclude_common_events: Whether to skip common events during traversal
        :return: List of action IDs in traversal order
        """
        visited = set()
        result = []
        
        def visit(action_id):
            if action_id in visited:
                return
            visited.add(action_id)
            
            if exclude_common_events and self.is_common_event(action_id):
                return
            
            result.append(action_id)
            
            for transition in self.get_next_transitions(action_id):
                target_id = transition["targetId"]
                visit(target_id)
        
        visit(start_action_id)
        return result
    
    def get_ordered_actions(self) -> List[str]:
        """
        Get all actions in topological order (starting actions first, following transitions).
        Common events are separated and placed at the end.
        
        :return: List of action IDs in logical order
        """
        ordered_actions = []
        visited = set()
        
        # Depth-first traversal from each starting action
        def visit(action_id):
            if action_id in visited:
                return
            visited.add(action_id)
            
            # Skip common events in the main flow
            if self.is_common_event(action_id):
                return
            
            ordered_actions.append(action_id)
            
            # Visit all next actions
            for transition in self.get_next_transitions(action_id):
                target_id = transition["targetId"]
                visit(target_id)
        
        # Start from all starting actions
        for start_id in self.get_starting_actions():
            visit(start_id)
        
        # Add any remaining actions not visited (common events and orphans)
        for action_id in self._graph.keys():
            if action_id not in visited:
                ordered_actions.append(action_id)
        
        return ordered_actions
    
    def to_dict(self) -> Dict:
        """
        Export the graph as a dictionary (for compatibility with old code).
        
        :return: Dictionary with graph, starting_actions, all_actions, incoming_refs
        """
        return {
            "graph": self._graph,
            "starting_actions": self.get_starting_actions(),
            "all_actions": self._actions,
            "incoming_refs": self._incoming_refs
        }
    
    def print_graph(self):
        """Print the transition graph in a readable format."""
        print_transition_graph(self.to_dict())
    
    def render_graph(self, figsize=(14, 10), save_path=None):
        """
        Render a visual representation of the transition graph.
        
        :param figsize: Figure size as (width, height) tuple
        :param save_path: Optional path to save the figure
        """
        return render_transition_graph(self.to_dict(), figsize=figsize, save_path=save_path)


def build_transition_graph(plan: PlanDefinition):
    """
    Build a graph of transitions based on soaTransition extensions.
    
    Returns a dictionary containing:
    - graph: dict mapping action.id -> list of target action.ids
    - starting_actions: list of action.ids with no incoming references
    - all_actions: dict mapping action.id -> action details
    
    :param plan: PlanDefinition resource
    :type plan: PlanDefinition
    :return: Dictionary with graph structure
    :rtype: dict
    """
    graph = {}  # action.id -> [target action.ids]
    all_actions = {}  # action.id -> action details
    incoming_refs = set()  # Track all action.ids that are referenced as targets
    
    # Process all actions and sub-actions
    for action in plan.action:
        action_id = action.id
        graph[action_id] = []
        all_actions[action_id] = {
            "id": action.id,
            "title": action.title,
            "description": action.description,
            "definition": action.definition_canonical,
            "type": "action"
        }
        
        # Process sub-actions to find soaTransition extensions
        if action.action:
            for sub_action in action.action:
                if sub_action.extension:
                    for ext in sub_action.extension:
                        _extension = unpack_extension(ext)
                        if _extension["type"] == "soaTransition":
                            target_id = _extension.get("soaTargetId")
                            if target_id:
                                condition_info = None
                                if sub_action.condition:
                                    condition_info = {
                                        "kind": sub_action.condition[0].kind if sub_action.condition else None,
                                        "expression": sub_action.condition[0].expression.expression if sub_action.condition and sub_action.condition[0].expression else None
                                    }
                                transition = {
                                    "targetId": target_id,
                                    "condition": condition_info
                                }
                                graph[action_id].append(transition)
                                incoming_refs.add(target_id)
    
    # Find starting actions (those with no incoming references)
    starting_actions = [action_id for action_id in graph.keys() 
                       if action_id not in incoming_refs]
    
    return {
        "graph": graph,
        "starting_actions": starting_actions,
        "all_actions": all_actions,
        "incoming_refs": incoming_refs
    }


def print_transition_graph(graph_data):
    """
    Pretty print the transition graph in logical order:
    - Start with nodes having no incoming references
    - Follow transitions in order (excluding common events)
    - Show common events (multiple incoming edges) at the bottom
    
    :param graph_data: Dictionary returned by build_transition_graph
    :type graph_data: dict
    """
    all_actions = graph_data["all_actions"]
    graph = graph_data["graph"]
    
    # Count incoming edges for each action
    incoming_count = {}
    for action_id in graph.keys():
        incoming_count[action_id] = 0
    
    for transitions in graph.values():
        for transition in transitions:
            target_id = transition["targetId"]
            if target_id in incoming_count:
                incoming_count[target_id] += 1
    
    # Identify common events (multiple incoming edges)
    common_events = {action_id for action_id, count in incoming_count.items() if count > 1}
    
    # Build ordered list using traversal from starting actions
    ordered_actions = []
    visited = set()
    
    def traverse(action_id):
        if action_id in visited:
            return
        visited.add(action_id)
        
        # Only add non-common events during traversal
        if action_id not in common_events:
            ordered_actions.append(action_id)
            
            # Follow transitions to non-common events
            if action_id in graph:
                for transition in graph[action_id]:
                    target_id = transition["targetId"]
                    if target_id not in common_events:
                        traverse(target_id)
    
    # Start traversal from starting actions
    for start_id in graph_data["starting_actions"]:
        traverse(start_id)
    
    # Add any remaining non-common, unvisited actions
    for action_id in graph.keys():
        if action_id not in visited and action_id not in common_events:
            ordered_actions.append(action_id)
    
    # Add common events at the end
    common_event_list = sorted(common_events)
    
    print("=== Transition Graph ===")
    print(f"\nStarting Actions (no incoming references):")
    for action_id in graph_data["starting_actions"]:
        action = all_actions[action_id]
        print(f"  - {action_id}: {action['title']}")
    
    print(f"\nTransitions (in logical order):")
    
    # Print ordered actions first
    for action_id in ordered_actions:
        action = all_actions[action_id]
        transitions = graph.get(action_id, [])
        print(f"  {action_id} ({action['title']}) ({action['definition'] or 'No definition'}):")
        if transitions:
            for transition in transitions:
                target_id = transition["targetId"]
                condition = transition["condition"]
                target = all_actions.get(target_id)
                target_title = target['title'] if target else "Unknown"
                target_def = target['definition'] if target else "Unknown"
                if condition:
                    condition_str = f" [condition-kind: {condition['kind']}]"
                    if condition['expression']:
                        condition_str += f" {condition['expression']}"
                else:
                    condition_str = ""
                print(f"    -> {target_id} ({target_def}) ({target_title}){condition_str}")
        else:
            print(f"    -> [No transitions]")
    
    # Print common events (multiple incoming edges)
    if common_event_list:
        print(f"\n  === Common Events (multiple incoming edges) ===")
        for action_id in common_event_list:
            action = all_actions[action_id]
            transitions = graph.get(action_id, [])
            incoming = incoming_count[action_id]
            print(f"  {action_id} ({action['title']}) ({action['definition'] or 'No definition'}) [incoming: {incoming}]:")
            if transitions:
                for transition in transitions:
                    target_id = transition["targetId"]
                    condition = transition["condition"]
                    target = all_actions.get(target_id)
                    target_title = target['title'] if target else "Unknown"
                    target_def = target['definition'] if target else "Unknown"
                    if condition:
                        condition_str = f" [condition-kind: {condition['kind']}]"
                        if condition['expression']:
                            condition_str += f" {condition['expression']}"
                    else:
                        condition_str = ""
                    print(f"    -> {target_id} ({target_def}) ({target_title}){condition_str}")
            else:
                print(f"    -> [No transitions]")
    
    print(f"\nGraph Statistics:")
    print(f"  Total Actions: {len(all_actions)}")
    print(f"  Starting Actions: {len(graph_data['starting_actions'])}")
    print(f"  Common Events: {len(common_event_list)}")
    print(f"  Actions with Transitions: {sum(1 for t in graph.values() if t)}")


def render_transition_graph(graph_data, figsize=(14, 10), save_path=None):
    """
    Render a force-directed graph visualization of the transition graph using matplotlib.
    
    :param graph_data: Dictionary returned by build_transition_graph or TransitionGraph.to_dict()
    :type graph_data: dict
    :param figsize: Figure size as (width, height) tuple
    :type figsize: tuple
    :param save_path: Optional path to save the figure
    :type save_path: str or None
    """
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError:
        print("Error: matplotlib and networkx are required for graph visualization.")
        print("Install with: pip install matplotlib networkx")
        return
    
    # Create directed graph
    G = nx.DiGraph()
    
    all_actions = graph_data["all_actions"]
    graph = graph_data["graph"]
    starting_actions = graph_data["starting_actions"]
    

    # Count incoming edges for each action
    incoming_count = {}
    for action_id in graph.keys():
        incoming_count[action_id] = 0
    
    for transitions in graph.values():
        for transition in transitions:
            target_id = transition["targetId"]
            if target_id in incoming_count:
                incoming_count[target_id] += 1
    
    # Add nodes
    for action_id, action_info in all_actions.items():
        G.add_node(action_id, 
                   title=action_info['title'], 
                   definition=action_info.get('definition', 'N/A'))
    
    # Add edges with labels
    edge_labels = {}
    for action_id, transitions in graph.items():
        for transition in transitions:
            target_id = transition["targetId"]
            G.add_edge(action_id, target_id)
            
            # Create edge label from condition
            condition = transition.get("condition")
            if condition and condition.get("expression"):
                label = f"{condition['kind'][:3]}"  # Shortened label
                edge_labels[(action_id, target_id)] = label
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Use spring layout for force-directed positioning
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Categorize nodes
    starting_nodes = [n for n in G.nodes() if n in starting_actions]
    common_event_nodes = [n for n in G.nodes() if incoming_count.get(n, 0) > 1]
    regular_nodes = [n for n in G.nodes() if n not in starting_nodes and n not in common_event_nodes]
    
    # Draw nodes with different colors
    nx.draw_networkx_nodes(G, pos, nodelist=starting_nodes, 
                          node_color='lightgreen', node_size=3000, 
                          node_shape='s', alpha=0.9, ax=ax, label='Starting Actions')
    
    nx.draw_networkx_nodes(G, pos, nodelist=common_event_nodes, 
                          node_color='orange', node_size=3000, 
                          node_shape='d', alpha=0.9, ax=ax, label='Common Events')
    
    nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes, 
                          node_color='lightblue', node_size=3000, 
                          alpha=0.9, ax=ax, label='Regular Actions')
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', 
                          arrows=True, arrowsize=20, 
                          arrowstyle='->', width=2, 
                          connectionstyle='arc3,rad=0.1', ax=ax)
    
    # Draw labels
    labels = {node: f"{node}\n{all_actions[node]['title'][:20]}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, 
                           font_weight='bold', ax=ax)
    
    # Draw edge labels if any
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels, 
                                     font_size=6, ax=ax)
    
    ax.set_title("Transition Graph Visualization", fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Graph saved to {save_path}")
    
    plt.show()
    
    return fig, ax


def unpack_extension(extension: Extension):
    """
    Turn the fhir4pharma extension into a Dictionary
    """
    assert extension.url in [
        "http://fhir4pharma.com/StructureDefinition/soaTransition",
        "http://fhir4pharma.com/StructureDefinition/soaPlannedTimepoint",
    ], f"Unknown extension URL: {extension.url}"
    struct = {}
    struct["type"] = extension.url.split("/")[-1]
    match extension.url:
        case "http://fhir4pharma.com/StructureDefinition/soaTransition":
            struct["type"] = extension.url.split("/")[-1]
            for ext in extension.extension:
                _key = ext.url
                if _key in ["soaTransitionDelay"]:
                    _value = dict(
                        value=ext.value_duration.value, 
                        unit=ext.value_duration.unit
                    )
                elif _key in ["soaTransitionRange"]:
                    _value = dict(
                        low=dict(
                            value=ext.value_range.low.value,
                            unit=ext.value_range.low.unit,
                        ),
                        high=dict(
                            value=ext.value_range.high.value,
                            unit=ext.value_range.high.unit,
                        ),
                    )
                else:
                    _value = ext.value_string
                struct[_key] = _value
        case "http://fhir4pharma.com/StructureDefinition/soaPlannedTimepoint":
            for ext in extension.extension:
                _key = ext.url
                match _key:
                    case "soaPlannedTimePoint":
                        _value = dict(
                            value=ext.value_quantity.value, unit=ext.value_quantity.unit
                        )
                    case "soaPlannedDuration":
                        _value = dict(
                            value=ext.value_duration.value, unit=ext.value_duration.unit
                        )
                    case "soaPlannedRange":
                        _value = dict(
                            low=dict(
                                value=ext.value_range.low.value,
                                unit=ext.value_range.low.unit,
                            ),
                            high=dict(
                                value=ext.value_range.high.value,
                                unit=ext.value_range.high.unit,
                            ),
                        )
                    case "soaRepeatAllowed":
                        _value = ext.value_boolean
                    case "soaRepeatInterval":
                        _value = dict(
                            value=ext.value_duration.value, unit=ext.value_duration.unit
                        )
                    case _:
                        _value = ext.value_string
                struct[_key] = _value
    return struct
