rename_dict = {'Date':'claim_serviceLines_0_serviceDateFrom',
       'Service Code':'claimserviceLines_0_procedureCode', 'POS':'claimserviceLines_0_placeOfService', 'Units':'claimserviceLines_0_units', 'Last Name':'patient_lastName',
       'First Name':'patient_firstName', 'DOB':'patient_dob', 'Patient Member ID':'insured_id',
       'Clinician NPI':'claimserviceLines_0_renderingProvidernpi',
       'Primary Insurer Name':'payer_name',
       'Primary Diagnosis':'icdA','Rate':'claimserviceLines_0_chargeAmount',
       'Modifier Code 1':'claim_serviceLines_0_procedureModifiers_0', 'Modifier Code 2':'claim_serviceLines_0_procedureModifiers_1',
       'Modifier Code 3':'claim_serviceLines_0_procedureModifiers_2', 'Modifier Code 4':'claim_serviceLines_0_procedureModifiers_3'}


drop_columns = ['Type','Appointment Type','Billing Method','Payment Type','Service Description','Clinician Type','Bill as Supervisor','Supervisor Name','Supervisor NPI','Location',
               'Primary Insurer Group', 'In Network', 'Secondary Insurer Name','Secondary Insurer Group', 'Note Status',
               'Payment Assigned to Practice' , 'Patient Amount Due','Patient Amount Paid', 'Patient Unassigned Credit',
               'Patient Balance Status', 'Insurance Amount Due','Insurance Amount Paid', 'Insurance Unassigned Credit','Insurance Balance Status',
               'Documents Created', 'Comments','Clinician Name'
               ]


all_columns = ['claim_serviceLines_3_Diagnose_pointer', 'claimserviceLines_3_procedureCode', 'claimserviceLines_1_units', 'patient_streetLine1', 'patient_telephone', 'claimserviceLines_1_placeOfService', 'claim_serviceLines_4_procedureModifiers_0', 'icdI', 'claim_serviceLines_1_serviceDateTo', 'claimserviceLines_5_placeOfService', 'claimserviceLines_2_procedureCode', 'claimserviceLines_2_placeOfService', 'claim_serviceLines_4_procedureModifiers_1', 'claim_serviceLines_4_serviceDateFrom', 'patient_city', 'claimserviceLines_2_chargeAmount', 'icdB', 'claim_serviceLines_4_serviceDateTo', 'claimserviceLines_5_procedureCode', 'claim_serviceLines_5_serviceDateFrom', 'claim_serviceLines_1_procedureModifiers_0', 'claim_serviceLines_3_procedureModifiers_0', 'claimserviceLines_4_placeOfService', 'claim_serviceLines_3_serviceDateTo', 'claim_serviceLines_3_serviceDateFrom', 'claim_serviceLines_0_serviceDateTo', 'claim_serviceLines_2_Diagnose_pointer', 'claim_serviceLines_5_serviceDateTo', 'claimserviceLines_1_procedureCode', 'claimserviceLines_3_placeOfService', 'claimserviceLines_1_chargeAmount', 'claim_serviceLines_4_procedureModifiers_2', 'claim_serviceLines_1_Diagnose_pointer', 'claim_serviceLines_1_procedureModifiers_2', 'icdL', 'patient_zip', 'claim_serviceLines_2_procedureModifiers_3', 'icdJ', 'claim_serviceLines_2_serviceDateTo', 'claim_serviceLines_5_Diagnose_pointer', 'claim_serviceLines_2_procedureModifiers_0', 'claimserviceLines_5_units', 'icdK', 'claim_serviceLines_3_procedureModifiers_3', 'claim_serviceLines_2_procedureModifiers_1', 'payer_id', 'claimserviceLines_5_chargeAmount', 'icdH', 'icdD', 'claim_serviceLines_5_procedureModifiers_3', 'claim_serviceLines_5_procedureModifiers_1', 'claim_serviceLines_1_serviceDateFrom', 'patient_state', 'claimserviceLines_3_chargeAmount', 'claimserviceLines_4_chargeAmount', 'claim_serviceLines_1_procedureModifiers_3', 'claimserviceLines_3_units', 'claim_serviceLines_4_procedureModifiers_3', 'patient_middleName', 'claim_serviceLines_0_Diagnose_pointer', 'claim_serviceLines_3_procedureModifiers_2', 'claim_serviceLines_2_procedureModifiers_2', 'claimserviceLines_2_units', 'claim_serviceLines_3_procedureModifiers_1', 'patient_gender', 'claimserviceLines_4_units', 'claim_serviceLines_4_Diagnose_pointer', 'icdF', 'claim_serviceLines_2_serviceDateFrom', 'icdC', 'claim_serviceLines_5_procedureModifiers_0', 'claimserviceLines_4_procedureCode', 'claim_serviceLines_1_procedureModifiers_1', 'claim_serviceLines_5_procedureModifiers_2', 'icdE', 'patient_streetLine2', 'icdG']

get_letter = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L"}


otp_keys = {
       "contact-us+1@gina4med.com":"L3GUZQGQ7GTXCXU5JYMFPN6YKSILIH5KVYYQ3UCUGYPZSX2BB4TQ"
}



