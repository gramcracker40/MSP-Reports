import json

def filter_cw_companies_and_ids():
    companies_file = open("data/companies_and_IDs_CW.json", "r")
    companies = json.load(companies_file)

    companies_and_ids = {}
    for company in companies:
        companies_and_ids[company["name"]] = company["id"]

    return companies_and_ids


# test = filter_cw_companies_and_ids()
# print(json.dumps(test, indent=2))