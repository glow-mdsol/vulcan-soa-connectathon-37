Instance: CTMRIAssessment-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "CT/MRI Disease Assessment"
* title = "CT/MRI Disease Assessment"
* description = "Order CT or MRI imaging for disease assessment."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://snomed.info/sct"
  * code = #77477000
  * display = "Computerized tomography of whole body"
* code.coding[+]
  * system = "http://snomed.info/sct"
  * code = #113091000119100
  * display = "Magnetic resonance imaging of whole body"

