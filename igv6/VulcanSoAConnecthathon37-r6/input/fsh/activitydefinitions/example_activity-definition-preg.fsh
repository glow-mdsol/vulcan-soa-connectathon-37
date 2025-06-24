Instance: PregnancyTest-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Pregnancy Test Activity Definition"
* title = "Pregnancy Test"
* description = "ActivityDefinition for ordering a pregnancy test."
* status = #active
* kind = #ServiceRequest
* code = http://loinc.org#35064-3 "Pregnancy test panel"
* observationResultRequirement[+] = Canonical(SoA-PoC-Pregnancy-Test-Observation-Definition)
