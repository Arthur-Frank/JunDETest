from utils import *

#if_github update

class Bundle:

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def name_controller(self):
        counter = 0
        if "VeeamBackupLogs" in self.name:
            for nu in self.name[:10].split('-'):
                if nu.isdigit():
                    counter += 1
                else:
                    break
        if counter == 3:
            return True
        else:
            return False

    def extract_log(self):
        path_to_zip = path_OS_platform(self)
        bundle = zipfile.ZipFile(path_to_zip, 'r')
        logs_list = bundle.namelist()
        job_name = check_job(logs_list)
        print("the Job name is " + job_name)
        latest_job_log = get_latest_log(job_name, logs_list)
        #bundle.extract(latest_job_log, Bundle.path)
        log = Log(latest_job_log, self.path)
        file = log.parse_log(bundle, job_name)
        return file


class Log:

    def __init__(self, job_log, target_path):
        self.job_log = job_log
        self.target_path = target_path

    def parse_log(self, bundle_zipfile, job_name):
        list_of_errors= []
        with open (os.path.join(self.target_path, job_name+".txt"), 'w+') as temp_file:
            version = get_version(bundle_zipfile, self.job_log)
            list_of_errors = get_latest_error(bundle_zipfile, list_of_errors, self.job_log)
            temp_file.write("Veeam version from the Job log: " + version +'\n\n')
            temp_file.write("The last error stacktrace:\n")
            for line in list_of_errors:
                temp_file.write(line + "\n")
        return temp_file

