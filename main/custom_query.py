

def custom_sql(querry):
    from django.db import connection
    cursor = connection.cursor()
    # Data retrieval operation - no commit required
    cursor.execute(querry)
    row = cursor.fetchall()

    return row  

def request_querry (status,module_code,date_from,date_to,company_id):  
    "new" if status is None else status
    if status=='new':
     status='00'
    elif status=='complete':
     status='11'
    elif status=='in-progress':
     status='44' 
    elif status=='interim':
     status='33'         
    else:
     status='00'

    list_querry=('SELECT pel_psmt_request.request_ref_number,'
                 'pel_psmt_request.bg_dataset_name, '
                 'pel_psmt_request.request_id, '
                 'pel_psmt_request.request_plan, '
                 'pel_psmt_request.dataset_citizenship, '
                 'pel_psmt_request.bg_dataset_email, '
                 'pel_psmt_request.bg_dataset_mobile, '
                 'pel_psmt_request.bg_dataset_idnumber, '
                 'pel_psmt_request.registration_number, '
                 'pel_psmt_request.client_number, '
                 'pel_psmt_request.company_type, '
                 'pel_psmt_request.dataset_incorporation_no, '
                 'pel_psmt_request.dataset_kra_pin, '
                 'pel_psmt_request.request_type, '
                 'pel_psmt_request.dataset_name, '
                 'pel_psmt_request.request_package, '
                 'pel_module.module_code, '
                 'pel_psmt_request.client_id, '
                 'pel_psmt_request.client_login_id, '
                 'pel_psmt_request.client_name, '
                 'pel_psmt_request.request_date, '
                 'pel_psmt_request.package_id, '
                 'pel_psmt_request.verified_date, '
                 'pel_psmt_request.adverse_status, '
                 'pel_psmt_request.company_name '         
                 'FROM '
                 'pel_psmt_request '
                 'INNER JOIN pel_psmt_request_modules ON pel_psmt_request_modules.request_ref_number = pel_psmt_request.request_ref_number '
                 'INNER JOIN pel_module ON pel_psmt_request_modules.module_id = pel_module.module_id '
                 'WHERE '
                 'pel_psmt_request.status="'+status+'" AND '              
                 'pel_module.module_code="'+module_code+'" AND '
                 'pel_psmt_request.request_date >= "'+ date_from+'" AND pel_psmt_request.request_date <= "'+date_to +'" AND '
                 'pel_psmt_request.client_login_id="'+company_id +'"')
    #print(list_querry)                     
    module_data = custom_sql(list_querry) 
    return module_data 

def ngo_society_sacco_trust (status,module_code,date_from,date_to,company_id): 
    "new" if status is None else status
    if status=='new':
     status='00'
    elif status=='complete':
     status='11'
    elif status=='in-progress':
     status='44' 
    elif status=='interim':
     status='33'         
    else:
     status='00'  

    list_querry =('SELECT pel_company_registration.company_name,'
            'pel_psmt_request.request_id, '
            'pel_company_registration.email_address, '
            'pel_company_registration.registration_number, '
            'pel_company_registration.mobile_number, '
            'pel_company_registration.registration_date, '
            'pel_company_registration.country, '
            'pel_company_registration.data_notes, '
            'pel_company_registration.match_status, '
            'pel_company_registration.address, '
            'pel_company_registration.offices, '
            'pel_company_registration.operation_status, '
            'pel_company_registration.industry, '
            'pel_company_registration.module_name, '
            'pel_company_registration.business_type, '
            'pel_company_registration.nature_of_business, '
            'pel_company_registration.postal_address, '
            'pel_company_registration.type, '
            'pel_company_registration.member_count, '
            'pel_company_registration.objective, '
            'pel_company_official_details.role, '
            'pel_company_official_details.`name` AS official_name, '
            'pel_psmt_request.request_ref_number, '
            'pel_psmt_request.request_plan, '
            'pel_psmt_request.`status`, '
            'pel_psmt_request.request_package, '
            'pel_psmt_request.registration_number AS request_reg_number, '
            'pel_psmt_request.client_number, '
            'pel_psmt_request.request_date, '
            'pel_psmt_request_modules.request_id, '
            'pel_psmt_request_modules.module_id, '
            'pel_module.module_code '
            'FROM ' 
            'pel_company_registration '
            'INNER JOIN pel_company_official_details ON pel_company_official_details.company_id = pel_company_registration.company_reg_id '
            'INNER JOIN pel_psmt_request ON pel_company_registration.search_id = pel_psmt_request.request_ref_number '
            'INNER JOIN pel_psmt_request_modules ON pel_psmt_request_modules.request_id = pel_psmt_request.request_ref_number '
            'INNER JOIN pel_module ON pel_psmt_request_modules.module_id = pel_module.module_id '
            'WHERE '
            'pel_psmt_request.status="'+status+'" AND ' 
            'pel_module.module_code="'+module_code+'" AND '
            'pel_psmt_request.request_date BETWEEN "'+ date_from+'" AND "'+date_to +'" AND '
            'pel_psmt_request.client_login_id = "'+company_id +'"') 
    #print(list_querry)         
    module_data = custom_sql(list_querry) 
    return module_data  

