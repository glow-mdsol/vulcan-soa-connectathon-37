// https://fhir.mskcc.org/resources/diagnostic-report/

Instance: Example-DiagnosticReport-Complete-Response
InstanceOf: DiagnosticReport
Usage: #inline
* status = #final
* category = #RAD "Radiology"
* code = #97509-4 "Cancer disease progression"
* conclusion = "RECIST Complete Response"
* conclusionCode = $NCIT#C159715 "RECIST Complete Response"

Instance: Example-DiagnosticReport-Partial-Response
InstanceOf: DiagnosticReport
Usage: #inline
* status = #final
* category = #RAD "Radiology"
* code = #97509-4 "Cancer disease progression"
* conclusion = "RECIST Partial Response"
* conclusionCode = $NCIT#C159547 "RECIST Partial Response"

Instance: Example-DiagnosticReport-Progressive-Disease
InstanceOf: DiagnosticReport
Usage: #inline
* status = #final
* category = #RAD "Radiology"
* code = #97509-4 "Cancer disease progression"
* conclusion = "RECIST Progressive Disease"
* conclusionCode = $NCIT#C159716 "RECIST Progressive Disease"

Instance: Example-DiagnosticReport-Stable-Disease
InstanceOf: DiagnosticReport
Usage: #inline
* status = #final
* category = #RAD "Radiology"
* code = #97509-4 "Cancer disease progression"
* conclusion = "RECIST Stable Disease"
* conclusionCode = $NCIT#C159546 "RECIST Stable Disease"

