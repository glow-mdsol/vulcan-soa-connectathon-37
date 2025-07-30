
Instance: BloodChemistry-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Blood Chemistry"
* title = "Blood Chemistry Panel"
* description = "Order blood chemistry laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #24323-8
  * display = "Basic metabolic 2000 panel - Serum or Plasma"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/UricAcid-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/eGFR-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Chloride-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Bicarbonate-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Sodium-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Magnesium-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Phosphate-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/ALT-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/TotalBilirubin-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/DirectBilirubin-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/LDH-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/TotalProtein-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Albumin-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/TSH-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/FreeT4-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/FreeT3-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/TotalT3-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/GlucoseFasting-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Calcium-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/AlkalinePhosphatase-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/AST-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Potassium-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Creatinine-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/BUN-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Glycated-Hemoglobin-ObservationDefinition"

Instance: BloodChemistry-ActivityDefinition-HBA1C
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Blood Chemistry - HbA1C"
* title = "Blood Chemistry Panel - HbA1C"
* description = "Order blood chemistry laboratory tests."
* status = #active
* kind = #ServiceRequest
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Glycated-Hemoglobin-ObservationDefinition"


Instance: BloodChemistry-ActivityDefinition-AFP
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Blood Chemistry (including Alpha-fetoprotein (AFP))"
* title = "Blood Chemistry Panel (required for HCC)"
* description = "Order blood chemistry laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #24323-8
  * display = "Basic metabolic 2000 panel - Serum or Plasma"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/AFP-ObservationDefinition"


Instance: BloodChemistry-ActivityDefinition-CA125
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Blood Chemistry (including CA-125)"
* title = "Blood Chemistry Panel"
* description = "Order blood chemistry laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #24323-8
  * display = "Basic metabolic 2000 panel - Serum or Plasma"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/CA125-ObservationDefinition"


Instance: Hematology-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Hematology"
* title = "Hematology Panel"
* description = "Order hematology laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #58410-2
  * display = "Complete blood count (hemogram) panel - Blood by Automated count"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/PlateletCount-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/RBC-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Hemoglobin-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Hematocrit-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Neutrophils-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Lymphocytes-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Monocytes-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Eosinophils-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/Basophils-ObservationDefinition"

Instance: Coagulation-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Coagulation"
* title = "Coagulation Panel"
* description = "Order coagulation laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #34534-8
  * display = "Coagulation studies (PT, aPTT, INR, Fibrinogen, D-dimer)"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/ProthrombinTime-ObservationDefinition"
* observationResultRequirement[+]
  * reference = "ObservationDefinition/ActivatedPTT-ObservationDefinition"


Instance: SerologyHBV-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Serology HBV"
* title = "Serology for Hepatitis B Virus"
* description = "Order serology tests for Hepatitis B Virus (HBV)."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #5196-1
  * display = "Hepatitis B virus panel - Serum or Plasma"

Instance: Urinalysis-ActivityDefinition
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Urinalysis"
* title = "Urinalysis"
* description = "Order urinalysis laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #24357-6
  * display = "Urinalysis complete panel - Urine"
