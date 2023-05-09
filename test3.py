# user variables
main_dir = "C:\\Users\\calvi\\3D Objects\\" # where you keep your python projects
test_dir = "C:\\Users\\calvi\\3D Objects\\test\\" # where you keep your test folder
shorthand = { # for "project_name"
    "util": "poweruser_utilities"
}
# script
import os, shutil, time

def ask(str):
    return input("\n"+str+": ")

def clear():
    os.system("cls")

unsatisfied = True
while unsatisfied:
    clear()
    file_ext = ask("file_ext")
    original = ask("test_file")
    project = ask("project_name")
    copy = ask("file_new")
    clear()
    file_ext = ".py" if file_ext == "" else "."+file_ext
    print("\n{}{} > {}/{}{}".format(original,file_ext,project,copy,file_ext))
    if ask("satisfied? ") in ["y", "o"]:
        unsatisfied = False

if project in list(shorthand.keys()):
    project = shorthand[project]

initial = test_dir+original+file_ext
new_dir = main_dir+project
target = new_dir+"\\"+copy+file_ext

try:
    os.mkdir(new_dir)
except:
    pass
shutil.copyfile(initial, target)
while os.stat(initial).st_size != os.stat(target).st_size:
    time.sleep(0.100)
os.remove(initial)

input("press enter to exit")