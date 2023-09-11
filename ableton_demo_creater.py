import os
import glob
import shutil
import subprocess

# Path to the folder containing WAV files
convert_folder = "C:\\Users\\calvi\\Documents\\Ableton\\User Library\\Sets\\_auto-convert"
# Path to the demo folder where the converted MP3 files will be moved
demo_folder = "C:\\Users\\calvi\Documents\\Ableton\\User Library\\Demos"

# Create the demo_folder if it does not exist
os.makedirs(demo_folder, exist_ok=True)

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

# Move MP3 files to demo_folder
for mp3_file in glob.glob(os.path.join(convert_folder, '*.mp3')):
    shutil.move(mp3_file, demo_folder)

# Open demo_folder
if os.name == 'nt':  # Windows
    subprocess.run(f'explorer {demo_folder}', shell=True)
elif os.name == 'posix':  # macOS and Linux
    subprocess.run(f'open {demo_folder}', shell=True)
