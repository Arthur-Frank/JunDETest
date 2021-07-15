# Here a concept of other possible information can be extracted from Logs
# I will use the same logic as in the parent Script:
#     - reading the  file line by line and running analyze methods against each of them
#     - differnt methods needed to scale the main method easily, e.g. if some additional data need to be extracted
#     from the Log or the same search can be run against another log file
#     - result will be associated with some variable that will be written to a result file

import os
import datetime

# method reads log line by line and apply parsing func to each of them. Results put into a dict
def get_parsing_result (bundle_zipfile,job_log ):
    #dictionary with results of parsing
    #dictioanry has a key - variable of the result to process and value - lines from Log file to write to result .txt
    result_dictionary = {}
    with bundle_zipfile.open(job_log) as myfile:
        for line in myfile:
            line = line.decode("utf-8")
            result_dictionary.update({'hypervisor is ':hypervisor_detector(line)})
    return result_dictionary

# get result from dictionary and creates and writes into result file in format "Key\nVal\n\n"
# dict_with_result - dictionary with parser results
# target_path - where to save result file
# job_name - name of the processed Job
def result_file (target_path, job_name, dict_with_result):
    with open(os.path.join(target_path, job_name + ".txt"), 'w+') as temp_file:
        for key, val in dict_with_result.items():
            temp_file.write(key + '\n')
            temp_file.write(val + '\n\n')
    return temp_file


#get hypervisor info from logs
def hypervisor_detector(line):
    if "Job Type" in line:
        if line[51:62] == "VDDK Backup":
            hypervisor = "VMware"
        else:
            hypervisor = "Hyper-V"
    return hypervisor


