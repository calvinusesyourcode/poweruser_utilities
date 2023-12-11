filename = "C:\\Users\\calvi\\3D Objects\\poweruser_utilities\\downloads\\audio_____the_most_important_2_minutes_of_your_life__david_goggins_motivational_speeches.mp4"
timestamp = "word"
import subprocess
command = f'insanely-fast-whisper --file-name "{filename}" --device-id 0 --language en --timestamp "{timestamp}"'
print(command)
# command = "insanely-fast-whisper --help"
subprocess.run(command, shell=True, check=True)