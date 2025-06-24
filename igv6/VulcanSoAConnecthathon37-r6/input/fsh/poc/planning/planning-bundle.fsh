Instance: StudyProtocolSoaPoCBundle
InstanceOf: Bundle
Usage: #example
* type = #transaction
* entry[+]
  * resource = Vulcan-SoA-Blood-Pressure-Panel
  * request
    * method = #POST  
    * url = "Questionnaire"
* entry[+]
  * resource = Demographics-Questionnaire
  * request
    * method = #POST  
    * url = "Questionnaire"
* entry[+]
  * resource = Vulcan-SoA-Height-Weight-Panel
  * request
    * method = #POST  
    * url = "Questionnaire"
* entry[+]
  * resource = PHQ-15-Questionnaire
  * request
    * method = #POST  
    * url = "Questionnaire"
* entry[+]
  * resource = SoA-PoC-Visit-Date
  * request
    * method = #POST  
    * url = "ActivityDefinition"
* entry[+]
  * resource = SoA-PoC-ProtocolDesign
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Screening-Visit1
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Baseline-Visit2
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Treatment-Visit3
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Treatment-Visit4
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Treatment-Visit5
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Treatment-Visit6
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Treatment-VisitEOS
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-ResearchStudy
  * fullUrl = "https://soa.vulcan.org/ResearchStudy/vulcan_soa_poc_01"
  * request
    * method = #POST  
    * url = "ResearchStudy"

