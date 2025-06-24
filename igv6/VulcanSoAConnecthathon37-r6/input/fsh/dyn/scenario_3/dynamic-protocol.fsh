Instance: SoA-PoC-ResearchStudy-DynamicProtocol-ScenarioThree
InstanceOf: ResearchStudySoa
Usage: #example
* status = #active
* identifier[+]
  * value = "vulcan_soa_dyn_03"
* title = "Vulcan Schedule of Activities PoC - ResearchStudy Dynamic Scenario 3"
* protocol = Reference(PlanDefinition/SoA-PoC-DynamicProtocol-ScenarioThree-ProtocolDesign)
* phase = $research-study-phase#phase-2 "Phase 2"
* comparisonGroup[+]
  * observedGroup = Reference(Group/SCCHN-Group)
  * description = "Patient Cohort: Squamous Cell Carcinoma of the Head and Neck"
* comparisonGroup[+]
  * observedGroup = Reference(Group/HCC-Group)
  * description = "Patient Cohort: Hepatocellular Carcinoma"
* comparisonGroup[+]
  * observedGroup = Reference(Group/EOC-Group)
  * description = "Patient Cohort: Epithelial Ovarian Carcinoma"
* comparisonGroup[+]
  * observedGroup = Reference(Group/GBM-Group)
  * description = "Patient Cohort: Glioblastoma Multiforme"

