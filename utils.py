import os
import zipfile
import platform
import datetime


def get_archives(path):
    list_of_archives = []
    for file in os.listdir(path):
        if file.endswith(".zip"):
            list_of_archives.append(file)
    return list_of_archives


def get_path():
    print("Please provide path to log bundle (zip archive) directory")
    path_to_bundle = input()
    if os.path.exists(path_to_bundle):
        return path_to_bundle
    else:
        print("Path does not exists")
        path_to_bundle = get_path()
        return path_to_bundle


def select_bundle(list_of_archives):
    print("select the bundle you want to parse. type '0' to parse all bundles \n type 9999 to exit")
    order = 0
    for archive in list_of_archives:
        order += 1
        print(archive + '- {}'.format(order))
    nu = input()
    try:
        nu = int(nu)
    except:
        print("not a number. please try again")
        nu = select_bundle(list_of_archives)
        nu = int(nu)
        return nu
    if nu == 0:
        return 0
    if nu <= len(list_of_archives):
        return nu
    if nu == 9999:
        quit()
    else:
        print("number not in the list - please try again")
        nu = select_bundle(list_of_archives)
        nu = int(nu)
        return nu


def worker(Bundle):
    if Bundle.name_controller():
        Bundle.extract_log()
    else:
        print("The archive " + Bundle.name + " is not a Veeam log bundle")


def path_OS_platform(Bundle):
    if platform.system() == "Windows":
        filename = os.path.abspath(Bundle.path + '\\' + Bundle.name)
        filename = filename.replace('\\', os.path.sep)
    else:
        filename = Bundle.path + '/' + Bundle.name
    return filename


def check_job(logs_list):
    for file in logs_list:
        if '.html' in file:
            job_name = file[:-5]
    if job_name is None:
        print("bundle collected for server not a Job or is incomplete. Please provide the Job name")
        job_name = input()
    return job_name


def get_latest_log(job_name, logs_list):
    latest_job_log = ""
    log_name_like = "Job." + job_name + ".Backup.log"
    for file in logs_list:
        if log_name_like in file:
            latest_job_log = file
    return latest_job_log


def get_latest_error(bundle_zipfile, list_of_errors, job_log):
    with bundle_zipfile.open(job_log) as myfile:
        for line in myfile:
            line = line.decode("utf-8")
            if "Error" in line:
                if list_of_errors:
                    line = line.strip('\n')
                    time_stamp = datetime.datetime.strptime(list_of_errors[0][1:20], '%d.%m.%Y %H:%M:%S')
                    new_time_stamp = datetime.datetime.strptime(line[1:20], '%d.%m.%Y %H:%M:%S')
                    if time_stamp.time() < new_time_stamp.time():
                        list_of_errors = []
                        list_of_errors.append(line)
                    if time_stamp.time() == new_time_stamp.time():
                        list_of_errors.append(line)
                else:
                    list_of_errors.append(line)
    return list_of_errors


def get_version(bundle_zipfile, job_log):
    with bundle_zipfile.open(job_log) as myfile:
        time_stamp = datetime.datetime.strptime('1/1/1901 1:00:00', '%d/%m/%Y %H:%M:%S')
        for line in myfile:
            line = line.decode("utf-8")
            if "Module: [C:\Program Files\Veeam\Backup and Replication\Backup\Veeam.Backup.Manager.exe" in line:
                version = line[104:115]
                version = version.strip(']')
            if "Process start time:" in line:
                old_time_stamp = time_stamp
                time_stamp = datetime.datetime.strptime(line[21:37], '%d/%m/%Y %H:%M:%S')
                if time_stamp > old_time_stamp:
                    new_version = version
        if new_version is None:
            print ("The modules version is not found. Please try another log.")
    return new_version
