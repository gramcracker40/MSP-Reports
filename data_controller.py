# This file will be used to make additions during runtime to specific data pieces. 
#   Will be options to check all MSP Reports data, add Environments from Liongard and their
#   respective Connectwise ID's to lg_env_to_cw_companies.json
import json

prompt = int(input("""Please enter the number for the option you are seeking
                          \n0: Quit data_controller
                          \n1: add Liongard environment:Connectwise ID (Use search_cw_companies.py to find correct ID)
                          \n2: """))
                          
#TODO UPDATE THIS FILE TO LG_ENV_TO_CW_COMPANIES CURRENT STRUCTURE
while prompt != 0:

    if prompt == 1:
        # opening the JSON object associating LG env names with CW company id's
        lg_env_cw_id_file = open("lg_env_to_cw_companies.json", "r")
        lg_env_cw_id = json.load(lg_env_cw_id_file)
        
        # grabbing the info to add
        lg_environment = input("Please enter the exact name of the Liongard environment you are adding...")
        cw_id = input("Please enter the Connectwise company ID")
        
        # adding the desired values
        lg_env_cw_id["env_to_id"][lg_environment] = cw_id
        lg_env_cw_id["id_to_env"][cw_id] = lg_environment

        #rewriting the JSON object 
        lg_env_cw_id_file_write = open("lg_env_to_cw_companies.json", "w")
        json.dump(lg_env_cw_id, lg_env_cw_id_file_write)


    prompt = int(input("""Please enter the number for the option you are seeking
                          \n0: Quit data_controller
                          \n1: add Liongard environment:Connectwise ID
                          \n2: """))