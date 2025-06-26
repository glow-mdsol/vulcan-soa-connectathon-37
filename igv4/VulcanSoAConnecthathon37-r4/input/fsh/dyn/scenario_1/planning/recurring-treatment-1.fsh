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

Instance: TreatmentCycles-Cycle2-Plus-PlanDefinition
InstanceOf: PlanDefinition
Title: "ACME Chemotherapy Regimen"
Description: "Repeatable chemotherapy regimen every 21 days until progression"
Usage: #example
* status = #active
* type.text = "Chemotherapy Regimen"
* title = "ACME Chemotherapy Regimen"
* action[+]
  * title = "Physical Examination"
  * definitionCanonical = "ActivityDefinition/SoA-PoC-Physical-Examination-Activity-Definition"
* action[+]
  * title = "Vital Signs"
  * definitionCanonical = "ActivityDefinition/SoA-PoC-Vital-Signs-Activity-Definition"
* action[+]
  * title = "Performance Status"
  * definitionCanonical = "ActivityDefinition/SoA-PoC-PerformanceStatus"
* action[+]
  * title = "Resting O2 Saturation"
  * definitionCanonical = "ActivityDefinition/O2Sats-ActivityDefinition"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/SCCHN-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
* action[+]
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
  * definitionCanonical = "ActivityDefinition/Blood-Typing-Interference-Test-ActivityDefinition"
  * title = "Blood Typing Interference Test"
  * description = "Blood Typing Interference Test (Cycle 2 Day 1 only)"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
* action[+]
  * definitionCanonical = "ActivityDefinition/BloodChemistry-ActivityDefinition"
  * title = "Blood Chemistry"
* action[+]
  * definitionCanonical = "ActivityDefinition/Hematology-ActivityDefinition"
  * title = "Hematology"
* action[+]
  * definitionCanonical = "ActivityDefinition/Coagulation-ActivityDefinition"
  * title = "Coagulation (for GBM)"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/GBM-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
* action[+]
  * title = "Isatuximab Administration"
  * definitionCanonical = "ActivityDefinition/IsatuximabAdministration-ActivityDefinition"
* action[+]
  * title = "Atezolizumab Administration"
  * definitionCanonical = "ActivityDefinition/AtezolizumabAdministration-ActivityDefinition"
* action[+]
  * title = "Send a AppointmentRequest for 21 days"
  // Hook on encounter start; add extension to   

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