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
  * id = "SoA-PoC-EOT-Plan-Definition-S1"
  * title = "End of Treatment"
  * description = "End of treatment"
  * condition[+]
    * kind = #applicability
    * expression.language = #text/fhirpath
    * expression.expression = "%patient.Observation.where(code.coding.where(code='disease-progression').exists()).exists()"
  * definitionCanonical = "PlanDefinition/EndOfTreatment"
* action[+]
  * id = "SoA-PoC-Follow-Up-30-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp60-Plan-Definition"
  * relatedAction[+]
    * targetId = "SoA-PoC-EOT-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 30 'd'
    * extension[acceptableOffsetRange].valueRange.low = 23 'd'
    * extension[acceptableOffsetRange].valueRange.high = 37 'd'
* action[+]
  * id = "SoA-PoC-Follow-Up-60-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp30-Plan-Definition"
  * relatedAction[+]
    * targetId = "SoA-PoC-EOT-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 60 'd'
    * extension[acceptableOffsetRange].valueRange.low = 53 'd'
    * extension[acceptableOffsetRange].valueRange.high = 67 'd'
* action[+]
  * id = "SoA-PoC-Follow-Up-90-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp90-Plan-Definition"
  * relatedAction[+]
    * targetId = "SoA-PoC-EOT-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 90 'd'
    * extension[acceptableOffsetRange].valueRange.low = 83 'd'
    * extension[acceptableOffsetRange].valueRange.high = 97 'd'
* action[+]
  * id = "SoA-PoC-Follow-Up-Recurring-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-Survival-FollowUpRecurring-Plan-Definition"
  * relatedAction[+]
    * targetId = "SoA-PoC-Follow-Up-90-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 90 'd'
    * extension[acceptableOffsetRange].valueRange.low = 83 'd'
    * extension[acceptableOffsetRange].valueRange.high = 97 'd'
  * timingTiming.repeat
    * period = 90
    * periodUnit = #d
* action[+]
  * id = "SoA-PoC-End-Of-Study-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-End-Of-Study-Participation-Plan-Definition"
