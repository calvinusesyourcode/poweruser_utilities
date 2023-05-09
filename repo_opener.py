import subprocess
import inquirer

locations = {"peden-web": "C:\\Users\\calvi\\3D Objects\\peden-v2",
             "audio-tool": "C:\\Users\\calvi\\3D Objects\\audio_file_categorization_tool"}

questions = [
    inquirer.List(
        "project",
        message="",
        choices=["peden-web","audio-tool"],
    ),
]

answers = inquirer.prompt(questions)

vscode = "C:\\Users\\calvi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
folder = locations[answers["project"]]

subprocess.run('"{}" "{}"'.format(vscode,folder), shell=True)