def ngo_society_sacco_trust_official_details (request_id): 
    request_id=str(request_id)
    querry=('SELECT pel_company_registration.company_name, '
                'pel_company_registration.email_address, '
                'pel_company_registration.registration_number, '
                'pel_company_registration.mobile_number, '
                'pel_company_registration.registration_date, '
                'pel_company_registration.country, '
                'pel_company_registration.data_notes, '
                'pel_company_registration.match_status, '
                'pel_company_registration.address, '
                'pel_company_registration.offices, '
                'pel_company_registration.operation_status, '
                'pel_company_registration.industry, '
                'pel_company_registration.module_name, '
                'pel_company_registration.business_type, '
                'pel_company_registration.nature_of_business, '
                'pel_company_registration.postal_address, '
                'pel_company_registration.type, '
                'pel_company_registration.member_count, '
                'pel_company_registration.objective, '
                'pel_company_official_details.role, '
                'pel_company_official_details.`name` AS official_name, '
                'pel_psmt_request.request_ref_number, '
                'pel_psmt_request.request_id, '
                'pel_psmt_request.request_plan, '
                'pel_psmt_request.`status`, '
                'pel_psmt_request.request_package, '
                'pel_psmt_request.registration_number AS request_reg_number, '
                'pel_psmt_request.client_number, '
                'pel_psmt_request.request_date, '
                'pel_psmt_request_modules.request_id, '
                'pel_psmt_request_modules.module_id, '
                'pel_psmt_request.request_ref_number, '
                'pel_module.module_code '
                'FROM '
                'pel_company_registration '
                'INNER JOIN pel_company_official_details ON pel_company_official_details.company_id = pel_company_registration.company_reg_id '
                'INNER JOIN pel_psmt_request ON pel_company_registration.search_id = pel_psmt_request.request_ref_number '
                'INNER JOIN pel_psmt_request_modules ON pel_psmt_request_modules.request_id = pel_psmt_request.request_ref_number '
                'INNER JOIN pel_module ON pel_psmt_request_modules.module_id = pel_module.module_id '
                'WHERE '
                'pel_psmt_request.request_id ="'+request_id +'"')          
    module_data = custom_sql(querry) 
    return module_data  

