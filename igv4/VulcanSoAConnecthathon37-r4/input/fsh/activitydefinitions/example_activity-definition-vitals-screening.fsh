Instance: SoA-PoC-Vital-Signs-Screening-Activity-Definition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Collect Vital Signs"
* title = "Collect Vital Signs"
* description = "Collect vital signs data from the patient."
* status =  #active
* kind = #Task
* observationResultRequirement[+] = Canonical(SoA-PoC-Vital-Signs-Observation-Definition)

