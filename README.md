# MSP Report --- Automating Liongard data flow into Connectwise configurations
This project is a back end service that simply grabs a pre defined set of metrics from
a few specific types of systems in Liongard. At the time of writing, this only supports
N-Able RMM, Sentinel One, and N-Able backups (Cove). It will first go and grab all systems of these
three types from Liongard, and then it will query each system for the defined set of metrics
located in env_var.py. Once it has obtained all of the data, it will go out and match 
the environments to their systems compiled data. To post the data to the correct CW company
there is a cross reference JSON file named lg_env_to_cw_companies.json. Reading the file
will give insight to its uses. When given a liongard environment name, it will match it to
the corresponding Connectwise company ID and vice versa. This assists when taking the matched
data and running it through the update_reports function. You could also allow a user to specify this
in their individualized configuration of the script. 

Reading main will answer most questions about the functionality of the program. 

## To change what systems you are gathering data for
You will need to make changes in filter_systems.py and env_var.py
filter_systems.py is hard coded but changing the env_var.py file
will require you to read the env_var.py comments and figure out
what is truly going on

## Linking Liongard environments and Connectwise company ID's
simply run data_controller.py, it will handle the additions to 
lg_env_cw_companies.json, It will run in a infinite while loop when ran, so
you could write a script that feeds in multiple account names from a seperate
data file 

## How do I find the CW company ID?
I added a few scripts I wrote into the utilities folder called grab, filter, and 
search_cw_companies. grab will go and get all of your CW companies and dump a list
of CW company JSON objects into data/companies_and_IDs. filter will sort through this JSON
and grab the name and companyID. Once you have run grab_cw_companies.py, you can simply run 
search_cw_companies.py to grab a CW company ID. 

## How do I get this to run checks?
In the runner.py file I have a very simple implementation of a check and run scenario. 
Main is the update process. 

## What is env_var.py???
env_var.py is the holder of all environment variables. Meaning, any commonly used variable 
in the package is there. The "liongard_controller" is in this file as well and is the main 
object for making calls to Liongard. 

## What is master_metric_table in env_var.py
Master metric table holds the var name of the filtered systems as keys and the
corresponding list of integers form metricIDs for the metrics I am wanting to pull
from each individual type of system.

## What is metric_custom_field_match in env_var.py?
This simply matches the Liongard Metric IDs to a Connectwise configuration custom field ID's
if you do not setup custom fields for connectwise configurations you will have to specify the
fields in your own manner within update_reports(), complete rework will be needed for how the 
function adds the fields to the body sent in the put request.


