# SBOM
SBOM is a Python script used to fetch dependencies form one or many git repositories in a directory.
## Description
The script goes throw all "requirements.txt" and "package.json" files then finds all the dependencies and saves them by thier name, verison, type and path. 

The script can also fetch **indirect dependencies** from "package-lock.json" files but needs to be toggled on ( see [How to Use](#how-to-use)
).
## Getting Started

### Libraries Used
* **pathlib**: Used for finding and creating files
* **pandas**: Use to create DataFrame
* **json**: Used to serialize and deserialize json
* **sys**: Use to get "argv"
* **datetime**: Used to get time

### Installing
* Clone the repository with:
```bash
git clone https://github.com/Bahaagh3/SBOM.git
```
### How To Use
To use SBOM run `SBOM.py` with these arguments:
```
python SBOM.py <source_path> <dest_path>
```
* *source_path*: The path to the git repositories directory. Default set to the current directory
* *dest_path*: The path to a directory where SBOM files are saved. Default set to the current directory

By calling `SBOM.py` this will create 2 files `sbom.csv` and `sbom.json` that contains the dependencies.

You can also fetch all **indirect dependencies** by changing the value in `SBOM.py` line 152 to True (default set to False):
```python
    indirect = True
```
## The Formats 
Both files almost have the same format, which is:
| name    | version | type    | path |
| -------- | ------- | -------- | ------- |
| Name of the dependency  | Version of the dependency | Either `pip` or `npm`  | The absolute path where dependency was found |

### sbom.csv
```csv
name,version,type,path
@emotion/react,11.13.0,npm,C:\Users\example\SBOM\package.json
```
### sbom.json
The json file contains an extra attribute `timestamp` which shows when the script ran.
```javascript
{
    "timestamp": "2024-09-15 14:01:03.187000",
    "content": [
        {
            "name": "@emotion/react",
            "version": "11.13.0",
            "type": "npm",
            "path": "C:\\Users\\example\\SBOM\\package.json"
        },
        {
            "name": "picocolors",
            "version": "^1.0.0",
            "type": "npm",
            "path": "C:\\Users\\example\\SBOM\\package-lock.json"
        },
        ...
    ]
}
```

## Authors
* Bahaa Aldeen Ghazal (bahaaghazal2003@gmail.com)
