# Vulcan SoA Connectathon - June 2025

There are three scenarios under investigation:

## Conditional Activities

*Synopsis:* 
In the conduct of a clinical Study, some patients may have a different set of activities based on their characteristics, sponsor decisions or emergent factors

**Conditional Activities - Scenario 1**
Using a Planned Activity, add a applicability test for doing a pregnancy test for biological females.
* It should take account of Sex.
* It should take account of Child-bearing potential, such as surgical sterilisation, prophylactic treatments

**Conditional Activities - Scenario 2**
Using a Planned activity, add an applicability test for doing a HbA1C test for patients with Diabetes
* It should take into account Medical History
* It should allow for distinction between Type I and Type II DM

*Success Criteria:*  
Using API and sample Patients evaluate whether an activity is applicable, and complete if so

*Bonus point:*

## Repeating Planned Sets of Activities (Cycles)

*Synopsis:* 
In many of the more complex (Oncology) studies, treatment cycles are utilised to allow patients to continue to receive IP until some stopping criteria.  Examples of stopping condition could be related to disease (eg Progressive Disease), design (eg max number of cycles before moving to long term follow-up) or emergent conditions (eg sponsor decision).   In addition, within the frame of repeating cycles some cohorts may have conditional activities based on patient characteristics (eg basket studies).  Note, we are not focusing on activities, so an indicative visit will suffice.  There is a need to update the ResearchSubject.subjectState (assuming R6).  You will be provided with a sample SoA for the cycles.


**Oncology Cycles - Scenario 1**
Define a Plan for 10 Cycles, with Encounters Day 1, Day 8 and Day 15 with no nesting, and no cycle dependencies (each treatment is the same); use an applicability filter based on ResearchSubject.subjectState to gate access to latter cycles and end of treatment.  Use inter-encounter for timing
* Test a Patient, with 3 cycles completed, change ResearchSubject.subjectState and confirm that latter cycles are not scheduled (apart from EOT)

**Oncology Cycles - Scenario 2**
Define a Plan for 10 Cycles, with Encounters Day 1, Day 8 and Day 15 with a PlanDefinition for each of the cycles, and no cycle dependences (each treatment is the same); use an applicability filter based on ResearchSubject.subjectState to gate access to latter cycles and end of treatment.
* Test a Patient, with 3 cycles completed, change ResearchSubject.subjectState and confirm that latter cycles are not scheduled (apart from EOT)
* use timing within the cycle and between the cycles

**Oncology Cycles - Scenario 3**

Define a Plan for 10 Cycles, with Encounters Day 1, Day 8 and Day 15 with a PlanDefinition for each of the cycles, and no cycle dependences (each treatment is the same).  Use a repeated timing for the encounter timing.  Use an applicability filter based on ResearchSubject.subjectState to gate access to latter cycles and end of treatment.
* Test a Patient, with 3 cycles completed (repeat 3 times), change ResearchSubject.subjectState and confirm that latter cycles are not scheduled (apart from EOT)
* use timing within the cycle and between the cycles

*Success Criteria:*  
* In each scenario illustrate the stopping condition after cycle 3
* Evaluate the timing outcomes compared to the provided SoA

*Bonus point*

## Unscheduled Activities

*Synopsis:* 
Up until to now the Study Design has been limited to pure 'happy path' implementation; where each subject has a single path through the study. More practically it is known that there can actually be variations in what datapoints are expected for a study participant as part of the activities

**Unscheduled Activities - Scenario 1**
Implement an unscheduled PlanDefinition for a set of Unscheduled Activities as an encounter that can be referred to in the SoA​
* Add an encounter based on the unscheduled PlanDefinition (PD->CP->SR->EN)​
* Annotate the PlanDefinition as an Unscheduled Encounter​
* Identify the set of activities/outcomes based on the Unscheduled Activity

