"""
Streamlit UI for browsing research subject activities and evaluations.

Run with: streamlit run src/tasks/ui.py
or from project root: poetry run streamlit run src/tasks/ui.py
"""

import streamlit as st
from typing import Dict, Any, Optional
import os
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Ensure .env is loaded before importing config
from dotenv import load_dotenv
load_dotenv()

# Now import from tasks
from tasks.config import Config
from tasks.evaluate import evaluate
from tasks.report import generate_research_subject_report, visualize_patient_journey
from tasks.common import TransitionGraph
from tasks.fhirsdk.client import Client, Auth, AuthCredentials
from tasks.fhirsdk import ResearchSubject, ResearchStudy


# Page configuration
st.set_page_config(
    page_title="Research Subject Activity Browser",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark mode compatible
st.markdown("""
<style>
    /* Use CSS variables that adapt to theme */
    :root {
        --success-color: #28a745;
        --warning-color: #ffc107;
        --info-color: #17a2b8;
    }
    
    /* Metrics - use semi-transparent backgrounds */
    .stMetric {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Decision box - adapts to theme */
    .decision-box {
        background-color: rgba(255, 193, 7, 0.2);
        border-left: 4px solid var(--warning-color);
        padding: 10px;
        margin: 10px 0;
    }
    
    /* Event colors - visible in both modes */
    .event-completed {
        color: #4caf50;
    }
    
    .event-active {
        color: #ff9800;
    }
    
    /* Cycle badge - good contrast in both modes */
    .cycle-badge {
        background-color: #2196f3;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        display: inline-block;
    }
    
    /* Expander styling for better visibility */
    .streamlit-expanderHeader {
        border-radius: 5px;
    }
    
    /* Make sure text in custom elements is visible */
    .decision-box, .event-completed, .event-active {
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_config() -> Config:
    """Load configuration from environment."""
    return Config()


@st.cache_data(ttl=60)
def get_research_subjects(config: Config) -> list:
    """Fetch list of research subjects."""
    try:
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
        
        # Search for research subjects
        result = client.search(ResearchSubject, {"_count": "100"})
        
        subjects = []
        if result and result.entry:
            for entry in result.entry:
                rs = entry.resource
                subjects.append({
                    "id": rs.id,
                    "patient_ref": rs.subject.reference if rs.subject else "Unknown",
                    "study_ref": rs.study.reference if rs.study else "Unknown",
                    "status": rs.status if hasattr(rs, 'status') else "Unknown"
                })
        
        return subjects
    except Exception as e:
        st.error(f"Error fetching research subjects: {str(e)}")
        return []


def display_evaluation_summary(eval_result: Dict[str, Any]):
    """Display evaluation summary metrics."""
    st.subheader("📊 Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_events = len(eval_result.get("events", []))
        st.metric("Total Events", total_events)
    
    with col2:
        completed = len([e for e in eval_result.get("events", []) if e.get("status") == "completed"])
        st.metric("Completed", completed, delta=None)
    
    with col3:
        active = len([e for e in eval_result.get("events", []) if e.get("status") == "active"])
        st.metric("Active", active, delta=None)
    
    with col4:
        available = len(eval_result.get("available_actions", []))
        st.metric("Available Actions", available)


def display_events(eval_result: Dict[str, Any], graph: TransitionGraph):
    """Display completed and active events."""
    st.subheader("📅 Patient Events")
    
    events = eval_result.get("events", [])
    if not events:
        st.info("No events recorded yet.")
        return
    
    # Create tabs for completed and active
    tab1, tab2 = st.tabs(["✅ Completed Events", "🔄 Active Events"])
    
    with tab1:
        completed_events = [e for e in events if e.get("status") == "completed"]
        if completed_events:
            for event in completed_events:
                action_id = event.get("action_id")
                details = graph.get_action_details(action_id)
                repeat_num = event.get("repeat_number", 1)
                
                with st.expander(f"✓ {details.get('title', action_id)}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Action ID:** `{action_id}`")
                        st.write(f"**CarePlan:** `{event.get('care_plan_id')}`")
                        date_str = event.get("date")
                        if date_str:
                            st.write(f"**Date:** {date_str}")
                        
                        if graph.is_repeatable(action_id) or repeat_num > 1:
                            st.markdown(f"**Cycle:** <span class='cycle-badge'>C{repeat_num}</span>", unsafe_allow_html=True)
                    
                    with col2:
                        st.write(f"**Status:** `{event.get('status')}`")
        else:
            st.info("No completed events.")
    
    with tab2:
        active_events = [e for e in events if e.get("status") == "active"]
        if active_events:
            for event in active_events:
                action_id = event.get("action_id")
                details = graph.get_action_details(action_id)
                repeat_num = event.get("repeat_number", 1)
                
                with st.expander(f"→ {details.get('title', action_id)}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Action ID:** `{action_id}`")
                        st.write(f"**CarePlan:** `{event.get('care_plan_id')}`")
                        date_str = event.get("date")
                        if date_str:
                            st.write(f"**Date:** {date_str}")
                        
                        if graph.is_repeatable(action_id) or repeat_num > 1:
                            st.markdown(f"**Cycle:** <span class='cycle-badge'>C{repeat_num}</span>", unsafe_allow_html=True)
                    
                    with col2:
                        st.write(f"**Status:** `{event.get('status')}`")
        else:
            st.info("No active events.")


def display_available_actions(eval_result: Dict[str, Any], graph: TransitionGraph):
    """Display available next actions."""
    st.subheader("🎯 Available Next Actions")
    
    available = eval_result.get("available_actions", [])
    recommended = eval_result.get("next_recommended_actions", [])
    
    if not available:
        st.info("No available actions at this time.")
        return
    
    # Create tabs for recommended and all available
    tab1, tab2 = st.tabs(["⭐ Recommended", "📋 All Available"])
    
    with tab1:
        if recommended:
            for action_info in recommended:
                action_id = action_info.get("action_id")
                details = graph.get_action_details(action_id)
                event_count = action_info.get("event_count", 0)
                is_cycle = action_info.get("is_cycle", False)
                
                cycle_label = f" (Cycle #{event_count + 1})" if is_cycle else ""
                
                with st.expander(f"⭐ {details.get('title', action_id)}{cycle_label}", expanded=True):
                    st.write(f"**Action ID:** `{action_id}`")
                    
                    plan_def_id = details.get('definition', '').split('/')[-1]
                    st.write(f"**PlanDefinition:** `{plan_def_id}`")
                    
                    if event_count > 0:
                        st.info(f"This action has been performed {event_count} time(s) previously.")
                    
                    if action_info.get("condition"):
                        condition = action_info["condition"]
                        st.markdown(f"**Condition:** [{condition['kind']}] {condition.get('expression', 'no expression')}")
                    
                    if action_info.get("from_last_activity"):
                        st.success("← Follows from last completed activity")
        else:
            st.info("No recommended actions. See 'All Available' tab for other options.")
    
    with tab2:
        for action_info in available:
            action_id = action_info.get("action_id")
            details = graph.get_action_details(action_id)
            event_count = action_info.get("event_count", 0)
            is_cycle = action_info.get("is_cycle", False)
            is_common = graph.is_common_event(action_id)
            
            cycle_label = f" (Cycle #{event_count + 1})" if is_cycle else ""
            common_label = " (Common Event)" if is_common else ""
            
            with st.expander(f"• {details.get('title', action_id)}{cycle_label}{common_label}"):
                st.write(f"**Action ID:** `{action_id}`")
                
                plan_def_id = details.get('definition', '').split('/')[-1]
                st.write(f"**PlanDefinition:** `{plan_def_id}`")
                
                if event_count > 0:
                    st.info(f"Previously performed: {event_count} time(s)")
                
                if action_info.get("condition"):
                    condition = action_info["condition"]
                    st.markdown(f"**Condition:** [{condition['kind']}] {condition.get('expression', 'no expression')}")


def display_visualization(research_subject_id: str, config: Config):
    """Display patient journey visualization."""
    st.subheader("🗺️ Patient Journey Visualization")
    
    try:
        with st.spinner("Generating visualization..."):
            report = generate_research_subject_report(research_subject_id, config)
            
            # Generate visualization to a temporary file
            import tempfile
            temp_dir = tempfile.gettempdir()
            viz_path = Path(temp_dir) / f"patient_journey_{research_subject_id}"
            
            full_path = visualize_patient_journey(
                report,
                output_path=str(viz_path),
                view=False
            )
            
            if full_path and os.path.exists(full_path):
                st.image(full_path, use_container_width=True)
            else:
                st.error("Could not generate visualization.")
    
    except Exception as e:
        st.error(f"Error generating visualization: {str(e)}")


def main():
    """Main UI application."""
    st.title("🔬 Research Subject Activity Browser")
    st.markdown("Browse and analyze research subject activities and protocol evaluations.")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Load config
        try:
            config = load_config()
            st.success("✓ Configuration loaded")
            st.text(f"Endpoint: {config.endpoint_url}")
            st.text(f"Username: {config.fhir_username}")
        except ValueError as e:
            st.error(f"❌ Configuration Error")
            st.error(str(e))
            
            # Show helpful information
            st.markdown("---")
            st.markdown("### Configuration Setup")
            
            # Find .env file location
            env_path = Path.cwd() / ".env"
            example_env = Path.cwd() / "example.env"
            
            if env_path.exists():
                st.info(f"✓ Found .env file at: `{env_path}`")
            else:
                st.warning(f"⚠️ No .env file found at: `{env_path}`")
                if example_env.exists():
                    st.info(f"Copy `example.env` to `.env` and fill in your values")
            
            st.markdown("""
            **Required environment variables:**
            - `ENDPOINT_URL` or `FHIR_ENDPOINT_URL`
            - `FHIR_USERNAME`
            - `FHIR_PASSWORD`
            
            **Example .env file:**
            ```
            ENDPOINT_URL=https://your-fhir-server.com/fhir
            FHIR_USERNAME=your-username
            FHIR_PASSWORD=your-password
            ```
            """)
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            st.exception(e)
            st.stop()
        
        st.markdown("---")
        
        # Research subject selection
        st.header("Select Research Subject")
        
        # Option 1: Select from list
        with st.expander("Browse Research Subjects", expanded=True):
            if st.button("🔄 Refresh List"):
                st.cache_data.clear()
            
            subjects = get_research_subjects(config)
            
            if subjects:
                # Group subjects by study
                subjects_by_study = {}
                for s in subjects:
                    study_id = s['study_ref'].split('/')[-1] if s['study_ref'] != "Unknown" else "Unknown Study"
                    if study_id not in subjects_by_study:
                        subjects_by_study[study_id] = []
                    subjects_by_study[study_id].append(s)
                
                # Create study selection dropdown
                study_ids = list(subjects_by_study.keys())
                
                if len(study_ids) > 1:
                    selected_study = st.selectbox(
                        "Filter by Research Study:",
                        options=["All Studies"] + study_ids,
                        index=0
                    )
                else:
                    selected_study = "All Studies"
                    if study_ids:
                        st.info(f"Study: {study_ids[0]}")
                
                # Filter subjects based on selected study
                if selected_study == "All Studies":
                    display_subjects = subjects
                else:
                    display_subjects = subjects_by_study[selected_study]
                
                # Create subject dropdown with grouped display
                if selected_study == "All Studies":
                    # Group format: Study ID | Subject ID (Patient Ref)
                    subject_options = {
                        f"{s['study_ref'].split('/')[-1]} | {s['id']} ({s['patient_ref']})": s['id']
                        for s in display_subjects
                    }
                else:
                    # Simple format when filtered by study
                    subject_options = {
                        f"{s['id']} ({s['patient_ref']})": s['id']
                        for s in display_subjects
                    }
                
                selected_display = st.selectbox(
                    f"Select a research subject ({len(display_subjects)} available):",
                    options=list(subject_options.keys())
                )
                
                selected_id = subject_options.get(selected_display)
            else:
                st.warning("No research subjects found or unable to fetch list.")
                selected_id = None
        
        # Option 2: Manual entry
        with st.expander("Manual Entry"):
            manual_id = st.text_input("Enter Research Subject ID:")
            if manual_id:
                selected_id = manual_id
        
        st.markdown("---")
        
        # Display options
        st.header("Display Options")
        show_visualization = st.checkbox("Show Visualization", value=True)
        auto_refresh = st.checkbox("Auto-refresh (60s)", value=False)
    
    # Main content area
    if not selected_id:
        st.info("👈 Please select or enter a Research Subject ID from the sidebar.")
        return
    
    # Display selected research subject
    st.header(f"Research Subject: `{selected_id}`")
    
    try:
        # Run evaluation
        with st.spinner("Evaluating research subject..."):
            eval_result = evaluate(selected_id, config)
        
        # Get the transition graph for additional info
        from tasks.fhirsdk import PlanDefinition
        
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
        
        research_subject = client.read(ResearchSubject, selected_id)
        study = client.read(ResearchStudy, research_subject.study.reference.split("/")[-1])
        protocol = study.protocol[0]
        parent_plan = client.read(PlanDefinition, protocol.reference.split("/")[-1])
        graph = TransitionGraph(parent_plan, client)
        
        # Display patient and study info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Patient ID", eval_result.get("patient_id", "N/A"))
        with col2:
            study_id = eval_result.get("study_id", "N/A").split("/")[-1]
            st.metric("Study ID", study_id)
        with col3:
            st.metric("Protocol", parent_plan.title if parent_plan.title else parent_plan.id)
        
        st.markdown("---")
        
        # Display evaluation summary
        display_evaluation_summary(eval_result)
        
        st.markdown("---")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📅 Events", "🎯 Available Actions", "📊 Raw Data"])
        
        with tab1:
            display_events(eval_result, graph)
        
        with tab2:
            display_available_actions(eval_result, graph)
        
        with tab3:
            st.subheader("Raw Evaluation Result")
            st.json(eval_result)
        
        # Visualization section
        if show_visualization:
            st.markdown("---")
            display_visualization(selected_id, config)
        
        # Auto-refresh
        if auto_refresh:
            import time
            time.sleep(60)
            st.rerun()
    
    except Exception as e:
        st.error(f"Error evaluating research subject: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
