Instance: SoA-PoC-DynamicProtocol-ScenarioOne-ProtocolDesign
InstanceOf: PlannedStudyVisitSoa
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities PoC - Study Plan (Scenario 1)"
* type = http://terminology.hl7.org/CodeSystem/plan-definition-type#clinical
* action[+]
  * title = "Screening (D-28 to D-14)"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Screening-Period-Plan-Definition-Early"
  * relatedAction[+]
    * actionId = "SoA-PoC-Cycle1Day1-Plan-Definition-S1"
    * relationship = #before
    * offsetRange
      * low = 14 'd'
      * high = 28 'd'
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "ResearchSubject.where(individual = 'Patient/' + Id and study.reference == 'ResearchStudy/456' and status == 'http://hl7.org/fhir/ValueSet/research-subject-status#screening').exists()"
* action[+]
  * title = "Screening (D-14 to D-1)"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Screening-Period-Plan-Definition-Late"
  * condition[+]
    * kind = #start
    * expression
      * language = #text/fhirpath
      * expression = "ServiceRequest()"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "ResearchSubject.where(individual = 'Patient/' + Id).where(status = 'http://hl7.org/fhir/ValueSet/research-subject-status#screening').exists()"
  * relatedAction[+]
    * actionId = "SoA-PoC-Cycle1Day1-Plan-Definition-S1"
    * relationship = #before
    * offsetRange
      * low = 1 'd'
      * high = 14 'd'
* action[+]
  * id = "SoA-PoC-Cycle1Day1-Plan-Definition-S1"
  * title = "Cycle 1 Day 1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Cycle1Day1-Plan-Definition"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "ResearchSubject.where(individual = 'Patient/' + Id).where(status = 'http://hl7.org/fhir/ValueSet/research-subject-status#randomized').exists()"
* action[+]
  * title = "Disease Assessments"
  * definitionCanonical = "PlanDefinition/Disease-Assessments"
  * relatedAction[+]
    * actionId = "SoA-PoC-Cycle1Day1-Plan-Definition-S1"
    * relationship = #concurrent-with-start
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "ResearchSubject.where(individual = 'Patient/' + Id).where(status = 'http://hl7.org/fhir/ValueSet/research-subject-status#randomized').exists()"
* action[+]
  * id = "SoA-PoC-Cycle1Day8-Plan-Definition-S1"
  * title = "Cycle 1 Day 8"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Cycle1Day1-Plan-Definition"
  * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/Exit]
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/destinations]
      * actionId = "SoA-PoC-EndOfTreatment-Plan-Definition-S1"
      * basedOn[+]
        * expression = "DiagnosticReport.where(subject = 'Patient/' + Id).where(conclusion = 'RECIST Progressive Disease').exists()"
  * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/NextSteps][+]
    * actionId = "SoA-PoC-Cycle1Day15-Plan-Definition-S1"
    * basedOn[+]
      * expression = "DiagnosticReport.where(subject = 'Patient/' + Id).where(conclusion = 'RECIST Progressive Disease').exists()"
  * relatedAction[+]
    * actionId = "SoA-PoC-Cycle1Day1-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 7 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.low = 6 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.high = 9 'd'
* action[+]
  * id = "SoA-PoC-Cycle1Day15-Plan-Definition-S1"
  * title = "Cycle 1 Day 15"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Cycle1Day1-Plan-Definition"
  * relatedAction[+]
    * actionId = "SoA-PoC-Cycle1Day8-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 7 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.low = 6 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.high = 9 'd'
* action[+]
  * title = "TreatmentCycles-Cycle2-Plus"
  * definitionCanonical = "PlanDefinition/TreatmentCycles-Cycle2-Plus-PlanDefinition"
  // Need to create a request to initiate another instance of this in 21 days (via a Task, or CommunicationRequest)
  //  eg by a 
  * timingTiming
    * repeat
      * period = 21
      * periodUnit = #d
  * condition[+]
    * kind = #stop
    * expression
      * language = #text/fhirpath
      * expression = "DiagnosticReport.where(subject = 'Patient/' + Id).where(conclusion = 'RECIST Progressive Disease').exists()"
// TODO: Identify how to stop a repeating action
* action[+]
  * id = "SoA-PoC-EOT-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-EndOfTreatment-Plan-Definition"
  * title = "End of Treatment"
  * description = "End of treatment"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "ResearchSubject.where(individual = 'Patient/' + Id).where(status = 'http://hl7.org/fhir/ValueSet/research-subject-status#off-study').exists()"
  * extensions[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa]
* action[+]
  * id = "SoA-PoC-Follow-Up-30-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp60-Plan-Definition"
  * relatedAction[+]
    * actionId = "SoA-PoC-EOT-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 30 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.low = 23 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.high = 37 'd'
* action[+]
  * id = "SoA-PoC-Follow-Up-60-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp30-Plan-Definition"
  * relatedAction[+]
    * actionId = "SoA-PoC-EOT-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 60 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.low = 53 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.high = 67 'd'
* action[+]
  * id = "SoA-PoC-Follow-Up-90-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-FollowUp90-Plan-Definition"
  * relatedAction[+]
    * actionId = "SoA-PoC-EOT-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 90 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.low = 83 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.high = 97 'd'
* action[+]
  * id = "SoA-PoC-Follow-Up-Recurring-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-Survival-FollowUpRecurring-Plan-Definition"
  * relatedAction[+]
    * actionId = "SoA-PoC-Follow-Up-90-Plan-Definition-S1"
    * relationship = #after
    * offsetDuration = 90 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.low = 83 'd'
    * extension[http://hl7.org/fhir/uv/vulcan-schedule/StructureDefinition/AcceptableOffsetRangeSoa].valueRange.high = 97 'd'
  * timingTiming.repeat
    * period = 90
    * periodUnit = #d
* action[+]
  * id = "SoA-PoC-End-Of-Study-Plan-Definition-S1"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-End-Of-Study-Participation-Plan-Definition"
* action[+]
  * id = "SoA-PoC-Unscheduled-Activity"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Safety-End-Of-Study-Participation-Plan-Definition"
