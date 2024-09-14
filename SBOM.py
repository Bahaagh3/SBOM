from pathlib import Path
import pandas as pd
import json
import sys
def get_file(path:str,file_name:str) -> list[Path]:
    """
    This function takes a path and a file name, than return a list with the files with the same name.
    If the path is not vaild it throw NotADirectoryError error 
    Parameters:
        - path (str) : The absolute or relative path to a directory
        - file_name (str) : The name of the file to find
    
    Returns:
        files_list (list[Path]) :list of available files with the name file_name.
    """

    dir = Path(path)

    if not dir.exists() and not dir.is_dir():
        raise NotADirectoryError(f"Did not find a real directory at '{path}'")
    
    files= dir.rglob(file_name)
    files_list = [i for i in files]
    
    return files_list

def get_requirements(path:str)-> list[dict]:
    files = get_file(path,"requirements.txt")

    
    data = []
    for file in files: 
        text =file.read_text().split("\n")
        for line in text:
            if line == "":
                continue
            name,version = line.split("==") # the format is <name>==<verison>
            data.append({"name":name, "version":version,"type":"pip","path":str(file.absolute())})
    return data


def get_package(path:str):

    files = get_file(path,"package.json")
    data = []

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

def create_files(path:str,dest:str= Path.cwd()):
    # creating csv
    req_data = get_requirements(path)
    pack_data = get_package(path)
    data = req_data+pack_data
    df = pd.DataFrame(data)
    dest_dir = Path(dest)
    if not dest_dir.exists() and not dest_dir.is_dir():
        raise NotADirectoryError(f"Did not find a real directory at '{dest_dir}'")

    csv_file = Path(dest).joinpath("SBOM.csv")
    csv_file.write_text(df.to_csv(index_label= False,index=False),newline="")
    print(f"Saved SBOM in CSV format at '{dest_dir}'")

    # creating json

    json_file = Path(dest).joinpath("SBOM.json")

    json_file.write_text(json.dumps(data,indent=4),newline="")
    print(f"Saved SBOM in JSON format at '{dest_dir}'")


if __name__ == "__main__":
    args = sys.argv
    length = len(args)
    if length == 1:
        create_files(str(Path.cwd()))
    elif length == 2:
        create_files(args[1])
    elif length == 3:
        create_files(args[1],args[2])
    else:
        print("""Usage:
    python SBOM.py <source_path> <dest_path>
        source_path: The path to the git repositories directory. Default set to the current directory
        dest_path: The path to a directory where SBOM files are saved. Default set to the current directory""")
    
