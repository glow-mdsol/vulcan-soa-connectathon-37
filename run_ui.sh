#!/bin/bash
# Launcher script for the Research Subject Activity Browser UI

echo "🔬 Starting Research Subject Activity Browser..."
echo ""
echo "The UI will open in your default browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Set PYTHONPATH to include src directory so imports work correctly
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Run streamlit with the UI script
poetry run streamlit run src/tasks/ui.py
