from env_var import liongard_controller

def filtered_systems():
    '''
    filtered_systems gives back all the systems of given inspector ID's
                    for now it only gives back sentinel one, n-able rmm, and
                    n-able backups(cove) systems we have for all of our clients.
                    if we need more report data later on from various inspector
                    we can always add more return objects. 
    '''
    # grabbing all current systems 
    all_systems = liongard_controller.get_systems()

    sentinel_one_systems = []
    rmm_systems = []
    cove_systems = []
    for system in all_systems:
        if system['Inspector']['ID'] == 70:
            sentinel_one_systems.append(system)
        elif system['Inspector']['ID'] == 87:
            rmm_systems.append(system)
        elif system['Inspector']['ID'] == 76:
            cove_systems.append(system)

    return sentinel_one_systems, rmm_systems, cove_systems
