# meant to allow us to search a company by name, whether it be 1-100 characters and
# return a list of companies that have the same string concatenation within it
# ex: searching "Web Fire" will return all companies that start with "web fire".lower()
#       and their CW API companyID
import json
from filter_cw_companies import filter_cw_companies_and_ids

cw_companies = filter_cw_companies_and_ids()

def cw_company_lookup(search_string):
    
    # Pulling dict with CW company name as key and companyID as value
    
    found_companies = {company: cw_companies[company] for company 
        in cw_companies if search_string.lower() in company.lower()}

    return found_companies


while True:
    input_text = input("Please enter a company to search\n")
    test = cw_company_lookup(input_text)
    print(test)


