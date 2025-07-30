Instance: SoA-PoC-Vital-Signs-Screening-Activity-Definition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Collect Vital Signs"
* title = "Collect Vital Signs"
* description = "Collect vital signs data from the patient."
* status =  #active
* kind = #Task
* observationResultRequirement[+] 
  * reference = "ObservationDefinition/SoA-PoC-Height-Observation-Definition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/SoA-PoC-Weight-Observation-Definition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/SoA-PoC-Temperature-Observation-Definition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/SoA-PoC-SYSBP-Observation-Definition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/SoA-PoC-Diastolic-BP-Observation-Definition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/SoA-PoC-Heart-Rate-Observation-Definition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/SoA-PoC-Respiratory-Rate-Observation-Definition"