def company_bussiness_clg (request_id): 
    request_id=str(request_id)
    querry=('SELECT pel_company_registration.company_name, '
            'pel_company_registration.email_address, '
            'pel_company_registration.registration_number, '
            'pel_company_registration.mobile_number, '
            'pel_company_registration.registration_date, '
            'pel_company_registration.country, '
            'pel_company_registration.data_notes, '
            'pel_company_registration.match_status, '
            'pel_company_registration.address, '
            'pel_company_registration.offices, '
            'pel_company_registration.operation_status, '
            'pel_company_registration.industry, '
            'pel_company_registration.module_name, '
            'pel_company_registration.business_type, '
            'pel_company_registration.nature_of_business, '
            'pel_company_registration.postal_address, '
            'pel_company_registration.type, '
            'pel_company_registration.member_count, '
            'pel_company_registration.objective, '
            'pel_psmt_request.request_ref_number, '
            'pel_psmt_request.request_id, '
            'pel_psmt_request.request_plan, '
            'pel_psmt_request.`status`, '
            'pel_psmt_request.request_package, '
            'pel_psmt_request.registration_number AS request_reg_number, '
            'pel_psmt_request.client_number, '
            'pel_psmt_request.request_date, '
            'pel_psmt_request_modules.request_id, '
            'pel_psmt_request_modules.module_id, '
            'pel_module.module_code, '
            'pel_company_shares_data.shares_id, '
            'pel_company_shares_data.first_name, '
            'pel_company_shares_data.second_name, '
            'pel_company_shares_data.`status`, '
            'pel_company_shares_data.share_type, '
            'pel_company_shares_data.address, '
            'pel_company_shares_data.added_by, '
            'pel_company_shares_data.verified_by, '
            'pel_company_shares_data.user_id, '
            'pel_company_shares_data.search_id, '
            'pel_company_shares_data.registration_date, '
            'pel_company_shares_data.shafile, '
            'pel_company_shares_data.data_source, '
            'pel_company_shares_data.data_notes, '
            'pel_company_shares_data.match_status, '
            'pel_company_shares_data.third_name, '
            'pel_company_shares_data.shares_number, '
            'pel_company_shares_data.data_id, '
            'pel_company_shares_data.date_added, '
            'pel_company_shares_data.verified_date, '
            'pel_company_shares_data.review_status, '
            'pel_company_shares_data.review_notes, '
            'pel_company_shares_data.percentage, '
            'pel_company_shares_data.id_number, '
            'pel_company_shares_data.business, '
            'pel_company_shares_data.description, '
            'pel_company_shares_data.citizenship '
            'FROM '
            'pel_company_registration '
            'INNER JOIN pel_psmt_request ON pel_company_registration.search_id = pel_psmt_request.request_ref_number '
            'INNER JOIN pel_psmt_request_modules ON pel_psmt_request_modules.request_id = pel_psmt_request.request_ref_number '
            'INNER JOIN pel_module ON pel_psmt_request_modules.module_id = pel_module.module_id '
            'INNER JOIN pel_company_shares_data ON pel_company_shares_data.business = pel_company_registration.company_reg_id '
            'WHERE '
            'pel_psmt_request.request_id ="'+request_id +'"')  
               
    module_data = custom_sql(querry) 
    return module_data  

def encumburances (request_id): 
    request_id=str(request_id)
    querry=('SELECT pel_company_encumbrances.id, '
            'pel_company_encumbrances.search_id, '
            'pel_company_encumbrances.`status`, '
            'pel_company_encumbrances.description, '
            'pel_company_encumbrances.date, '
            'pel_company_encumbrances.amount_secured, '
            'pel_company_encumbrances.added_by, '
            'pel_company_encumbrances.date_added, '
            'pel_company_encumbrances.last_updated, '
            'pel_company_encumbrances.review_status, '
            'pel_company_encumbrances.verified_by, '
            'pel_company_encumbrances.review_notes, '
            'pel_company_encumbrances.verified_date, '
            'pel_company_encumbrances.business, '
            'pel_company_registration.search_id, '
            'pel_psmt_request.request_id '
            'FROM '
            'pel_company_encumbrances '
            'INNER JOIN pel_company_registration ON pel_company_registration.company_reg_id = pel_company_encumbrances.business '
            'INNER JOIN pel_psmt_request ON pel_psmt_request.request_ref_number = pel_company_registration.search_id '
            'WHERE pel_psmt_request.request_id ="'+request_id +'"')

    module_data = custom_sql(querry) 
    return module_data  




def nominal_shares (request_id):
    request_id=str(request_id) 
    querry=('SELECT pel_company_registration.search_id, '
            'pel_psmt_request.request_id, '
            'pel_company_share_capital.id, '
            'pel_company_share_capital.number_of_shares, '
            'pel_company_share_capital.nominal_value, '
            'pel_company_share_capital.`name`, '
            'pel_company_share_capital.business_id '
            'FROM '
            'pel_company_registration '
            'INNER JOIN pel_psmt_request ON pel_psmt_request.request_ref_number = pel_company_registration.search_id '
            'INNER JOIN pel_company_share_capital ON pel_company_share_capital.business_id = pel_company_registration.company_reg_id '
            'WHERE '
            'pel_psmt_request.request_id ="'+request_id +'"')
    module_data = custom_sql(querry)
    return module_data 
