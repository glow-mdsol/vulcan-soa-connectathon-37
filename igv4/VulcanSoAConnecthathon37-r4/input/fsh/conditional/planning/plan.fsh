Instance: SoA-PoC-Conditional-ProtocolDesign
InstanceOf: StudyProtocolSoa
Usage: #inline
* status = #active
* title = "Vulcan Schedule of Activities PoC - Conditional Activities"
* action[+]
  * title = "Screening (D-28 to D-14)"
  * definitionCanonical = "PlanDefinition/SoA-PoC-Conditional-Visit-1" 


Instance: SoA-PoC-Conditional-Visit-1
InstanceOf: StudyVisitSoa
Usage: #inline
* status = #active
* title = "Visit 1 - Screening"
* action[+]
  * definitionCanonical = "ActivityDefinition/PregnancyTest-ActivityDefinition"
  * title = "Pregnancy Test"
  * condition[+]
    * kind = #applicability
    * expression
      * description = "Pregnancy test for Biological Females"
      * language = #text/fhirpath
      * expression = "Patient.gender='female'"
  * condition[+]
    * kind = #applicability
    * expression
      * description = "Evaluation of Fertility"
      * language = #text/fhirpath
      // 118183008 | Finding of fertility (finding) |
      // 8619003 | Infertile (finding) |
      * expression = "Observation.where(subject.reference = 'Patient/' + Id).where(code.coding.system = 'http://snomed.info/sct' and code.coding.code = '118183008').valueCodeableConcept!='http://snomed.info/sct|8619003'"
* action[+]
  * definitionCanonical = "ActivityDefinition/BloodChemistry-ActivityDefinition"
  * title = "Blood Chemistry"
* action[+]
  * definitionCanonical = "ActivityDefinition/BloodChemistry-HBA1C-ActivityDefinition"
  * title = "Blood Chemistry - Diabetic"
  * condition[+]
    * kind = #applicability
    * expression
      * description = "Blood Chemistry with HbA1c"
      * language = #text/fhirpath
      * expression = "Condition.where(subject.reference = 'Patient/' + Id).where(code.coding.system = 'http://snomed.info/sct' and code.coding.code = '73211009').exists()"
