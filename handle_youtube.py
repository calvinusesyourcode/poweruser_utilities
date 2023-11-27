from pytube import YouTube
from pathlib import Path
import datetime, math, subprocess, os, torch, openai, pathlib, re, inquirer, time, pyperclip

from handle_audio import audio_mp4_to_mp3
from handle_strings import get_clipboard, show_message

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def find_videos(channel,search_terms):
    """Find video URLs from a channel that match a search term.
    
    "lex" or "huberman" for channel"""
    
    from requests_html import HTMLSession
    url = {'lex': 'https://www.youtube.com/@lexfridman/videos',
            'huberman': 'https://www.youtube.com/@hubermanlab/videos'}[channel]
    
    #use the session to get the data
    s = HTMLSession().get(url)
    #Render the page, up the number on scrolldown to page down multiple times on a page
    s.html.render(sleep=1, keep_page=True, scrolldown=1)

    titles = []
    links = []
    divs = s.html.find('.ytd-two-column-browse-results-renderer',first=True).find("#primary",first=True).find(".ytd-rich-grid-renderer")#.find("#contents",first=True)
    for div in divs:
        if div.find("#contents",first=True):
            video_rows = div.find("#contents",first=True).find(".ytd-rich-grid-row")
            for i, row in enumerate(video_rows):
                try:
                    videos = row.find("#contents",first=True).find(".ytd-rich-item-renderer")
                    for k, video in enumerate(videos):
                        try:
                            metadata = video.find(".ytd-rich-item-renderer",first=True).find("#content",first=True).find(".ytd-rich-grid-media",first=True) \
                            .find("#dismissible",first=True).find("#details",first=True).find("#meta",first=True) \
                            .find("#video-title-link",first=True)
                            title = metadata.attrs["title"]
                            link = "https://www.youtube.com"+metadata.attrs["href"]
                            if title not in titles:
                                titles.append(title)
                                links.append(link)
                        except:
                            print('FAILED: video.find(".ytd-rich-item-renderer",first=True).find("#content",first=True).find(".ytd-rich-grid-media",first=True) \
                            .find("#dismissible",first=True).find("#details",first=True).find("#meta",first=True) \
                            .find("#video-title-link",first=True)')
                except:
                    print('FAILED: row.find("#contents",first=True).find(".ytd-rich-item-renderer")')
    video_urls = []
    for i, title in enumerate(titles):
        for search_term in search_terms:
            if search_term in title.lower():
                video_urls.append(links[i])
    os.system("cls")
    print("Got urls from HTML")
    with (open(f"log.txt", "w")) as f:
                f.write("Got urls from HTML:\n")
                f.write("".join(str(each)+"\n" for each in video_urls))
    return video_urls

def download_from_youtube(video_url:str, folder:pathlib.WindowsPath="downloads", mode:str="video", quality:str="good", okay_with_webm:bool=True):
    """
    Download video using pytube, returns youtube video title.
    
    Args:
        *video_url: URL of the video to download.
        folder: Destination folder.
        mode: Download mode. Can be "video" or "audio". Defaults to "video".
        quality: Quality of the video. Can be "highest", "good" for 1080p, "medium" for 720p, "low" for 480p, "lowest". Defaults to "good".
        okay_with_webm: Defaults to True.

    Returns:
        str: A formatted title of the downloaded YouTube video.
    """
    print(f"Downloading from YouTube... {video_url}")

    if mode == "video":
        
        audio_path = download_from_youtube(video_url, folder, mode="audio", quality=quality, okay_with_webm=okay_with_webm)
        video_path = download_from_youtube(video_url, folder, mode="video_only", quality=quality, okay_with_webm=okay_with_webm)
        print(video_path, audio_path)
        output_filename = Path(folder, str(audio_path.stem).split("_____")[1]+".mp4")

        command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_filename}"
        subprocess.check_output(command, shell=True)
        os.remove(video_path)
        os.remove(audio_path)
        print(output_filename)
        return output_filename


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
            # return Path(folder, output_filename)
            path = Path(audio_mp4_to_mp3(folder, output_filename))
            return path
        else:
            return Path(folder, output_filename)

import os
import subprocess
import inquirer
from typing import List, Tuple

def download_video_and_transcript(video_url: str, folder: pathlib.WindowsPath = "downloads"):
    """
    Download video and its transcript using pytube, returns youtube video title and transcript.
    
    Args:
        video_url: URL of the video to download.
        folder: Destination folder.

    Returns:
        Tuple: A tuple containing the title of the downloaded YouTube video and its transcript.
    """
    video_id = extract_video_id_from_url(video_url)
    try:
        global transcript
        transcript = get_transcript(video_id)
    except Exception as e:
        print(e, "No transcript found")
    if transcript:
        print("\n~".join([f"{start_time}s: {text}" for start_time, text in transcript[:10]]) + "...")
    video_path = download_from_youtube(video_url, folder, mode="video", quality="good", okay_with_webm=True)
    if transcript:
        import re
        transcript_folder = os.path.join(folder, "transcripts")
        os.makedirs(transcript_folder, exist_ok=True)
        video_title = re.search(r'\\([^\\]*?)\.', str(video_path)).group(1)
        with open(os.path.join(transcript_folder, f"{video_title}.txt"), "w") as f:
            for start_time, text in transcript:
                f.write(f"{start_time}s: {text}\n")

    return video_path, transcript

