Instance: SoA-PoC-DynamicProtocol-ScenarioTwo-ProtocolDesign
InstanceOf: PlannedStudyVisitSoa
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities PoC - Study Plan (Scenario 2)"
* type = http://terminology.hl7.org/CodeSystem/plan-definition-type#clinical
* action[+]
  * id = "SoA-PoC-Screening-Period-Plan-Definition-Early-S2"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Screening-Period-Plan-Definition-Early"
* action[+]
  * id = "SoA-PoC-Screening-Period-Plan-Definition-Late-S2"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Screening-Period-Plan-Definition-Late"
// Study Plan

* action[+]
  * id = "SoA-PoC-Follow-Up-60-Plan-Definition-S3"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp60-Plan-Definition"
* action[+]
  * id = "SoA-PoC-Follow-Up-90-Plan-Definition-S3"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp90-Plan-Definition"
* action[+]
  * id = "SoA-PoC-Follow-Up-Recurring-Plan-Definition-S3"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-Survival-FollowUpRecurring-Plan-Definition"
* action[+]
  * id = "SoA-PoC-End-Of-Study-Plan-Definition-S3"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-End-Of-Study-Participation-Plan-Definition"
