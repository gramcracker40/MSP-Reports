# grabs all the companies in Connectwise and dumps them into a json file. 
# includes all pertinent information to the connectwise organization

import requests
import json
import math
import sys
import os

# linking package to this module to import env_var
package = os.getcwd()
sys.path.insert(1,package)

import env_var

###############################################################
###############################################################
# Main Process 
# grabbing companies based off the max of 1000 companies in CW API
# per request, grabs number of companies in CW instance, makes the requests
# for each of those pages, seperates them into individual companies in a
# single list that we then place in companies_and_IDs_CW.json
###############################################################


def get_companies(page):
    get_url = f"{env_var.cw_base_url}/company/companies?pagesize=1000&page={page}"
    companies = requests.get(get_url, headers=env_var.cw_headers)
    companies_obj = json.loads(companies.text)

    return companies_obj


count = requests.get(env_var.cw_companies_count, headers=env_var.cw_headers)
count_obj = json.loads(count.text)

#grabbing max number of pages needed to pull back 
max_pages = math.ceil(int(count_obj['count']) / 1000)

#grabbing each page from the CW API 
all_companies = open('data/companies_and_IDs_CW.json', 'w')
list_of_companies = []
for page in range(max_pages):
    companies = get_companies(page+1)
    #print(f"Request #{page + 1} completed")

    list_of_companies.append(companies)


#making it a single list of companies, instead of multiple lists
neat_companies = []
for item in list_of_companies:
    for company in item:
        neat_companies.append(company)

json.dump(neat_companies, all_companies, indent=2)
