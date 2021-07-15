# file to execute

from cls import *

# takes path to dircetory with .zip log bundles from user input
path_to_bundle = get_path()
# creates list of .zip files in the provided directory
list_of_bundles = get_archives(path_to_bundle)
# returns the number of file from directory needs to be processed as a Log bundle
nu = select_bundle(list_of_bundles)
# checkes if the user prefers to process all bundles from archive or a one
if nu == 0:
    for bundle in list_of_bundles:
        newbundle = Bundle(path_to_bundle, bundle)
        worker(newbundle)
else:
    newbundle = Bundle (path_to_bundle, list_of_bundles[nu-1])
    worker(newbundle)

input("Press any key to quit")






