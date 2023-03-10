# handles the CW side of "MSP Reports" facilitating updates of current configs, creating new configs
#      gathers MSP clients and is able to check which ones have no MSP Report config and posts one for those companies
import os, sys, logging
import requests, json, math

# linking package to this module to import env_var
package = os.getcwd()
sys.path.insert(1,package)
from env_var import cw_headers, get_cw_configuration , cw_configuration_count, custom_field_types, patch_cw_configuration
from env_var import MSP_report_ID, post_cw_configuration, master_metric_table, metric_custom_field_match

# setting up logger
logging.basicConfig(level=logging.DEBUG, filename="MSP_Report.log", format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def get_all_msp_report_configs():
    '''
    grabs all "MSP Report" configurations from Connectwise and returns them
    '''
    config_count = json.loads(requests.get(cw_configuration_count, headers=cw_headers).text)
    max_pages = math.ceil(int(config_count['count']) / 1000)

    msp_reports = []
    for page in range(max_pages):
        url = get_cw_configuration + f"&page={page+1}"

        req = requests.get(url, headers=cw_headers)

        if req.status_code != 200:
            logger.error(f"""def get_all_msp_report_configs(): cw_msp_reports.py\n 
                            Status received from request {req.status_code}
                            Returned text {req.text}""")

        page_configurations = json.loads(req.text)
        
        configs = [config for config in page_configurations
                   if config['type']['id'] == MSP_report_ID]
        msp_reports.append(configs)
                
    return msp_reports


def get_all_msp_companies():
    '''
    grabs a list of all companies with the type "MSP" from Connectwise 

    needs: updated json list produced by grab_cw_companies.py
    '''
    companies_file = open('data\companies_and_IDs_CW.json', 'r')
    companies = json.load(companies_file)

    msp_companies = []
    for company in companies:
        if type(company['types']) == list:
            for each in company['types']:
                if each['name'].lower() == "msp":
                    msp_companies.append(company)
                    break 
        else:
            if each['name'].lower() == "msp":
                    msp_companies.append(company)

    return msp_companies

# Function dependant global variables
configs = get_all_msp_report_configs()
user_entered = json.load(open('lg_env_to_cw_companies.json', 'r'))

def post_not_posted(have_nots=[], list_IDs=[]):
    '''
    grabs the companies returned from the check_msp_companies_msp_report function
        and posts a new, blank "MSP Report" configuration to that ID 

    purpose: to help ensure all MSP type companies have an "MSP Report" config
        by posting after the two checks, check_user_entered_IDs(), and check_msp_companies_msp_report()
    '''
    if have_nots != []:
        IDs = [x['id'] for x in have_nots]

        for count, id in enumerate(IDs):
            postable_obj = {
                "company" : {
                    "id": id
                },
                "type" : {
                    "id": MSP_report_ID
                },
                "name": f"{have_nots[count]['name']} MSP Report"
            }

        req = requests.post(post_cw_configuration, headers=cw_headers, json=postable_obj)

        if req.status_code == 201:
            logger.info(f"posted new 'MSP Report' successfully --- {have_nots[count]['name']}")
        else:
            logger.error(f"error posting new 'MSP Report' : {have_nots[count]['name']}")

    if list_IDs != []:
        for id in list_IDs:
            postable_obj = {
                "company" : {
                    "id": id
                },
                "type" : {
                    "id": MSP_report_ID
                },
                "name": f"{user_entered['id_to_env'][str(id)]} MSP Report"
            }

        req = requests.post(post_cw_configuration, headers=cw_headers, json=postable_obj)

        if req.status_code == 201:
            logger.info(f"posted new 'MSP Report' successfully --- {user_entered['id_to_env'][str(id)]}")
        else:
            logger.error(f"error posting new 'MSP Report' : {user_entered['id_to_env'][str(id)]}")


def check_msp_companies_msp_report():
    '''
    filters through all type "MSP" companies and ensures they have an "MSP Report" config
    will return the list of companies who do not have an "MSP Report" in their configurations
    
    returns: list of MSP companies without a "MSP Report"
    '''

    companies = get_all_msp_companies()

    have_nots_ = []
    for company in companies:
        have = False
        for config in configs:
            if config['company']['name'] == company['name']:
                have = True
                break
        if not have:
            have_nots_.append(company)

    post_not_posted(have_nots=have_nots_)
    #return have_nots

# user_entered is used across multiple functions as a 
# lookup dictionary for interchanging Liongard Environments with CW Company ID's

def check_user_entered_IDs():
    '''
    a check for the companies placed in lg_env_to_cw_companies.json to ensure
    the company ID's placed there have a configuration to patch later on

    compares: lg_env_to_cw_companies.json id's against the returned 
        configurations company id's from get_all_msp_report_configs()
    
    returns: list of company ID's without MSP Report configurations. 
    '''

    for id in user_entered['id_to_env']:
        matched = [x['id'] for x in configs if int(id) == x['company']['id']]
        
        if not matched:
            logger.info(f"Adding new 'MSP Report' configuration to {user_entered['id_to_env'][id]}")
            post_not_posted(list_IDs=[id])




def update_reports(matched_systems):
    '''
    grabs a list of MSP reports and tries to match them based on lg_env_to_cw_companies.json
        once "matched" it will patch the new data from matched_systems into the appropriate fields
        within the corresponding companies "MSP Report"
    
    needs: matched_systems produced by match_systems_and_environments()
    '''
    msp_reports = get_all_msp_report_configs()
    lg_cw_connector = json.load(open("lg_env_to_cw_companies.json", "r"))

    rmm_patches_field_id = 6
    rmm_errors_field_id = 7

    #print(msp_reports[0].keys())
    
    for env in matched_systems:
        try:
            matched_report_id = [x["id"] for x in msp_reports 
                    if x["company"]["id"] == int(lg_cw_connector["env_to_id"][env])]

            if matched_report_id:
                custom_fields = []
                update_obj = {
                    "company" : {
                        "id": int(lg_cw_connector["env_to_id"][env])
                    },
                    "type" : {
                        "id": MSP_report_ID
                    },
                    "status": {
                        "name": "Active"
                    },
                    "name": f"{env} MSP Report",
                    "customFields": custom_fields
                }

                patches_performed = 0
                rmm_errors = 0
                for metric in matched_systems[env]:
                    value = ""
                    
                    # For accumulating total patches and errors in RMM, and then patching
                    if metric_custom_field_match[metric] == 6:
                        patches_performed += matched_systems[env][metric]
                        continue
                    elif metric_custom_field_match[metric] == 7:
                        rmm_errors += matched_systems[env][metric]
                        continue
                    
                    # If there are multiple devices, parse into single string
                    if type(matched_systems[env][metric]) == list and matched_systems[env][metric]:
                        for device in matched_systems[env][metric]:
                            value += device + ", "
                    elif not matched_systems[env][metric]:
                        continue
                    else:
                        value = str(matched_systems[env][metric])

                    # If the custom_field_type is a text area or field
                    if custom_field_types[metric_custom_field_match[metric]] == str and value != '':
                        custom_field = {
                            "id": metric_custom_field_match[metric],
                            "numberOfDecimals": 0,
                            "value": value
                        }
                        custom_fields.append(custom_field)

                    # If the custom_field_type is a number
                    elif custom_field_types[metric_custom_field_match[metric]] == int and value != '':
                        custom_field = {
                            "id": metric_custom_field_match[metric],
                            "numberOfDecimals": 0,
                            "value": int(value)
                        }
                        custom_fields.append(custom_field)
                
                if patches_performed != 0:
                    custom_field = {
                            "id": rmm_patches_field_id,
                            "numberOfDecimals": 0,
                            "value": patches_performed
                        }
                    custom_fields.append(custom_field)

                if rmm_errors != 0:
                    custom_field = {
                            "id": rmm_errors_field_id,
                            "numberOfDecimals": 0,
                            "value": rmm_errors
                        }
                    custom_fields.append(custom_field)
                
                #print(json.dumps(update_obj, indent=2))
                # patching the correct report
                url = patch_cw_configuration + str(matched_report_id[0])
                update_req = requests.put(url, headers=cw_headers, json=update_obj)

                if update_req.status_code != 200:
                    logger.error(f"Did not successfully update 'MSP Report' for {env} :: Check list of company ID's")
                    print(update_req.text)
                    print(update_obj)
                else:
                    logger.info(f"Successfully updated 'MSP Report' for {env}")

            else:
                logger.error(f"did not find id for '{env}' check lg_env_to_cw_companies.json")
            

        except KeyError as err:
            logger.error(f"cw_msp_reports.py --> update_reports() --> " + 
                         f"KeyError : lg_env_to_cw_companies.json is missing --> {err}")






# from filter_systems import filtered_systems
# from report_data import get_all_systems_data, match_systems_and_environments
# # # will pull back all of our current Sentinel One, N-Able RMM, and Cove backup inspector
# s1_systems_data, rmm_systems_data, cove_systems_data = filtered_systems()

# test = get_all_systems_data([s1_systems_data, rmm_systems_data, cove_systems_data], metric_table=master_metric_table)
# filtered_test = match_systems_and_environments(test, [s1_systems_data, rmm_systems_data, cove_systems_data])

# update_reports(filtered_test)
