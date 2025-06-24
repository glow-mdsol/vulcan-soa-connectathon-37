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
  * id = "informed-consent"
  * definitionUri = "ActivityDefinition/Eligbility"
* action[+]
  * id = "phys-exam"
  * definitionUri = "ActivityDefinition/PhysicalExam"
* action[+]
  * id = "vital-signs"
  * definitionUri = "ActivityDefinition/VitalSigns"
* action[+]
  * id = "performance-status"
  * definitionUri = "ActivityDefinition/PerformanceStatus"


Instance: SoA-PoC-Screening-Period-Plan-Definition-Late
InstanceOf: PlannedStudyVisitSoa
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities PoC - Screening Period (Day -14 to Day -1)"
* type = http://terminology.hl7.org/CodeSystem/plan-definition-type#clinical
* action[+]
  * id = "phys-exam"
  * definitionUri = "ActivityDefinition/PhysicalExam"
* action[+]
  * id = "vital-signs"
  * definitionUri = "ActivityDefinition/VitalSigns"
* action[+]
  * id = "performance-status"
  * definitionUri = "ActivityDefinition/PerformanceStatus"
* action[+]
  * id = "labs-chemistry"
  * definitionUri = "ActivityDefinition/LabsChemistry"
* action[+]
  * id = "labs-hematology"
  * definitionUri = "ActivityDefinition/LabsHematology"
* action[+]
  * id = "labs-coagulation"
  * definitionUri = "ActivityDefinition/LabsCoagulation"


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
