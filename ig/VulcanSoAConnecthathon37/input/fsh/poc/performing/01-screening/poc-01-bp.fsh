Instance: PoC-01-BP-QuestionnaireResponse
InstanceOf: QuestionnaireResponse
Usage: #example
* questionnaire = "Questionnaire/Vulcan-SoA-Blood-Pressure-Panel"
* status = #completed
* subject = Reference(Patient/Bill-Hicks) 
* authored = "2024-09-04T15:52:29.265Z"
* author
  * reference = Reference(Practitioner/smart-Practitioner-71482713)
  * type = #Practitioner
  * display = "Susan Clark"
* item[+]
  * linkId = "/96608-5"
  * text = "BP Sys Avg"
  * answer.valueDecimal = 120
* item[+]
  * linkId = "/96609-3"
  * text = "BP Dias Avg"
  * answer.valueDecimal = 80
