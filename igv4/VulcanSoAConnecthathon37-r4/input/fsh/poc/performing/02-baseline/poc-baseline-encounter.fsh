Instance: PoC-Baseline-Encounter-Visit-Request
InstanceOf: ServiceRequest
Usage: #example
* status = #active
* intent = #plan
* instantiatesCanonical = "ActivityDefinition/SoA-PoC-Visit-Date"
* subject = Reference(Patient/Bill-Hicks)

Instance: PoC-Baseline-Encounter
InstanceOf: Encounter
Usage: #example
* status = #completed
* class = #AMB
* serviceType = #492 "Medical Research"
* subject = Reference(Patient/Bill-Hicks)
* basedOn = Reference(ServiceRequest/SoA-PoC-Baseline-Visit-Request)
* period
  * start = "2024-05-08T08:00:00Z"
  * end = "2024-05-08T09:00:00Z" 
* location[+]
  * location = Reference(Location/SoA-PoC-Research-Clinic)
  * physicalType = #si "Site"
* serviceProvider = Reference(Organization/SoA-PoC-Research-Clinic)
