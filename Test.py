#unit tests for Classes methods

import unittest
from cls import Bundle, Log
import os

# etalon output for parsing methods in the Script for 2021-07-07T161552_VeeamBackupLogs.zip from the test task
# The Zip must be in teh working directory of the Script
etalon_list = ['Veeam version from the Job log: 10.0.1.4854\n', '\n', 'The last error stacktrace:\n', '[07.07.2021 16:08:39] <01> Error    [SimplePointGenerationPolicy] Transform failed\n', '[07.07.2021 16:08:39] <01> Error    Operation was canceled by user LISA-VBRSQL\\Administrator (Veeam.Backup.Common.CStopSessionException)\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CStopSessionControl.CheckStoped()\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CMultiStopSessionSync.CheckStoped()\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CLocalBackupPointGenerationPolicy.CheckIsSessionStoppedOrStopAfterCurrent()\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CLocalBackupPointGenerationPolicy.TransformSafe()\n', '[07.07.2021 16:08:39] <01> Error    Operation was canceled by user LISA-VBRSQL\\Administrator (Veeam.Backup.Common.CStopSessionException)\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CStopSessionControl.CheckStoped()\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CMultiStopSessionSync.CheckStoped()\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CLocalBackupPointGenerationPolicy.CheckIsSessionStoppedOrStopAfterCurrent()\n', '[07.07.2021 16:08:39] <01> Error       at Veeam.Backup.Core.CLocalBackupPointGenerationPolicy.TransformSafe()\n', '[07.07.2021 16:08:39] <01> Error    [RetentionAlgorithm] Retain storages skipped: session is stopping\n']

# opens and reads teh result file. Writes it content to a list line by line
def checking_file(file):
    filecontent_check_list = []
    with open (file.name, 'r') as tempfile:
        for line in tempfile:
            filecontent_check_list.append(line)
    return filecontent_check_list


class TestBundle(unittest.TestCase):
    def setUp(self):
        self.bundle = Bundle (os.getcwd(), '2021-07-07T161552_VeeamBackupLogs.zip')
    def test_correct_name_controller(self):
        self.assertEqual(self.bundle.name_controller(),True)
    def test_incorrect_name(self):
        self.bundle.name= '01010SOmeotherarchive.zip'
        self.assertEqual(self.bundle.name_controller(), False)
    def test_parsing(self):
        self.assertEqual(checking_file(self.bundle.extract_log()), etalon_list)
        os.remove('TinyVM_backup.txt')


# Log class was not tested as it is called inside extract_log method in the Bundle class.
# Possible needs to be improved in future to split a big extract_log method of the Bundle class


if __name__ == '__main__':
    unittest.main()
