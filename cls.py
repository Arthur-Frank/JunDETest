from utils import *

# Bundle is a class as it can have more function in future to process the bundle
class Bundle:

    #the Bundle has a path (directory it is located in) and the name (with .zip extension)
    def __init__(self, path, name):
        self.path = path
        self.name = name

    # method returns bool after checking if the Bundle name from provided directory has an appropriate Veeam log format
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

    # method reads and processes log from the zip file
    # the log is a new instance of the Log class. Parser runs inside this method, however,
    # it can be easily refactored to be processed by an additional method or be started from the main.py
    def extract_log(self):
        path_to_zip = path_OS_platform(self)
        bundle = zipfile.ZipFile(path_to_zip, 'r')
        archived_files_list = bundle.namelist()
        job_name = check_job(archived_files_list)
        print("the Job name is " + job_name)
        latest_job_log = get_latest_log(job_name, archived_files_list)
        # func can extarct log from the zip in case it needs in future
        #bundle.extract(latest_job_log, Bundle.path)
        log = Log(latest_job_log, self.path)
        file = log.parse_log(bundle, job_name)
        return file


#the Log file is a class
# may have more function for scaling
class Log:

    # the Log has a name to be addressed by ZipFile lib methods and path to target directory where
    # to extract it or where to create a file with parsing results
    def __init__(self, job_log, target_path):
        self.job_log = job_log
        self.target_path = target_path

    # the methods run parsing functions against the Log
    # it can be easily scaled with adding new parsing functions
    # in this case needs a new method that will write results to the file to not to paste-copy code
    #
    # once the parsing returns the result - it is written to the result file
    def parse_log(self, bundle_zipfile, job_name):
        list_of_errors= []
        with open (os.path.join(self.target_path, job_name+".txt"), 'w+') as temp_file:
            version = get_version(bundle_zipfile, self.job_log)
            list_of_errors = get_latest_error(bundle_zipfile, list_of_errors, self.job_log)
            temp_file.write("Veeam version from the Job log: " + version +'\n\n')
            temp_file.write("The last error stacktrace:\n")
            for line in list_of_errors:
                # writing lines in Windows adds \n to the file. In Linux need to add new line symbol explicitly
                if platform.system() == "Windows":
                    temp_file.write(line)
                else:
                    temp_file.write(line + "\n")
        return temp_file

