Instance: IsatuximabAdministration-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Isatuximab Administration"
* title = "Isatuximab Administration"
* description = "Administer Isatuximab to the participant."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://www.whocc.no/atc"
  * code = #L01FC02
  * display = "Isatuximab"

Instance: AtezolizumabAdministration-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Atezolizumab Administration"
* title = "Atezolizumab Administration"
* description = "Administer Atezolizumab to the participant."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://www.whocc.no/atc"
  * code = #L01FF05
  * display = "Atezolizumab"

