from pathlib import Path
import pandas as pd

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

    if not dir.exists():
        raise NotADirectoryError(f"Did not find a real directory at '{path}'")
    
    files= dir.rglob(file_name)
    files_list = [i for i in files]
    
    return files_list

def get_requirements(path:str)-> pd.DataFrame:
    files = get_file(path,"requirements.txt")

    
    data = {"name":[], "version":[],"type":[],"path":[]}
    for file in files: 
        text =file.read_text().split("\n")
        for line in text:
            if line == "":
                continue
            name,version = line.split("==") # the format is <name>==<verison>
            data["name"].append(name)
            data["version"].append(version)
            data["type"].append("pip")
            data["path"].append(file.absolute())
    df = pd.DataFrame(data)
    return df


def get_package(path:str):
    return get_file(path,"package.json")

def create_csv(path:str):
    # TODO get dependencys form package.json
    df =get_requirements(path)
    out_file =  Path("SBOM.csv",)
    out_file.write_text(df.to_csv(index_label= False,index=False),newline="")

if __name__ == "__main__":
    create_csv("test")