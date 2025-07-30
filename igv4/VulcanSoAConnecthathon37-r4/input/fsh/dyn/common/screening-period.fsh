Instance: SoA-PoC-Screening-Period-Plan-Definition-Early
InstanceOf: PlannedStudyVisitSoa
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities PoC - Screening Period (Day -28 to Day -15)"
* type = http://terminology.hl7.org/CodeSystem/plan-definition-type#clinical
* action[+]
  * id = "informed-consent"
  * definitionUri = "ActivityDefinition/InformedConsent"
* action[+]
  * id = "eligibility"
  * definitionUri = "ActivityDefinition/Eligbility"
* action[+]
  * id = "phys-exam"
  * definitionUri = "ActivityDefinition/PhysicalExam"
* action[+]
  * id = "vital-signs"
  * definitionUri = "ActivityDefinition/SoA-PoC-Vital-Signs-Screening-Activity-Definition"
* action[+]
  * id = "performance-status"
  * definitionUri = "ActivityDefinition/PerformanceStatus"
* action[+]
  * id = "imaging-ct"
  * definitionUri = "ActivityDefinition/CTAssessment-Liver-ActivityDefinition"
* action[+]
  * id = "imaging-mri"
  * definitionUri = "ActivityDefinition/MRIAssessment-Liver-ActivityDefinition"
// TODO: Exploratory Biomarkers

Instance: SoA-PoC-Screening-Period-Plan-Definition-Late
InstanceOf: PlannedStudyVisitSoa
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities PoC - Screening Period (Day -14 to Day -1) (activities required to be done within 7 days of Day 1)"
* type = http://terminology.hl7.org/CodeSystem/plan-definition-type#clinical
* action[+]
  * id = "phys-exam"
  * definitionUri = "ActivityDefinition/PhysicalExam"
* action[+]
  * id = "pregnancy-test"
  * definitionCanonical = "ActivityDefinition/PregnancyTest-ActivityDefinition"
  * title = "Pregnancy Test"
  * condition[+]
    * kind = #applicability
    * expression
      * description = "Pregnancy test for Biological Females"
      * language = #text/fhirpath
      * expression = "Patient.gender='female'"
  * condition[+]
    * kind = #applicability
    * expression
      * description = "Evaluation of Fertility"
      * language = #text/fhirpath
      // 118183008 | Finding of fertility (finding) |
      // 8619003 | Infertile (finding) |
      * expression = "Observation.where(subject.reference = 'Patient/' + Id).where(code.coding.system = 'http://snomed.info/sct' and code.coding.code = '118183008').valueCodeableConcept!='http://snomed.info/sct|8619003'"
* action[+]
  * id = "labs-chemistry"
  * definitionUri = "ActivityDefinition/LabsChemistry"
* action[+]
  * id = "labs-hematology"
  * definitionUri = "ActivityDefinition/LabsHematology"
* action[+]
  * id = "labs-coagulation"
  * definitionUri = "ActivityDefinition/LabsCoagulation"
* action[+]
  * id = "blood-typing-interference-test"
  * definitionUri = "ActivityDefinition/Blood-Typing-Interference-Test-ActivityDefinition"
  * title = "Blood Typing Interference Test"
* action[+]
  * id = "labs-urinalysis"
  * definitionUri = "ActivityDefinition/Urinalysis-ActivityDefinition"


// Instance: ScreeningD28D15
// InstanceOf: StudyVisitSoa
// Usage: #example
// Title: "Screening (up to 28 days before Day 1) - Day -28 to Day -15"
// Description: "Initial Screening"
// * title = "D -28 to D -15"

// Instance: ScreeningD14D1
// InstanceOf: StudyVisitSoa
// Usage: #example
// Title: "Screening (up to 28 days before Day 1) - Day -14 to Day -1"
// Description: "Initial Screening"
// * title = "D-14 to D-1"