def select_transcript_lines(transcript: List) -> List[Tuple[float, float]]:
    """
    Prompt the user to multiple choice select which lines of the transcript.

    Args:
        transcript: The transcript of the video.

    Returns:
        List[Tuple[float, float]]: A list of tuples where each tuple represents the start and end time of a selected line.
    """
    lines = [f"{i}, {start_time}s: {text}" for i, [start_time, text] in enumerate(transcript)]
    choices = [inquirer.Checkbox("lines", message="Select lines", choices=lines)]
    selected_lines =  inquirer.prompt(choices)["lines"]
    
    selected_times = {}
    last_i = 0
    block = 0
    for i in [int(line[0]) for line in selected_lines]:
        time, text = transcript[i]
        if i-1 == last_i:
            block_time = transcript[block][0]
            duration = transcript[i+1][0]-block_time-0.05
            text = transcript[block][1] + " " + text
        else:
            block_time = time
            duration = transcript[i+1][0]-time-0.05
            block = i
        selected_times[block_time] = [duration, text]
        last_i = i

    return selected_times

def video_to_clips(video_path: str, io_points, output_folder: str):
    """
    Use ffmpeg to cut out slices from the downloaded video.

    Args:
        video_path: The path of the video file.
        io_points: A list of tuples where each tuple represents the start and end time of a slice.
        output_folder: The folder to save the output clips.
    """
    print("video_to_clips", video_path, io_points, output_folder, sep=";;")
    os.makedirs(output_folder, exist_ok=True)
    
    for i, (start, (duration, _)) in enumerate(io_points.items()):
        print(start, duration)
        output_file = os.path.join(output_folder, f"clip_{i}.mp4")
        command = f'ffmpeg -i "{video_path}" -ss {start} -to {start+duration} "{output_file}"'
        print(command)

        subprocess.check_output(command, shell=True)

def yt_urls_to_audiopath(urls:list,folder:str="output"):
    audiopaths = []
    for url in urls:
        audio_path = download_from_youtube(url,folder,mode="audio",quality="low",okay_with_webm=True)
        audiopaths.append(audio_path)
    return audiopaths

def download_with_ui():
    url = pyperclip.paste()
    if "https://" not in url or "you" not in url or len(url) > 100:
        print("No YouTube URL found in clipboard.")
    else:
        questions = [
            inquirer.List(
                "file_type",
                message="",
                choices=["video","audio","video_only"]
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
        print(download_from_youtube(url, mode=answers["file_type"], quality=answers["quality"]))

        subprocess.Popen(f'explorer "{folder}"')

import re
import pyperclip
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id_from_url(url):
    match = re.search(r"watch\?v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = []
        for item in transcript_list:
            start_time = item['start']
            text = item['text']
            try:
                transcript.append([start_time, text])
            except:
                print("Failed to add to transcript")
        if "Could not retrieve a transcript for the video" in "".join([text for _, b in transcript[:6]]):
            raise Exception("Could not retrieve a transcript for the video")
        return transcript
    except Exception as e:
        raise e

def download_transcript_with_ui():
    clipboard_content = pyperclip.paste()
    video_id = extract_video_id_from_url(clipboard_content)

    if not video_id:
        video_id = extract_video_id_from_url(input("Enter YouTube video ID: "))

    transcript = get_transcript(video_id)
    print(transcript)
    return transcript

def test():
    folder = "downloads"
    video_url = pyperclip.paste()
    if not video_url:
        video_url = input("Enter YouTube URL: ")

    # Download video and transcript
    video_path, transcript = download_video_and_transcript(video_url, folder)

    # Select lines from transcript
    selected_times = select_transcript_lines(transcript)

    # Cut out slices from video
    print(video_path)
    output_folder = os.path.join(folder, "clips")
    print(video_path, selected_times, output_folder)

    video_to_clips(video_path, selected_times, output_folder)


def test2():
    _, video_path, selected_times, output_folder = """video_to_clips;;downloads\youre_afraid_of_the_effort_david_goggins.mp4;;s;;downloads\clips""".split(";;")
    selected_times = {0.42: [4.14, "I hear it all the time but he doesn't want to end up like him"]}
    video_to_clips(video_path, selected_times, output_folder)
    

# test()