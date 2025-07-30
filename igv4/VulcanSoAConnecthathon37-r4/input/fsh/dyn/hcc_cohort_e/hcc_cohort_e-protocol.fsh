Instance: SoA-PoC-ResearchStudy-DynamicProtocol-HCC-Cohort-E
InstanceOf: ResearchStudySoa
Usage: #inline
* status = #active
* identifier[+]
  * value = "vulcan_soa_hcc_cohort_e"
* title = "Vulcan Schedule of Activities PoC - ResearchStudy Dynamic Scenario (HCC Cohort E)"
* protocol = Reference(PlanDefinition/SoA-PoC-DynamicProtocol-ScenarioOne-ProtocolDesign)
* phase = #phase-2 "Phase 2"
* primaryPurposeType = #treatment "Treatment"
* focus[+]
  * code = $research-study-focus#hcc "Hepatocellular Carcinoma"
* focus[+]
  * code[+]
    * coding[+]
      * system = "http://www.whocc.no/atc"
      * code = #L01FC02
      * display = "Isatuximab"
* arm[+]
  * name = "HCC"
  * description = "Patient Cohort: Hepatocellular Carcinoma"

