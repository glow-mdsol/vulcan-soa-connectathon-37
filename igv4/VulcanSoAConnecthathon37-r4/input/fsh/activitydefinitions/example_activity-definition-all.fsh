Instance: InformedConsent-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Informed Consent"
* title = "Informed Consent"
* description = "Obtain written informed consent from the participant."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://snomed.info/sct"
  * code = #311401005
  * display = "Consent for clinical procedure"

Instance: EligibilityAssessment-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Eligibility Criteria Assessment"
* title = "Eligibility Criteria Assessment"
* description = "Assess participant eligibility according to protocol criteria."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://snomed.info/sct"
  * code = #386053000
  * display = "Evaluation and management of patient"


Instance: MedicalHistory-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Medical History"
* title = "Medical History"
* description = "Collect participant's medical history."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #11348-0
  * display = "History of Past Illness"

Instance: SurgicalHistory-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Surgical History"
* title = "Surgical History"
* description = "Collect participant's surgical history."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #29554-3
  * display = "Surgical procedures"


