import subprocess, os
from pathlib import Path

vscode_location = "C:\\Users\\calvi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
projects_location = "C:\\Users\\calvi\\3D Objects"

def open_with_vscode(path):
    vscode = Path(vscode_location)
    subprocess.run('"{}" "{}"'.format(vscode, path), shell=True)

with open(Path(os.getcwd()+"/repo_opener_projects.txt"),"r") as f:
    repo_locations = {}
    for line in f.readlines():
        line = line.strip()
        i = line.index(":")
        repo_locations[line[:i]] = line[i+2:]
    print(repo_locations)
