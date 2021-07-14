from cls import *

path_to_bundle = get_path()
list_of_bundles = get_archives(path_to_bundle)
nu = select_bundle(list_of_bundles)
if nu == 0:
    for bundle in list_of_bundles:
        newbundle = Bundle(path_to_bundle, bundle)
        worker(newbundle)
else:
    newbundle = Bundle (path_to_bundle, list_of_bundles[nu-1])
    worker(newbundle)





