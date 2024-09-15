from pathlib import Path
import pandas as pd
import json
import sys
import datetime

def get_file(path:str,file_name:str) -> list[Path]:
    """
    This function takes a path and a file name, than return a list with the files with the same name.
    If the path is not vaild it throw NotADirectoryError error 
    Parameters:
        - path (str) : The absolute or relative path to a directory
        - file_name (str) : The name of the file to find
    
    Returns:
        files_list (list[Path]) : list of available files with the name file_name.
    """

    dir = Path(path)
    # check if the path is valid
    if not dir.exists() and not dir.is_dir():
        raise NotADirectoryError(f"Did not find a real directory at '{str(dir.absolute())}'")
    
    # traverse thorw the path and find all files with 'file_name' name in all sub directory
    files= dir.rglob(file_name)
    # trun them to a list
    files_list = [i for i in files]
    
    return files_list

def get_requirements(path:str)-> list[dict]:
    """
    This function takes a path, fetches all 'requirements.txt', than trun them to a list of dict.
    Parameters:
        - path (str) : The absolute or relative path to a directory
    
    Returns:
        data (list[dict]) : list of all the data in the 'requirements.txt' files in 'path'
    """
    files = get_file(path,"requirements.txt")
    #last_check = str(datetime.datetime.now())
    data = []
    for file in files: 
        text = file.read_text().split("\n")
        for line in text:
            if line == "":
                continue
            name,version = line.split("==") # the format is <name>==<verison>
            data.append({"name":name, "version":version,"type":"pip","path":str(file.absolute())})
    return data


def get_package(path:str)-> list[dict]:
    """
    This function takes a path, fetches all 'package.json', than trun them to a list of dict.
    Parameters:
        - path (str) : The absolute or relative path to a directory
    
    Returns:
        data (list[dict]) : list of all the data in the 'package.json' files in 'path'
    """

    files = get_file(path,"package.json")
    data = []
    #last_check = str(datetime.datetime.now())

    for file in files:
        text = json.loads(file.read_text())
        dependencies = {}
        if "dependencies" in text:
            dependencies.update(text["dependencies"])
        if "devDependencies" in text:
            dependencies.update(text["devDependencies"])
        for d in dependencies:
            data.append({"name":d, "version":dependencies[d],"type":"npm","path":str(file.absolute())})
    return data
def get_package_lock(path:str)-> list[dict]:
    """
    This function takes a path, fetches all 'package-lock.json', than trun them to a list of dict.
    Parameters:
        - path (str) : The absolute or relative path to a directory
    
    Returns:
        data (list[dict]) : list of all the data in the 'package.json' files in 'path'
    """

    files = get_file(path,"package-lock.json")
    data = []
    

    for file in files:
        text = json.loads(file.read_text())
        dependencies = {}
        packages = text["packages"]
        for package in packages:
            # check if the package name is "" (which mean its the pacakge.json dependencies) and skip it so we dont get duplicets
            if  package == "" or"dependencies" not in packages[package]:
                continue
            current_dependencies =packages[package]["dependencies"]
            for dependency in current_dependencies:
                # If dependency allready exists than take the one with the latest version 
                if dependency in dependencies:
                    # The dependencies has the same format("^version") so we can use max() 
                    dependencies[dependency] = max(dependencies[dependency],current_dependencies[dependency])
                else:
                    dependencies[dependency] = current_dependencies[dependency]
        for d in dependencies:
            # Set the type for indirect dependencies to "npm", can also have a unique type like "npm-i".
            # We can know if dependency is indirect by checking if the version starts with '^'.
            data.append({"name":d, "version":dependencies[d],"type":"npm","path":str(file.absolute())}) 
    return data

def create_files(path:str,dest:str = Path.cwd(),indirect:bool = True) -> None:
    """
    This function create 'sbom.csv' and 'sbom.json' files given a 'path' to the repositories directory.
    Parameters:
        - path (str) : The absolute or relative path to a directory
        - dest (str) : The path to a directory where SBOM files are saved. Default set to the current directory
    """
    # getting the data
    req_data = get_requirements(path)
    pack_data = get_package(path)
    pack_lock_data = []
    if indirect:
        pack_lock_data = get_package_lock(path)

    data = req_data+pack_data+pack_lock_data
    if len(data) == 0:
        print(f"No data found at '{str(Path(path).absolute())}'")
        return
    # trun them to a dataframe so it can easily be trun into csv file 
    df = pd.DataFrame(data)
    dest_dir = Path(dest)
    # check if dest_dir is valid
    if not dest_dir.exists() and not dest_dir.is_dir():
        raise NotADirectoryError(f"Did not find a real directory at '{str(dest_dir.absolute())}'")

    # creating csv
    csv_file = Path(dest).joinpath("sbom.csv")
    csv_file.write_text(df.to_csv(index_label= False,index=False),newline="")
    print(f"Saved SBOM in CSV format at '{dest_dir}'")
    data = {"timestamp": str(datetime.datetime.now()),"content":data}
    # creating json
    json_file = Path(dest).joinpath("sbom.json")
    json_file.write_text(json.dumps(data,indent=4),newline="")
    print(f"Saved SBOM in JSON format at '{dest_dir}'")


if __name__ == "__main__":
    args = sys.argv
    # change to True if you want indirect dependencies
    indirect = False
    
    length = len(args)
    if length == 1:
        create_files(str(Path.cwd()),indirect=indirect)
    elif length == 2:
        create_files(args[1],indirect=indirect)
    elif length == 3:
        create_files(args[1],args[2],indirect=indirect)
    else:
        print("""Usage:
    python SBOM.py <source_path> <dest_path>
        source_path: The path to the git repositories directory. Default set to the current directory
        dest_path: The path to a directory where SBOM files are saved. Default set to the current directory""")
    
