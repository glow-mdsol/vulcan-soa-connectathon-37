Instance: CTAssessment-Liver-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "CT/MRI Disease Assessment of Liver for Disease Assessment"
* title = "CT/MRI Disease Assessment of Liver for Disease Assessment"
* description = "Order CT or MRI imaging for disease assessment (HCC)."
* status = #active
* kind = #ServiceRequest
* code.coding[+] = #241549007 "Computed tomography of liver (procedure)"
// TODO: Look at diagnostic report/tumor measurement

Instance: MRIAssessment-Liver-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "CT/MRI Disease Assessment of Liver for Disease Assessment"
* title = "CT/MRI Disease Assessment of Liver for Disease Assessment"
* description = "Order CT or MRI imaging for disease assessment (HCC)."
* status = #active
* kind = #ServiceRequest
* code.coding[+] = #241622002 "Magnetic resonance imaging of liver (procedure)"  

Instance: CTMRIAssessment-Ovarian-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "CT/MRI Disease Assessment of Ovary for Disease Assessment"
* title = "CT/MRI Disease Assessment of Ovary for Disease Assessment"
* description = "Order CT or MRI imaging for disease assessment (EOC)."
* status = #active
* kind = #ServiceRequest
* code.coding[+] = #241559008 "Computed tomography ovary (procedure)"
* code.coding[+] = #241628003 "Magnetic resonance imaging of ovary (procedure)"

Instance: CTMRIAssessment-Head-Neck-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "CT/MRI Disease Assessment of Head and Neck for Disease Assessment"
* title = "CT/MRI Disease Assessment of Head and Neck for Disease Assessment"
* description = "Order CT or MRI imaging for disease assessment (SCCHN)."
* status = #active
* kind = #ServiceRequest
* code.coding[+] = #429858000 "Computed tomography of head and neck (procedure)"
* code.coding[+] = #702725003 "Magnetic resonance imaging of head and neck (procedure)"

Instance: CTMRIAssessment-Brain-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "CT/MRI Disease Assessment of Brain for Disease Assessment"
* title = "CT/MRI Disease Assessment of Brain for Disease Assessment"
* description = "Order CT or MRI imaging for disease assessment (GBM)."
* status = #active
* kind = #ServiceRequest
* code.coding[+] = #34227000 "Computed tomography of brain (procedure)"
* code.coding[+] = #816077007 "Magnetic resonance imaging of brain (procedure)"

