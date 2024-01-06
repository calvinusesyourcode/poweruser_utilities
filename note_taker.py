import os, datetime
notes_folder = "notes"

def notes_loop():
    os.makedirs(notes_folder, exist_ok=True)
    if os.name == "nt": os.system("cls"); print("\n")
    session_name = None
    fdate = datetime.datetime.now().strftime("%Y%m%d")
    notes = [f for f in os.listdir(notes_folder) if abs(int(fdate)-int(f[:8])) <= 14]
    for i, note in enumerate(notes): print(f"  ({i}) {note[9:].split('.')[0]}")
    while session_name is None:
        session_name = input("\nsession_name: ")
    session_path = os.path.join(notes_folder, notes[int(session_name)]) if session_name.isdigit() else os.path.join(notes_folder, f"{fdate}-{session_name.replace(' ', '_')}.txt")
    if not os.path.exists(session_path):
        with open(session_path, "w") as f:
            f.write(f"{fdate}\n\n")
    print(f"session_path: {session_path}")
    while True:
        user_input = input("> ")
        if user_input == "exit":
            break
        with open(session_path, "a") as f:
            f.write("\n"+datetime.datetime.now().strftime("%H:%M")+"\n")
            f.write(user_input+"\n")
        # f.close()
    print("exiting...")