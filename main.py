from filter_systems import filtered_systems
from report_data import get_all_systems_data, match_systems_and_environments
from utilities.cw_msp_reports import check_msp_companies_msp_report, update_reports, check_user_entered_IDs
from env_var import master_metric_table

# Checks to ensure data will be stored properly - Ensuring there are "MSP Reports" for each MSP type client
check_msp_companies_msp_report()
check_user_entered_IDs()

# will pull back all of our current Sentinel One, N-Able RMM, and Cove backup inspectors data from our Liongard instance
s1_systems_data, rmm_systems_data, cove_systems_data = filtered_systems()

# grabbing the appropriate metric data from each system and matching it to the environment
all_systems_data = get_all_systems_data([s1_systems_data, rmm_systems_data, cove_systems_data], metric_table=master_metric_table)
matched_data = match_systems_and_environments(all_systems_data, [s1_systems_data, rmm_systems_data, cove_systems_data])

# updating the individual "MSP Reports" based on the lg_env_to_cw_companies.json file
update_reports(matched_data)
