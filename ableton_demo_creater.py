import os
import glob
import shutil
import subprocess

def wav_to_mp3():
    convert_folder = "C:\\Users\\calvi\\Documents\\Ableton\\User Library\\Sets\\_auto-convert"
    demo_export_folder = "C:\\Users\\calvi\Documents\\Ableton\\User Library\\Demos"

    os.makedirs(demo_export_folder, exist_ok=True)

    # Convert WAV to MP3
    for wav_file in glob.glob(os.path.join(convert_folder, '*.wav')):
        print(wav_file)
        mp3_file = os.path.join(convert_folder, os.path.splitext(os.path.basename(wav_file))[0] + '.mp3')
        command = f'ffmpeg -i "{wav_file}" "{mp3_file}"'
        subprocess.run(command, shell=True)
        os.remove(wav_file)

    # Delete all .asd files
    for asd_file in glob.glob(os.path.join(convert_folder, '*.asd')):
        os.remove(asd_file)

    # Move MP3 files to demo_export_folder
    for mp3_file in glob.glob(os.path.join(convert_folder, '*.mp3')):
        shutil.move(mp3_file, demo_export_folder)

    # Open demo_export_folder
    if os.name == 'nt':  # Windows
        subprocess.run(f'explorer {demo_export_folder}', shell=True)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.run(f'open {demo_export_folder}', shell=True)
