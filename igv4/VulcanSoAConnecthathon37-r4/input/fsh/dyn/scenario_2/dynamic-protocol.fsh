Instance: SoA-PoC-ResearchStudy-DynamicProtocol-ScenarioTwo
InstanceOf: ResearchStudySoa
Usage: #example
* status = #active
* identifier[+]
  * value = "vulcan_soa_dyn_02"
* title = "Vulcan Schedule of Activities PoC - ResearchStudy Dynamic Scenario 2"
* protocol = Reference(PlanDefinition/SoA-PoC-DynamicProtocol-ScenarioTwo-ProtocolDesign)
* phase = $research-study-phase#phase-2 "Phase 2"
* arm[+]
  * name = "SCCHN"
  * description = "Patient Cohort: Squamous Cell Carcinoma of the Head and Neck"
* arm[+]
  * name = "HCC"
  * description = "Patient Cohort: Hepatocellular Carcinoma"
* arm[+]
  * name = "EOC"
  * description = "Patient Cohort: Epithelial Ovarian Carcinoma"
* arm[+]
  * name = "GBM"
  * description = "Patient Cohort: Glioblastoma Multiforme"

