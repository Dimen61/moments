import os

def get_all_files(folder_path):
   return [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
           if os.path.isfile(os.path.join(folder_path, f))]

def get_file_prefix_and_suffix(file_path):
    """Return ({prefix}, {suffix}) 
    "{prefix}{suffix}" constructs file name which suffix begains with '.'
    """
    _, file_name = os.path.split(file_path)
    prefix, suffix = os.path.splitext(file_name)
    return (prefix, suffix)



