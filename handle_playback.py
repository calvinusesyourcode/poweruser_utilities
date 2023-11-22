import subprocess

def play_video(video_path:str):
    subprocess.run(f'vlc "{video_path}"', shell=True) # requires vlc.exe available on PATH

play_video('downloads/alcohol_is_worse_than_you_think__andrew_huberman.mp4')