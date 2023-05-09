import subprocess, inquirer, os, time
from pathlib import Path
from sharing_is_caring import repo_locations, open_with_vscode, projects_location, github_username

questions = [
    inquirer.List(
        "project",
        message="",
        choices=list(repo_locations.keys()),
    ),
]

answers = inquirer.prompt(questions)

folder = Path(projects_location+"/"+repo_locations[answers["project"]])

if os.path.exists(folder):
    open_with_vscode(folder)
else:
    os.chdir(projects_location)
    repo = "https://github.com/"+github_username+"/"+repo_locations[answers["project"]]
    subprocess.run('git clone "{}"'.format(repo), shell=True)
    time.sleep(2)
    open_with_vscode(folder)