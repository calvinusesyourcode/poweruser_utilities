from pytube import YouTube
from pathlib import Path
import subprocess, os, pathlib, re, inquirer, time, pyperclip

from handle_audio import audio_mp4_to_mp3

def download_from_youtube(video_url:str, folder:pathlib.WindowsPath="downloads", mode:str="video", quality:str="good", okay_with_webm:bool=True):
    """
    Download video using pytube, returns file path.
    
    Args:
        *video_url: URL of the video to download.
        folder: Destination folder.
        mode: Audio or video? Defaults to "video".
        quality: Quality of the video. Can be "highest", "good" for 1080p, "medium" for 720p, "low" for 480p, "lowest". Defaults to "good".
        okay_with_webm: Defaults to True.

    Returns:
        str: A formatted title of the downloaded YouTube video.
    """

    if mode == "video":
        
        audio_path = download_from_youtube(video_url, folder, mode="audio", quality=quality, okay_with_webm=okay_with_webm)
        video_path = download_from_youtube(video_url, folder, mode="video_only", quality=quality, okay_with_webm=False)
        print(video_path, audio_path)
        output_filename = Path(folder, str(audio_path.stem).split("_____")[1]+".mp4")

        command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_filename}"
        subprocess.check_output(command, shell=True)
        os.remove(video_path)
        os.remove(audio_path)


    elif mode == "video_only":

        youtube_video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)

        videos = youtube_video.streams.filter(type="video")
        if not okay_with_webm:
            videos = videos.filter(file_extension="mp4")
        streams = sorted(videos, reverse=True, key=lambda stream: int(''.join(c for c in stream.resolution if c.isdigit())) if stream.resolution else 0)
        
        quality_map = {
            "highest": 999999,
            "good": 1080,
            "medium": 720,
            "low": 480,
            "lowest": 360,
        }
        selected_stream = next((stream for stream in streams if int(re.findall(r'\d+', stream.resolution)[0]) <= quality_map[quality]), None)

    elif "audio" in mode:

        youtube_video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        streams = sorted(youtube_video.streams.filter(only_audio=True, file_extension="mp4"), reverse=True, key=lambda stream: int(''.join(c for c in stream.abr if c.isdigit())) if stream.abr else 0)

        quality_map = {
            "highest": 160000,
            "good": 128000,
            "medium": 70000,
            "low": 50000,
            "lowest": 48000,
        }
        
        selected_stream = next((stream for stream in streams if stream.bitrate <= quality_map[quality]), None)
        if selected_stream is None: #TODO: optimize this
            selected_stream = next((stream for stream in sorted(streams, key=lambda x: x.bitrate) if stream.bitrate > quality_map[quality]), None)
        
        print(selected_stream)
    else:
        raise Exception("Invalid mode. Must be 'video', 'audio', or 'video_only'.")
    
    if mode != "video":
        default_filename = selected_stream.default_filename
        without_extension = "".join(default_filename.split(".")[:-1])
        video_title = mode+"_____"+"_".join("".join(c.lower() for c in without_extension if c.isalnum() or c == " ").split(" "))
        file_extension = default_filename[-7:].split(".")[-1]
        output_filename = f"{video_title}.{file_extension}"
        
        selected_stream.download(output_path=folder, filename=output_filename)

        if mode == "audio":
            return audio_mp4_to_mp3(folder, output_filename)
        else:
            return Path(folder, output_filename)

def download_with_ui():
    url = pyperclip.paste()
    if "https://" not in url:
        print("No URL found in clipboard.")
        time.sleep(5)
    else:
        questions = [
            inquirer.List(
                "file_type",
                message="",
                choices=["video","audio","video_only",]
            ),
            inquirer.List(
                "quality",
                message="",
                choices=['highest', 'good', 'medium', 'low', 'lowest']

            ),
        ]

        folder = "downloads"
        if not os.path.exists(folder):
            os.makedirs(folder)

        answers = inquirer.prompt(questions)
        download_from_youtube(url, mode=answers["file_type"], quality=answers["quality"])

        subprocess.Popen(f'explorer "{folder}"')

download_with_ui()