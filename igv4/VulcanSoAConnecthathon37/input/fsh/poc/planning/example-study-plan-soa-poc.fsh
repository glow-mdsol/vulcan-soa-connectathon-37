Instance: SoA-PoC-ProtocolDesign
InstanceOf: StudyProtocolSoa
Description: "SoA-PoC-Study-Plan"
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities - Study Plan"
* type = http://terminology.hl7.org/CodeSystem/plan-definition-type#clinical-protocol
* date = "2024-05-08"
* version = "Vulcan-SoA-PoC-1.0"
* purpose = "The purpose of this PlanDefinition is to illustrate the planned study encounters and use SDC to populate the study data."
* identifier[+]
  * value = "SoA-PoC-Protocol-Design"
  * type = http://terminology.hl7.org/CodeSystem/v2-0203#PLAC
  * use = #usual
* action[+]
  * id = "SoA-PoC-VISIT-1"
  * title = "Record Visit Date"
  * definitionUri = "PlanDefinition/SoA-PoC-Screening-Visit1"
  * relatedAction[+] 
    * actionId = "SoA-PoC-Visit-3"
    * relationship = #before
    * offsetDuration = 21 'd'
    * extension[acceptableOffsetRange].valueRange.low = 18 'd'    
    * extension[acceptableOffsetRange].valueRange.high = 24 'd'    
* action[+]
  * id = "SoA-PoC-Visit-2"
  * title = "Baseline"
  * definitionUri = "PlanDefinition/SoA-PoC-Baseline-Visit2"
  * relatedAction[+] 
    * actionId = "SoA-PoC-Visit-3"
    * relationship = #before
    * offsetDuration = 1 'd'
* action[+]
  * id = "SoA-PoC-Visit-3"
  * title = "Treatment - Day 1"
  * definitionUri = "PlanDefinition/SoA-PoC-Treatment-Visit3"
* action[+]
  * id = "SoA-PoC-Visit-4"
  * title = "Treatment - Day 7"
  * definitionUri = "PlanDefinition/SoA-PoC-Treatment-Visit4"
  * relatedAction[+] 
    * actionId = "SoA-PoC-Visit-3"
    * relationship = #after
    * offsetDuration = 7 'd'
    * extension[acceptableOffsetRange].valueRange.low = 6 'd'    
    * extension[acceptableOffsetRange].valueRange.high = 8 'd'    
* action[+]
  * id = "SoA-PoC-Visit-5"
  * title = "Treatment - Day 14"
  * definitionUri = "PlanDefinition/SoA-PoC-Treatment-Visit5"
  * relatedAction[+] 
    * actionId = "SoA-PoC-Visit-3"
    * relationship = #after
    * offsetDuration = 14 'd'
    * extension[acceptableOffsetRange].valueRange.low = 12 'd'    
    * extension[acceptableOffsetRange].valueRange.high = 17 'd'    
* action[+]
  * id = "SoA-PoC-Visit-6"
  * title = "Treatment - Day 21"
  * definitionUri = "PlanDefinition/SoA-PoC-Treatment-Visit6"
  * relatedAction[+] 
    * actionId = "SoA-PoC-Visit-3"
    * relationship = #after
    * offsetDuration = 21 'd'
    * extension[acceptableOffsetRange].valueRange.low = 19 'd'    
    * extension[acceptableOffsetRange].valueRange.high = 24 'd'    
* action[+]
  * id = "SoA-PoC-Visit-EOS"
  * title = "Treatment - End of Study"
  * definitionUri = "PlanDefinition/SoA-PoC-EOS-VisitEOS"
  * relatedAction[+] 
    * actionId = "SoA-PoC-Visit-3"
    * relationship = #after
    * offsetDuration = 28 'd'
    * extension[acceptableOffsetRange].valueRange.low = 26 'd'    
    * extension[acceptableOffsetRange].valueRange.high = 30 'd'    

