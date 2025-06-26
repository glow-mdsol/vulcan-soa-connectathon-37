Instance: SoA-PoC-ResearchStudy-DynamicProtocol-ScenarioOne
InstanceOf: ResearchStudySoa
Usage: #inline
* status = #active
* identifier[+]
  * value = "vulcan_soa_dyn_01"
* title = "Vulcan Schedule of Activities PoC - ResearchStudy Dynamic Scenario 1"
* protocol = Reference(PlanDefinition/SoA-PoC-DynamicProtocol-ScenarioOne-ProtocolDesign)
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


