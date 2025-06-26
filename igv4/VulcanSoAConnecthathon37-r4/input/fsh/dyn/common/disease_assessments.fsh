Instance: Disease-Assessment 
InstanceOf: PlanDefinition
Usage: #inline
* title = "Disease Assessment for Study Cohorts"
* status = #active
* action[+]
  * id = "SoA-PoC-Disease-Assessment-HCC"
  * timingTiming
    * repeat
      * period = 9
      * periodUnit = #wk
      * count = 3
  * condition[+]
    * kind = #applicability
    * expression
      * description = "Patient has HCC"
      * language = #text/fhirpath
      //* expression = "ResearchSubject.where(individual = 'Patient/' + Id).where(arm = 'HCC-Cohort')"
      //* expression = "Condition.where(subject.reference = 'Patient/' + Id).where(code.coding.system = 'http://snomed.info/sct' and code.coding.code = '109841003').exists()"
      * expression = "Group.where(id = 'Group/HCC-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-HCC-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Liver-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-HCC"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-HCC-Imaging"
      * relationship = #after
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-AFP"
    * definitionCanonical = "ActivityDefinition/BloodChemistry-ActivityDefinition-AFP"
* action[+]
  * id = "SoA-PoC-Disease-Assessment-HCC-Cont"
  * timingTiming
    * repeat
      * period = 12
      * periodUnit = #wk
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/HCC-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * relatedAction[+]
    * actionId = "SoA-PoC-Disease-Assessment-HCC"
    * relationship = #after
    * offsetDuration = 12 'wk'
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-HCC-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Liver-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-AFP"
    * definitionCanonical = "ActivityDefinition/BloodChemistry-ActivityDefinition-AFP"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-HCC"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-HCC-Imaging"
      * relationship = #after
* action[+]
  * id = "SoA-PoC-Disease-Assessment-SCCHN"
  * timingTiming
    * repeat
      * period = 9
      * periodUnit = #wk
      * count = 3
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/SCCHN-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-SCCHN-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Head-Neck-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-SCCHN"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-SCCHN-Imaging"
      * relationship = #after
* action[+]
  * id = "SoA-PoC-Disease-Assessment-SCCHN-Cont"
  * timingTiming
    * repeat
      * period = 12
      * periodUnit = #wk
  * relatedAction[+]
    * actionId = "SoA-PoC-Disease-Assessment-SCCHN"
    * relationship = #after
    * offsetDuration = 12 'wk'
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/SCCHN-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-SCCHN-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Head-Neck-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-SCCHN"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-SCCHN-Imaging"
      * relationship = #after
* action[+]
  * id = "SoA-PoC-Disease-Assessment-EOC"
  * timingTiming
    * repeat
      * period = 9
      * periodUnit = #wk
      * count = 3
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/EOC-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-CA125"
    * definitionCanonical = "ActivityDefinition/BloodChemistry-ActivityDefinition-CA125"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-EOC-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Ovarian-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-EOC"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-EOC-Imaging"
      * relationship = #after
* action[+]
  * id = "SoA-PoC-Disease-Assessment-EOC-Cont"
  * timingTiming
    * repeat
      * period = 12
      * periodUnit = #wk
  * relatedAction[+]
    * actionId = "SoA-PoC-Disease-Assessment-EOC"
    * relationship = #after 
    * offsetDuration = 12 'wk'
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/EOC-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-CA125"
    * definitionCanonical = "ActivityDefinition/BloodChemistry-ActivityDefinition-CA125"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-EOC-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Ovarian-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-EOC"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-EOC-Imaging"
      * relationship = #after
* action[+]
  * id = "SoA-PoC-Disease-Assessment-GBM"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/GBM-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * timingTiming
    * repeat
      * period = 6
      * periodUnit = #wk
      * count = 4
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-GBM-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Brain-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-GBM"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-GBM-Imaging"
      * relationship = #after
* action[+]
  * id = "SoA-PoC-Disease-Assessment-GBM-Cont"
  * condition[+]
    * kind = #applicability
    * expression
      * language = #text/fhirpath
      * expression = "Group.where(id = 'Group/GBM-Cohort').where(member.entity.reference = 'Patient/' + Id).exists()"
  * relatedAction[+]
    * actionId = "SoA-PoC-Disease-Assessment-GBM"
    * relationship = #after
    * offsetDuration = 12 'wk'
  * timingTiming
    * repeat
      * period = 12
      * periodUnit = #wk
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-GBM-Imaging"
    * definitionCanonical = "ActivityDefinition/CTMRIAssessment-Brain-ActivityDefinition"
  * action[+]
    * id = "SoA-PoC-Disease-Assessment-GBM"
    * definitionCanonical = "ActivityDefinition/DiseaseAssessment"
    * relatedAction[+]
      * actionId = "SoA-PoC-Disease-Assessment-GBM-Imaging"
      * relationship = #after
