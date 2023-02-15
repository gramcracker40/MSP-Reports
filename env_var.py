import requests
import json
import base64
from dotenv import dotenv_values
from liongardAPI import LiongardAPI

config = dotenv_values(".env")

# CW instance info
cw_id = config["CW_ID"]
cw_url = config["CW_URL"]

# Linking current connectwise codebase to the module
codebase_req = requests.get(f"https://{cw_url}/login/companyinfo/{cw_id}")
codebase_obj = json.loads(codebase_req.text)
accept_codebase = codebase_obj['VersionCode'].strip('v')

cw_base_url = f"https://{cw_url}/{codebase_obj['Codebase']}apis/3.0"

# CW credentials
clientId = config["CW_CLIENT_ID"]
cw_public = config["CW_PUBLIC"]
cw_private = config["CW_PRIVATE"]

# Packaging authentication headers {cw_id}
authorization_key = base64.b64encode(bytes(f"{cw_id}+{cw_public}:{cw_private}", 'utf-8'))

cw_headers = {
    "clientId": clientId,
    "Authorization":f"Basic {authorization_key.decode()}",
    "Accept": f"application/vnd.connectwise.com+json; version={accept_codebase}"
}

# CW MSP CONFIG ID
MSP_report_ID = 73

# CW Routes
post_cw_configuration = cw_base_url + "/company/configurations/"
patch_cw_configuration = cw_base_url + "/company/configurations/"
get_cw_configuration = cw_base_url + "/company/configurations?pageSize=1000"
cw_configuration_count = cw_base_url + "/company/configurations/count"
cw_companies_count = cw_base_url + "/company/companies/count"
cw_companies = cw_base_url + "/company/companies"
cw_status_url = cw_base_url + "/project/statusIndicators"

# Liongard credentials
lg_public = config["LG_PUBLIC"]
lg_private = config["LG_PRIVATE"]
lg_instance = config["LG_INSTANCE"]

# Liongard controller
liongard_controller = LiongardAPI(lg_instance, lg_private, lg_public)

# Liongard metric mappings

lg_metrics = {
    "2416": "Sentinel One total agents",
    "2290": "Sentinel One total threats",
    "2385": "Sentinel One total threats resolved",
    "2206": "Sentinel One total out of date agents",
    "2417": "Cove Data: Total devices",
    "1409": "Cove Data: 24 hours since last backup count",
    "1394": "Cove Data: Protected servers device name(s)",
    "1395": "Cove Data: Protected workstations device name(s)",
    "2395": "N-able RMM: Number of Desktops Failing Daily Safety Checks",
    "2394": "N-able RMM: Number of Servers Failing Daily Safety Checks",
    "2396": "N-able RMM: Number of Desktops Failing 24/7 Checks",
    "2397": "N-able RMM: Number of Servers Failing 24/7 Checks",
    "2400": "N-able RMM: Number of Patches Performed (Workstations)",
    "2401": "N-able RMM: Number of Patches Performed (Servers)",
    "1723": "N-able RMM: Server Count",
    "1724": "N-able RMM: Workstation Count",
}

# holds the metric systems 
master_metric_table = {
    "s1_systems_data": [2416, 2290, 2385, 2206],
    "rmm_systems_data": [2400, 2401, 2394, 2395, 2396, 2397, 1723, 1724], 
    "cove_systems_data": [2417, 1409, 1394, 1395]
}

# matches the metricID from Liongard to the corresponding custom field ID within the
# CW configuration. This ensures that the Liongard metric is posted to the correct field
metric_custom_field_match = {
    "2416": 3,
    "2290": 1,
    "2385": 2,
    "2206": 16,
    "2417": 10,
    "1409": 15,
    "1394": 13,
    "1395": 14,
    "2395": 7,
    "2394": 7,
    "2396": 7,
    "2397": 7,
    "2400": 6,
    "2401": 6,
    "1723": 4,
    "1724": 5,
}

custom_field_types = {
    1: str, 
    2: str, 
    3: str, 
    4: int, 
    5: int,
    6: int, 
    7: int, 
    8: str, 
    9: int,
    10: int, 
    11: int,
    12: str, 
    13: str,
    14: str,
    15: str,
    16: str
}

