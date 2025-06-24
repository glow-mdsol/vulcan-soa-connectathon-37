
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
* observationResultRequirement[+] = Canonical(UricAcid-ObservationDefinition)
* observationResultRequirement[+] = Canonical(eGFR-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Chloride-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Bicarbonate-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Sodium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Magnesium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Phosphate-ObservationDefinition)
* observationResultRequirement[+] = Canonical(ALT-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalBilirubin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(DirectBilirubin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(LDH-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalProtein-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Albumin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TSH-ObservationDefinition)
* observationResultRequirement[+] = Canonical(FreeT4-ObservationDefinition)
* observationResultRequirement[+] = Canonical(FreeT3-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalT3-ObservationDefinition)
* observationResultRequirement[+] = Canonical(GlucoseFasting-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Calcium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AlkalinePhosphatase-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AST-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Potassium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Creatinine-ObservationDefinition)
* observationResultRequirement[+] = Canonical(BUN-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Glycated-Hemoglobin-ObservationDefinition)


Instance: BloodChemistry-ActivityDefinition-AFP
InstanceOf: ActivityDefinition
Usage: #inline
* name = "Blood Chemistry (including Alpha-fetoprotein (AFP))"
* title = "Blood Chemistry Panel"
* description = "Order blood chemistry laboratory tests."
* status = #active
* kind = #ServiceRequest
* code.coding[+]
  * system = "http://loinc.org"
  * code = #24323-8
  * display = "Basic metabolic 2000 panel - Serum or Plasma"
* observationResultRequirement[+] = Canonical(UricAcid-ObservationDefinition)
* observationResultRequirement[+] = Canonical(eGFR-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Chloride-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Bicarbonate-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Sodium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Magnesium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Phosphate-ObservationDefinition)
* observationResultRequirement[+] = Canonical(ALT-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalBilirubin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(DirectBilirubin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(LDH-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalProtein-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Albumin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TSH-ObservationDefinition)
* observationResultRequirement[+] = Canonical(FreeT4-ObservationDefinition)
* observationResultRequirement[+] = Canonical(FreeT3-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalT3-ObservationDefinition)
* observationResultRequirement[+] = Canonical(GlucoseFasting-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Calcium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AlkalinePhosphatase-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AST-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Potassium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Creatinine-ObservationDefinition)
* observationResultRequirement[+] = Canonical(BUN-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Glycated-Hemoglobin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AFP-ObservationDefinition)


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
* observationResultRequirement[+] = Canonical(UricAcid-ObservationDefinition)
* observationResultRequirement[+] = Canonical(eGFR-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Chloride-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Bicarbonate-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Sodium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Magnesium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Phosphate-ObservationDefinition)
* observationResultRequirement[+] = Canonical(ALT-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalBilirubin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(DirectBilirubin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(LDH-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalProtein-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Albumin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TSH-ObservationDefinition)
* observationResultRequirement[+] = Canonical(FreeT4-ObservationDefinition)
* observationResultRequirement[+] = Canonical(FreeT3-ObservationDefinition)
* observationResultRequirement[+] = Canonical(TotalT3-ObservationDefinition)
* observationResultRequirement[+] = Canonical(GlucoseFasting-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Calcium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AlkalinePhosphatase-ObservationDefinition)
* observationResultRequirement[+] = Canonical(AST-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Potassium-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Creatinine-ObservationDefinition)
* observationResultRequirement[+] = Canonical(BUN-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Glycated-Hemoglobin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(CA125-ObservationDefinition)



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
* observationResultRequirement[+] = Canonical(PlateletCount-ObservationDefinition)
* observationResultRequirement[+] = Canonical(RBC-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Hemoglobin-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Hematocrit-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Neutrophils-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Lymphocytes-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Monocytes-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Eosinophils-ObservationDefinition)
* observationResultRequirement[+] = Canonical(Basophils-ObservationDefinition)

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
* observationResultRequirement[+] = Canonical(ProthrombinTime-ObservationDefinition)
* observationResultRequirement[+] = Canonical(ActivatedPTT-ObservationDefinition)


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
