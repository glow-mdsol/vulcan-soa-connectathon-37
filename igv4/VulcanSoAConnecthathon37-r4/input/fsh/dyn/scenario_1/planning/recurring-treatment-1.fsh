// Profile Definitions
Instance: ChemoDay1
InstanceOf: ActivityDefinition
Title: "Day 1 Chemotherapy Infusion"
Description: "Defines a single chemotherapy treatment"
Usage: #example
* status = #active
* kind = #ServiceRequest
* description = "Day 1 Chemotherapy Infusion"
* productCodeableConcept.text = "Oxaliplatin + 5-FU"
* timingTiming.repeat.duration = 1
* timingTiming.repeat.durationUnit = #d
* timingTiming.repeat.boundsDuration = 14 #d

Instance: AcmePlanDefinition
InstanceOf: PlanDefinition
Title: "ACME Chemotherapy Regimen"
Description: "Repeatable chemotherapy regimen every 14 days until progression"
Usage: #example
* status = #active
* type.text = "Chemotherapy Regimen"
* title = "ACME Chemotherapy Regimen"
* action[+].title = "Repeat Chemotherapy Cycle"
* action[=].description = "Repeat every 14 days until progression or clinician decision"
* action[=].definitionCanonical = "ActivityDefinition/ChemoDay1"
* action[=].timingTiming.repeat.frequency = 1
* action[=].timingTiming.repeat.period = 14
* action[=].timingTiming.repeat.periodUnit = #d
* action[=].condition[+]
  * kind = #applicability
  * expression
    * language = #text/fhirpath
    * expression = "%patient.Observation.where(code.coding.where(code='disease-progression').exists()).empty()"

Instance: CarePlanPatient123
InstanceOf: CarePlan
Title: "CarePlan for Oncology Trial - Cycle 5"
Description: "Shows patient currently on Cycle 5 of chemotherapy"
Usage: #example
* status = #active
* intent = #plan
* title = "Oncology Trial Care Plan"
* subject.reference = "Patient/patient123"
* instantiatesCanonical = "PlanDefinition/AcmePlanDefinition"
* activity[+].detail.kind = #ServiceRequest
* activity[=].detail.status = #in-progress
* activity[=].detail.code.text = "Cycle 5 - Day 1 Chemotherapy"
* activity[=].detail.scheduledTiming.repeat.boundsPeriod.start = "2025-04-25"
* activity[=].detail.scheduledTiming.repeat.boundsPeriod.end = "2025-04-25"

Instance: DiseaseProgressionObservation
InstanceOf: Observation
Title: "Disease Progression Observation"
Description: "Placeholder observation that would indicate disease progression"
Usage: #example
* status = #final
* code = http://example.org/fhir/CodeSystem/oncology-observations#disease-progression "Disease Progression"
* subject.reference = "Patient/patient123"
* effectiveDateTime = "2025-04-20"
* valueBoolean = true