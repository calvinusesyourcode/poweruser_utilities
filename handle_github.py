import socket, os, subprocess
from yaml import safe_load
from pathlib import Path

def auto_pull(config):
    repo_folder = config["repo_folder"]
    repos_to_pull = config["startup"]["repos_to_pull"]
    for repo in repos_to_pull:
        os.chdir(os.path.join(repo_folder, repo))
        stdout, stderr = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(f"{repo}: ", (stderr if stderr else stdout).decode("utf-8").replace("\n", ""))

def auto_push(config):
    repo_folder = config["repo_folder"]
    repos_to_push = config["shutdown"]["repos_to_push"]
    for repo in repos_to_push:
        os.chdir(os.path.join(repo_folder, repo))
        stdout, stderr = subprocess.Popen(["git", "add", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        # print(f"{repo}: ", (stderr if stderr else stdout).decode("utf-8").replace("\n", "\n    "), sep="\n    ")
        stdout, stderr = subprocess.Popen(["git", "commit", "-m", "auto commit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(f"{repo}: ", (stderr if stderr else stdout).decode("utf-8").replace("\n", "\n    "), sep="\n    ")
        stdout, stderr = subprocess.Popen(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(f"{repo}: ", (stderr if stderr else stdout).decode("utf-8").replace("\n", "\n    "), sep="\n    ")