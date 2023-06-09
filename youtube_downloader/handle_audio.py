import os, openai, subprocess, pathlib, math, datetime, json
from pathlib import Path

def audio_mp4_to_mp3(folder, filename: str):
    """Convert an mp4 audio file to mp3."""
    
    file_stem = Path(filename).stem
    mp4 = str(Path(folder, file_stem + ".mp4"))
    mp3 = str(Path(folder, file_stem + ".mp3"))
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', mp4]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    info = json.loads(result.stdout)

    # Extract the audio codec and sample rate from the info
    audio_info = [stream for stream in info['streams']][0]
    sample_rate = audio_info['sample_rate']

    command = ['ffmpeg', '-i', mp4, '-codec:a', 'libmp3lame', '-ar', sample_rate, mp3]

    print(" ".join(command))
    result = subprocess.run(command, shell=True, check=True)

    # Check the result
    if result.returncode != 0:
        raise Exception(f'An error occurred: {result.returncode}')
    else:
        mp3_size = os.path.getsize(mp3)
        mp4_size = os.path.getsize(mp4)
        if abs(mp3_size - mp4_size) < 0.1 * mp4_size:
            os.remove(mp4)
            return Path(mp3)




