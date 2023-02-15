import requests, json
from env_var import cw_headers, cw_base_url

max_retention = 29
MSP_report_ID = 73

custom_field_id_ref = {
    "1":"2290",
    "2":"2385",
    "3":"2416", 
    "4":"1723",
    "5":"1724",
    "6":"",
    "7":"",
    "8":"",
    "9":"",
    "10":"",
    "11":"",
    "12":""
}

def post_msp_report(company, companyID, metrics=[]):
    
    config_url = cw_base_url + "/company/configurations"
    custom_fields = []
    postable_obj = {
        "company" : {
            "id": companyID
        },
        "type" : {
            "id": MSP_report_ID
        },
        "name": f"{company} MSP Report",
        "customFields": custom_fields
    }
    
    #try adding the SentinelOne data
    try:
        custom_fields.append({
            "id": 1,
            "numberOfDecimals": 0,
            "value": str(metrics["2290"])
            })
        custom_fields.append({
            "id": 2,
            "numberOfDecimals": 0,
            "value": str(metrics["2385"])
            })
        custom_fields.append({
            "id": 3,
            "numberOfDecimals": 0,
            "value": str(metrics["2416"])
            })

    except KeyError:
        pass # simply means there is no SentinelOne inspector in this account
    
    #try adding the RMM data
    try:
        # Cleansing the data to prepare it for the posting in the CW API
        patches_in_rmm = 0
        if type(metrics["2400"]) == int and type(metrics["2401"]) == int:
            patches_in_rmm = metrics["2400"] + metrics["2401"]
        elif type(metrics["2400"]) == int and type(metrics["2401"]) == list:
            patches_in_rmm = metrics["2400"]
        elif type(metrics["2400"]) == list and type(metrics["2401"]) == int:
            patches_in_rmm = metrics["2401"]
        elif type(metrics["2400"]) == list and type(metrics["2401"]) == list:
            patches_in_rmm = 0

        error_metrics = [metrics["2394"], metrics["2395"], metrics["2396"], metrics["2397"]]
        
        total_errors = 0
        for metric in error_metrics:
            if type(metric) == int:
                total_errors += metric

        total_servers = 0
        if type(metrics['1723']) == int or type(metrics['1723']) == str:
            total_servers = int(metrics['1723'])
        else: 
            total_servers = 0

        total_workstations = 0
        if type(metrics['1724']) == int or type(metrics['1724']) == str:
            total_workstations = int(metrics['1724'])
        else:
            total_workstations = 0


        custom_fields.append({
            "id": 4,
            "numberOfDecimals": 0,
            "value": total_servers
            })
        custom_fields.append({
            "id": 5,
            "numberOfDecimals": 0,
            "value": total_workstations
            })
        custom_fields.append({
            "id": 6,
            "numberOfDecimals": 0,
            "value": patches_in_rmm
        })
        custom_fields.append({
            "id": 7,
            "numberOfDecimals": 0,
            "value": total_errors
            })

    except KeyError:
        pass # simply means there is no RMM inspector in this environment
    
    # try adding the cove inspector data
    try:
        #Ensuring the len() func is not run unless they are both list
        num_servers_backing = 0
        num_workstations_backing = 0
        
        # Only if they are lists do we extract the length from them
        # workstations
        if type(metrics['1395']) == list:
            num_workstations_backing = len(metrics['1395'])

        # servers
        if type(metrics['1394']) == list:
            num_servers_backing = len(metrics['1394'])
            

        custom_fields.append({
            "id": 9,
            "numberOfDecimals": 0,
            "value": int(metrics["2417"])
            })
        custom_fields.append({
            "id": 10,
            "numberOfDecimals": 0,
            "value": num_servers_backing
            })
        custom_fields.append({
            "id": 11,
            "numberOfDecimals": 0,
            "value": num_workstations_backing
            })
        custom_fields.append({
            "id": 12,
            "numberOfDecimals": 0,
            "value": str(max_retention)
            })

    except KeyError:
        
        pass # simply means there is no cove inspector in this environment

    # print(f"""{company} : {companyID}\n
    #           {json.dumps(postable_obj, indent=2)}
    #        """)
    #print(postable_obj)
    
    req_conf = requests.post(config_url, headers=cw_headers, json=postable_obj)

    print(req_conf.status_code)
    #print(req_conf.text)

#company, companyID, metrics=[]
def final_post(all_data):
    '''
    Used for the initial posting to all "MSP" client types in CW
        Gave all of them an "MSP Report" 
    '''
    environment_reference_file = open("lg_env_to_cw_companies.json", "r")
    environment_reference = json.load(environment_reference_file)

    process_log = open("logger.txt", "w")


    for env in all_data:
        try:
            post_msp_report(env, environment_reference[env], all_data[env])
        except KeyError as err:
            process_log.write(f"{err}\n")
        
        break
