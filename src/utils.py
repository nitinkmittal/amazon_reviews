from pickle import load, dump, HIGHEST_PROTOCOL
from os import mkdir


def dump_pickle(obj, filename : str):
    """Save object in Python pickle form."""
    dump(obj, open(f"{filename}.pickle", "wb"),
                   protocol=HIGHEST_PROTOCOL)
    
def load_pickle(filename : str):
    """Load Python pickle.""" 
    if ".pickle" in filename:
        filename = filename.replace(".pickle","")
    return load(open(f"{filename}.pickle", "rb"))

def create_dir(folder_name : str):
    """
    Create folder if not already exists.
    
    Assumes folder path is appropriately attached to folder_name.
    """
    try:
        mkdir(folder_name)
    except Exception as e:
        print(f"Failed creating directory, exception : {e}")
    else:
        print("Successfully created directory")