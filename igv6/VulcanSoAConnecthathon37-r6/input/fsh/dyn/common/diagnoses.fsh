Instance: HCC-Cohort
InstanceOf: Group
* type = #person
* membership = #enumerated

Instance: HCC
InstanceOf: Condition
Usage: #inline
* clinicalStatus = #active
* code
  * text = "Liver cell carcinoma (disorder)"
  * coding[+] = #109841003 "Liver cell carcinoma (disorder)"
* bodySite[+]
  * text = "Liver structure (body structure)"
  * coding[+] = #10200004 "Liver structure (body structure)"
* subject = Reference(Group/HCC-Cohort)

Instance: SCCHN-Cohort
InstanceOf: Group
Usage: #inline
* type = #person
* membership = #enumerated

Instance: SCCHN
InstanceOf: Condition
Usage: #example
* clinicalStatus = #active
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
* type = #person
* membership = #enumerated

Instance: EOC
InstanceOf: Condition
Usage: #example
* clinicalStatus = #active
* code
  * text = "Neoplasm of ovary (disorder)"
  * coding[+] = #123843001 "Neoplasm of ovary (disorder)" 
* bodySite[+]
  * text = "Ovarian structure (body structure)"
  * coding[+] = #15497006  "Ovarian structure (body structure)"
* subject = Reference(Group/EOC-Cohort)

Instance: GBM-Cohort
InstanceOf: Group
* type = #person
* membership = #enumerated

Instance: GBM
InstanceOf: Condition
Usage: #example
* clinicalStatus = #active
* code
  * text = "Glioblastoma multiforme (disorder)"
  * coding[+] = #393563007 "Glioblastoma multiforme (disorder)"
* bodySite[+]
  * text = "Brain structure (body structure)"
  * coding[+] = #12738006  "Brain structure (body structure)"
* subject = Reference(Group/GBM-Cohort)
