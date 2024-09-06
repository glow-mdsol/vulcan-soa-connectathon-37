# Vulcan SoA Connectathon 37

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



