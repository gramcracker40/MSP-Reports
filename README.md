---

# MSP Report - Automating Liongard Data Flow into Connectwise Configurations

This project is a backend service that extracts a predefined set of metrics from specific system types in Liongard, specifically N-Able RMM, Sentinel One, and N-Able backups (Cove). It matches Liongard environments with Connectwise company IDs and updates the reports accordingly.

## Functionality Overview
1. Retrieves systems from Liongard.
2. Queries each system for metrics defined in `env_var.py`.
3. Matches Liongard environments to their system's compiled data.
4. Posts data to the corresponding Connectwise company using a cross-reference JSON file (`lg_env_to_cw_companies.json`).

## Customization
- **Changing Target Systems:** Modify `filter_systems.py` and `env_var.py`. Note: `env_var.py` requires understanding the comments within the file for proper configuration.
- **Linking Liongard and Connectwise IDs:** Run `data_controller.py`. It operates in an infinite loop and can be scripted to process multiple accounts from a separate data file.
- **Finding Connectwise Company ID:** Utilize scripts in the utilities folder (`grab_cw_companies.py`, `filter_cw_companies.py`, and `search_cw_companies.py`) for retrieval and filtering of Connectwise company IDs.

## Components
- **runner.py:** Infinite loop for background service to update processes.
- **env_var.py:** Contains all environment variables, including `liongard_controller`, the main object for Liongard API calls.
- **master_metric_table (env_var.py):** Maps variable names of filtered systems to a list of metric IDs for desired data extraction.
- **metric_custom_field_match (env_var.py):** Links Liongard Metric IDs to Connectwise configuration custom field IDs. Requires custom field setup in Connectwise or modification of `update_reports()` for different field handling.

## Running Checks
To initiate checks, refer to the implementation in `runner.py`.

---
