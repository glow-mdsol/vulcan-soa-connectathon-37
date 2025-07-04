Instance: SoA-PoC-ResearchStudy-DynamicProtocol-ScenarioThree
InstanceOf: ResearchStudySoa
Usage: #example
* status = #active
* identifier[+]
  * value = "vulcan_soa_dyn_03"
* title = "Vulcan Schedule of Activities PoC - ResearchStudy Dynamic Scenario 3"
* protocol = Reference(PlanDefinition/SoA-PoC-DynamicProtocol-ScenarioThree-ProtocolDesign)
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

