from pathlib import Path
def get_file(path:str,file_name:str) -> list[Path]:
    """
    This function takes a path and return a list of requirements.txt and package.json files.
    If the path is not vaild it throw NotADirectoryError error 
    Parameters:
        - path (str) : The absolute path to a directory
        - file_name (str) : The name of the file to find
    
    Returns:
        files_list (list[Path]) :list of available requirements.txt and package.json files.
    """
    dir = Path(path)
    if not dir.exists():
        raise NotADirectoryError(f"Did not find a real directory at '{path}'")
    files= dir.rglob(file_name)
    files_list = [i for i in files]
    return files_list

if __name__ == "__main__":
    print(get_file("test","requirements.txt"))