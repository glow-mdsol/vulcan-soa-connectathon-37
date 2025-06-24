Instance: SoA-PoC-ResearchStudy-DynamicProtocol-ScenarioThree-Bundle
InstanceOf: Bundle
Usage: #example
* type = #transaction
* entry[+]
  * resource = SoA-PoC-ResearchStudy-DynamicProtocol-ScenarioThree
  * request
    * method = #POST  
    * url = "ResearchStudy"
* entry[+]
  * resource = SoA-PoC-DynamicProtocol-ScenarioThree-ProtocolDesign
  * request
    * method = #POST  
    * url = "PlanDefinition"  
* entry[+]
  * resource = SoA-PoC-Screening-Period-Plan-Definition-Early
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Screening-Period-Plan-Definition-Late
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Cycle1Day1-Plan-Definition
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Cycle1Day8-Plan-Definition
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-Cycle1Day15-Plan-Definition
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource = SoA-PoC-EndOfTreatment-Plan-Definition
  * request
    * method = #POST  
    * url = "PlanDefinition"
* entry[+]
  * resource =  SoA-PoC-Safety-FollowUp30-Plan-Definition 
  * request
    * method = #POST
    * url = "PlanDefinition"
* entry[+]
  * resource =  SoA-PoC-Safety-FollowUp60-Plan-Definition 
  * request
    * method = #POST
    * url = "PlanDefinition"
* entry[+]
  * resource =  SoA-PoC-Safety-FollowUp90-Plan-Definition 
  * request
    * method = #POST
    * url = "PlanDefinition"
* entry[+]
  * resource =  SoA-PoC-Safety-Survival-FollowUpRecurring-Plan-Definition 
  * request
    * method = #POST
    * url = "PlanDefinition"
* entry[+]
  * resource =  SoA-PoC-Safety-End-Of-Study-Participation-Plan-Definition 
  * request
    * method = #POST
    * url = "PlanDefinition"
* entry[+]
  * resource =  InformedConsent-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  EligibilityAssessment-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  MedicalHistory-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  SurgicalHistory-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  SoA-PoC-Demographics-Activity-Definition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  IsatuximabAdministration-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  AtezolizumabAdministration-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  CTMRIAssessment-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  BloodChemistry-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  BloodChemistry-ActivityDefinition-AFP 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  BloodChemistry-ActivityDefinition-CA125 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  Hematology-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  Coagulation-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  SerologyHBV-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  Urinalysis-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource =  SoA-PoC-PerformanceStatus 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = SoA-PoC-Physical-Examination-Activity-Definition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = PregnancyTest-ActivityDefinition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = SoA-PoC-Visit-Date 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = SoA-PoC-Vital-Signs-Screening-Activity-Definition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = SoA-PoC-Vital-Signs-Activity-Definition 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = InitiateVisitProcess 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = RandomizationStatus 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = Randomisation 
  * request
    * method = #POST
    * url = "ActivityDefinition"
* entry[+]
  * resource = HCC-Cohort
  * request
    * method = #POST  
    * url = "Group"
* entry[+]
  * resource = HCC
  * request
    * method = #POST  
    * url = "Condition"
* entry[+]
  * resource = SCCHN-Cohort
  * request
    * method = #POST  
    * url = "Group"
* entry[+]
  * resource = SCCHN
  * request
    * method = #POST  
    * url = "Condition"
* entry[+]
  * resource = EOC-Cohort
  * request
    * method = #POST  
    * url = "Group"
* entry[+]
  * resource = EOC
  * request
    * method = #POST  
    * url = "Condition"
* entry[+]
  * resource = GBM-Cohort
  * request
    * method = #POST  
    * url = "Group"
* entry[+]
  * resource = GBM
  * request
    * method = #POST  
    * url = "Condition"
* entry[+]
  * resource =  UricAcid-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  eGFR-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Chloride-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Bicarbonate-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Sodium-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Magnesium-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Phosphate-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  ALT-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  TotalBilirubin-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  DirectBilirubin-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  LDH-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  TotalProtein-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Albumin-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  TSH-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  FreeT4-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  FreeT3-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  TotalT3-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  GlucoseFasting-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Calcium-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  AlkalinePhosphatase-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  AST-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Potassium-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Creatinine-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  BUN-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  AFP-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  CA125-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Glycated-Hemoglobin-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  ProthrombinTime-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  ActivatedPTT-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-ECG-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  PlateletCount-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  RBC-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Hemoglobin-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Hematocrit-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Neutrophils-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Lymphocytes-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Monocytes-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Eosinophils-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  Basophils-ObservationDefinition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-O2Sats-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-Pregnancy-Test-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-Height-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-SYSBP-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-Diastolic-BP-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-Weight-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
* entry[+]
  * resource =  SoA-PoC-Heart-Rate-Observation-Definition 
  * request
    * method = #POST
    * url = "ObservationDefinition"