**Unscheduled Activities - Scenario 2:**
Describe the activity of Early Termination (as a Narrative)
* ​Let the Provider suggest how they would implement episodic sets of activities that should be available to add based on triggered need

Notes:
* PlanDefinitions can be apply'ed multiple times; this would reflect the current state of the data at the time of the action.  Use of Questionnaire is preferred to modify workflow.  Interactive feedback, will update the state of the precondition to the apply activities.  Use the QuestionnaireResponse and $extract to update the data state
* Need to define the Period over which the conditions would occur, this requires input from the User
* Pre-conditions
  * ResearchStudy
    * PlanDefintion - for each of the planned encounters
    * ActivityDefinition - for each of the activities to be done as and when 
* Activities:
  * Screen a Patient according to eligibility 
  * Initiate the Patient in the ResearchStudy
    * Action to create EarlyScreening
    * Complete activities - need to know when the activities are complicated 
    * Action to create LateScreening 
    * Complete activities

### Reference Materials
* https://www.youtube.com/watch?v=4qF6FNn79o8&list=PLKuZNI94tzWaDuupQSXGfLEYWpel_aj7y&index=110
  * https://www.devdays.com/wp-content/uploads/2024/07/6.12.24-Taylor-Le-InteractiveCDS-Taylor-Le.pdf
* https://build.fhir.org/clinicalreasoning-cds-on-fhir.html
  * recommendation as a card
* $apply implementation - https://github.com/cqframework/clinical-reasoning/tree/master/cqf-fhir-cr/src/main/java/org/opencds/cqf/fhir/cr/plandefinition
  * QuestionnaireResponse
* Profiles for CaseFeatures [Examples](https://build.fhir.org/ig/HL7/cqf-recommendations/examples.html#profile-index)
  * Relevant for workflow

Recommendation
* extension to define the next step


## Vulcan SoA Connectathon 37

## Plan

* Create a SoA using the Vulcan SoA IG and use the Structured Data Capture (SDC) profile on an EMR to populate Questionnaires
* Extract the data from the Questionnaires and push into CTMS or proxy system

### System roles:

|Role|Description|
|----|-----------|
| Creator | Creating SoA and Activity specifications and all dependent resources (eg Questionnaire, ResearchStudy) |
| Form Filler | (EHR supporting the SDC profile) - presenting forms and permitting entering data in presented forms in EHR |
| Reviewer | Reviewing data entered |
| Integrator | extracting QuestionnaireResponse resources for incorporation in CTMS|


## Scenarios

### Create an SoA for a Study

*Prerequisites*
Creator - Create a Simple SoA for a study
*Actions:*
* Create a Simple SoA for a Study consisting of:
  * One screening visit, One Baseline Visit, 4 treatment visits and one end of study (EoS) visit
  * One PHQ15 form per visit
  * One Vital Signs Panel in Screening, Baseline and EoS
  * (Optional) - Create an ActivityDefinition for the VS activity
* Create a Bundle of the Study Design (representation of the SoA)
* Load into EHR System

Precondition: Success Criteria: 

#### Success Criteria:  
* ResearchStudy created
* PlanDefinition for Visits created and linked to ResearchStudy
* PHQ15 Questionnaire resources created and linked to all PlanDefinition
* Vital Signs Questionnaire

##### Bonus point:

#### TestScript(s):
* FHIR queries (eg get Research Study by Id, etc )

### Form Filling 
Form Filler - Use the Planned Resources above to undertake the 

*Action:*
* Create a ResearchSubject Resource (based on ResearchStudy)
* Create an Encounter Resource for each Planned Encounter
* Access Questionnaires for each visit
* Complete Questionnaires 
  * Manual entry
  * Auto-population (if possible)
* Export QuestionResponse resources

#### Success Criteria
* ResearchSubject created
* Questionnaires available to enter
* Data entered
* Exportable resources

#### TestScript(s):
* FHIR queries (eg get Research Subject by Study, etc )



