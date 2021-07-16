The Script parses logs in the Veeam Bundle and creates a .txt file with the result for each processed Job

To run the script on Windows or Linux clone the project to some local directory. There is no need to preinstall any
libraries - Script uses default pythons libs installed with python.

To run it on Linux execute the following command from the directory where you clone the Project
(by default ''/home/user/project'):

python3 main.py


On Windows navigate to the directory you clone the Project (by default 'C:\users\username\project') double-click on
the "main.py" file or execute it in CMD with the command from the project directory:

main.py


The script will ask to provide a path to the directory with Log Bundles.
The script will get all .zip files from the provided directory and request the archive to process.
You may select an exact file or process all bundles.
The script looks for the LATEST JOB log and extracts the Veeam version from the last run and last error stack.
Data returned as a .txt file has the name of parsed Job and is located under the directory with log bundles.


In the Algorithm_task.py file, a concept of other data can be extracted from the Job log.


Test.py contains unit tests for the Bundle class. Checks cases with the correct and incorrect names of the Veeam log
bundle in the directory. Tests the main parser method from the Bundle class - extract_log. Creates a result txt file
from the Log bundle provided with project 2021-07-07T161552_VeeamBackupLogs.zip - compares contain this file with
a default list.
To run tests execute the Test.py file from the project directory.