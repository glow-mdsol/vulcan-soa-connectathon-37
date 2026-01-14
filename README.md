# Vulcan SoA Connectathon - Jan 2026

## Roles
System roles:

* Study Designer
* Site Coordinator
* Patient Participant in Clinical Trial


NOTE: There are three scenarios for testing, some of these will interleave and it will depend on the number of testers


## Scenarios

### Execute Linear Patient Path

Action:
* Enrol a Patient and progress through study based on protocol 

Precondition:
* Study Design for linear progression available

Success Criteria: 
[ ] Patient can be successfully enrolled
[ ] Patient can progress from V1 - V10 as scheduled (restricted to just scheduling Encounters)


Bonus point:
* Scheduled Activities added 

## Execute Branched Patient Path

Action:
* Enrol a Patient and progress through study based on protocol 
* Use decision point (eg Arm assignment) to drive patient down one of two paths

Precondition:
* Study Design for branched progression available

Success Criteria: 
[ ] Patient can be successfully enrolled
[ ] Patient can progress through screening
[ ] Patient can be randomized to an Arm
[ ] Patient can progress via the arm they are assigned in
[ ] Patient can complete the study

Bonus point:
[ ] Scheduled Activities added 

## Execute Cycle based Patient Progression

Action:
* Enrol a Patient 
* Complete Screening Assessments
* Complete Randomisation
* Enrol and complete Cycle 1
* Enrol and complete Cycle N
* Attribute Disease progression and either:
  * Enrol and complete Cycle N
  * Early Terminate
* Patient Terminates or Completes Successfully

Precondition:
* Study Design for simple Cycle Progression

Success Criteria: 
[ ] Patient can be successfully enrolled/screened and randomised
[ ] Patient can be attributed with disease progression status
[ ] Decision support available for system to present options for next cycle


Bonus point:
[ ] Scheduled Activities added 


# Tooling

## Web UI

A Streamlit-based web interface is available for browsing and analyzing research subject activities:

**Launch the UI:**
```bash
./run_ui.sh
# or
poetry run streamlit run src/tasks/ui.py
```

The UI provides:
- 📊 **Dashboard**: Summary metrics and patient information
- 📅 **Events Timeline**: Completed and active events with cycle tracking
- 🎯 **Available Actions**: Recommended next steps and all possible actions
- 🗺️ **Journey Visualization**: Interactive graph of patient progression
- 🔍 **Browse Subjects**: Select from all research subjects on the server

See [UI_README.md](UI_README.md) for detailed documentation.

## Command Line Tools

The API uses python, to set this up do the following:
* Install Python [Installing Python](https://www.python.org/downloads/)
* Install Poetry [Installing Poetry](https://python-poetry.org/docs/)
* Use a virtual env (recommended)
  ```
  $ poetry env activate
  ```
* Install the project 
  ```
  $ poetry install
  ```
* Add the configuration by copying the `example.env` to `.env` and inserting the correct values



