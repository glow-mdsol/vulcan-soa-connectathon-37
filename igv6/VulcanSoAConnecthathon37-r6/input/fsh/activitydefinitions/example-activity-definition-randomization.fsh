
//
// --- Observation Definition - Randomization
//

Instance: RandomizationStatus
InstanceOf: ObservationDefinition
Description: "Randomisation Status"
Usage: #inline
Title: "Randomisation Status"
* status = #registered

* code[+].coding[+].system = "https://library.cdisc.org"
* code[=].coding[=].code = #C186212
* code[=].coding[=].display = "RANDOMIZED"

* permittedDataType = #boolean

//
// --- Activity Definition - Randomization
//

Instance: Randomisation
InstanceOf: ActivityDefinition
Description: "Randomisation"
Usage: #inline
Title: "Research Subject Randomisation"
* status = #draft
* experimental = true
* kind = #Task
* subjectReference = Reference(ResearchSubject/SoA-PoC-ResearchSubject-Bill-Hicks)

* purpose = "Randomise [ResearchSubject] to Treatment Arm as detailed in the [ResearchStudy] Protocol"

* code[+].coding[+].system = "https://library.cdisc.org"
* code[=].coding[=].code = #C186212
* code[=].coding[=].display = "Randomization (Procedure)"

* participant[+].type = #patient
* participant[+].type = #practitioner
* participant[=].role.coding.system = "http://hl7.org/fhir/action-participant-function" 
* participant[=].role.coding.code = #performer
* participant[=].role.coding.display = "Performer"

// * observationResultRequirement[+] = Canonical(RandomizationStatus)

* dynamicValue[+].path = "ResearchSubject"
* dynamicValue[=].expression.language =  #text/fhirpath
* dynamicValue[=].expression.expression =  "ResearchSubject.progress.milestone = #Randomized"