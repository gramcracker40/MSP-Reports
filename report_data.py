from env_var import liongard_controller, master_metric_table

def get_systems_data(systems, metric_ID):
    '''
    systems = a given set of systems returned by filtered_systems
    metric_ID = list of metric id's to pull back from the specific system type you pass through

    This function will retrieve the neccessary metrics from each of the systems returned from filter_systems
     and filters it into one single dictionary thats keys are the systemID's originally passed through. metric_ID will
     be a list of various metric_IDs you can pass through to the function for it to go and retrieve the data
     from each of them systems. Visit
    '''
    systems_to_query = []
    data = {}
    if type(systems) == list:
        for count, system in enumerate(systems):
            systems_to_query.append(system["ID"])

            if (count % 10 == 0) or count == len(systems) - 1:
                temp_data = liongard_controller.get_metric_data(
                    systemID=systems_to_query, metricID=metric_ID)
                
                try:
                    for system in systems_to_query:
                        data[str(system)] = temp_data[str(system)]
                except KeyError:
                    if not temp_data:
                        print("""get_systems_data(): No data was returned from LiongardAPI.get_metric_data()
                                please check the metric_ID passed through and ensure
                                they are for the systems passed through""")
                    else:
                        print("Please ensure you have passed through valid systems and metric_ID")

                systems_to_query.clear()
    elif type(systems) == int:  
        data = liongard_controller.get_metric_data(
                    systemID=systems, metricID=metric_ID)
    else:
        print("type(system): invalid, please pass through an int, or list of ints")

    return data

def get_all_systems_data(all_systems_data, metric_table):
    '''
    all_systems_data = list of the individual systems_data
    metric_id_dict = name of the "systems_data" ex:{
        "s1_systems_data": [2416, 2290, 2385, 2206],
        "rmm_systems_data": [2400, 2401, 2394, 2395, 2396, 2397, 1723, 1724], 
        "cove_systems_data": [2417, 1409, 1394, 1395]
    }
    '''
    # goes through all_systems_data and grabs the individual variables name and contents to pass
    # to filtered_data

    filtered_data = {}
    for count, system in enumerate(all_systems_data):
        # grabbing the filtered_data var name to use as key in metric_table
        # print(all_systems_data[count][0])
     
        var_name = ""
        #enumerating master_metric_table to find the current variable name
        for count_lower, key in enumerate(master_metric_table):
            if count_lower == count:
                var_name = key
        
        # grabs the matching variable name for the reference variable wihtin the global scope
        #var_name = [ i for i, j in globals().items() if j == all_systems_data[count]][0] #[0]
        # adding each individual systems data to filtered_data
        data = get_systems_data(system, metric_table[var_name])
        for system in data:
            filtered_data[system] = data[system]

    return filtered_data


def match_systems_and_environments(system_data, systems):
    '''
    matches all systems to their proper environment with the environment
    name as the key. In env_var, there is a json template that matches the
    liongard environment name to the appropriate CW key. To add a report you
    must give the exact name of the liongard environment, and a key to the CW
    company in the Connectwise API for manage. 

    '''
    
    matched = {}
    for system in system_data:
        for count, index in enumerate(systems):
            # print(f"system[count]: {systems[count]}")
            for each in systems[count]:
                # print(f"each: {each}")
                if int(each['ID']) == int(system):
                    matched[each['Environment']['Name']] = system_data[system]

    matched_systems = {}
    for env in matched:
        matched_systems[env] = {}
        #print(env)
        for metric_id in matched[env]:
            #p#rint(metric_id)
            matched_systems[env][metric_id] = matched[env][metric_id]["Metric"]["value"]
    
    return matched_systems
