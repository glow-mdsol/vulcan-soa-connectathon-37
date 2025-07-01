Instance: HCC-Cohort
InstanceOf: Group
* type = #person
* actual = false

Instance: HCC
InstanceOf: Condition
Usage: #inline
* code
  * text = "Liver cell carcinoma (disorder)"
  * coding[+] = #109841003 "Liver cell carcinoma (disorder)"
* bodySite[+]
  * text = "Liver structure (body structure)"
  * coding[+] = #10200004 "Liver structure (body structure)"
* subject = Reference(Group/HCC-Cohort)
* clinicalStatus = #recurrence

Instance: SCCHN-Cohort
InstanceOf: Group
Usage: #inline
// this needs to be able to be the union of ResearchSubject in ResearchStudy and Disease
* type = #person
* actual = false

Instance: SCCHN
InstanceOf: Condition
Usage: #example
* code
  * text = "Squamous cell carcinoma of head and neck (disorder)"
  * coding[+] = #716659002 "Squamous cell carcinoma of head and neck (disorder)"
* bodySite[+]
  * text = "Head structure (body structure)"
  * coding[+] = #69536005 "Head structure (body structure)"
* bodySite[+]
  * text = "Neck structure (body structure)"
  * coding[+] = #45048000 "Neck structure (body structure)"
* subject = Reference(Group/SCCHN-Cohort)


Instance: EOC-Cohort
InstanceOf: Group
// this needs to be able to be the union of ResearchSubject in ResearchStudy and Disease
* type = #person
* actual = false

Instance: EOC
InstanceOf: Condition
Usage: #example
* code
  * text = "Neoplasm of ovary (disorder)"
  * coding[+] = #123843001 "Neoplasm of ovary (disorder)" 
* bodySite[+]
  * text = "Ovarian structure (body structure)"
  * coding[+] = #15497006  "Ovarian structure (body structure)"
* subject = Reference(Group/EOC-Cohort)

Instance: GBM-Cohort
InstanceOf: Group
// this needs to be able to be the union of ResearchSubject in ResearchStudy and Disease
* type = #person
* actual = false

Instance: GBM
InstanceOf: Condition
Usage: #example
* code
  * text = "Glioblastoma multiforme (disorder)"
  * coding[+] = #393563007 "Glioblastoma multiforme (disorder)"
* bodySite[+]
  * text = "Brain structure (body structure)"
  * coding[+] = #12738006  "Brain structure (body structure)"
* subject = Reference(Group/GBM-Cohort)


Instance: Tom-Daley
InstanceOf: Patient
Usage: #example
* name[+]
  * given = "Tom"
  * family = "Daley"


Instance: Subject-1001
InstanceOf: ResearchSubject
Usage: #inline
* identifier[+]
  * value = "1001"
  * type = #PLAC
* status = #active
* study = Reference(ResearchStudy/SoA-PoC-ResearchStudy-Conditional-Activities)
* individual = Reference(Patient/Tom-Daley)


Instance: Diabetes-1001
InstanceOf: Condition
Usage: #example
* clinicalStatus = #active
* code
  * text = "Diabetes mellitus (disorder)"
  * coding[+] = #73211009 "Diabetes mellitus (disorder)"
* verificationStatus = #confirmed
* subject = Reference(Patient/Tom-Daley)
* category = #diagnosis
