from pytube import YouTube
from pathlib import Path
import datetime, math, subprocess, os, torch, openai
from requests_html import HTMLSession

def find_videos(channel,search_terms):
    
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
                            pass
                except:
                    pass
    video_urls = []
    for i, title in enumerate(titles):
        for search_term in search_terms:
            if search_term in title.lower():
                video_urls.append(links[i])
    os.system("cls")
    print("Got urls from HTML")
    return video_urls

def download_video(video_url):
    # Download video using pytube
    yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    for i, stream in enumerate(yt.streams):
        if stream.mime_type == "audio/mp4" and stream.abr == "48kbps":
            yt.streams[i].download(output_path=folder, filename=youtube_audio_name)
            return stream.default_filename
    os.system("cls")
    print("Downloaded video")

def get_size(filename):
    """Get the size of an audio file."""
    cmd = ["ffprobe", '-i', filename, '-show_entries', 'format=size', '-v', 'quiet', '-of', 'csv=p=0']
    output = subprocess.check_output(cmd)
    return int(output)/1024/1024

def get_duration(filename):
    """Get the duration of an audio file."""
    cmd = ['ffprobe', '-i', filename, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
    output = subprocess.check_output(cmd)
    return float(output)

def reformat(filename):
    output_file = Path(folder,filename.stem+"_reformatted.mp3")
    command = ["ffmpeg", "-i", filename, "-vn", "-ac", "1", "-ar", "16000", "-ab", "192k", "-y", output_file]
    subprocess.run(command, check=True)
    os.remove(filename)
    return output_file

def to_time(seconds):
    """Convert seconds to hh:mm:ss."""
    return str(datetime.timedelta(seconds=seconds))

def split_file(filename,title):
    files = []
    filename = reformat(filename)
    """Split an audio file into chunks of a specified duration."""
    total_duration = get_duration(filename)
    chunk_duration = int(get_duration(filename)/(get_size(filename)/24))
    num_chunks = math.ceil(total_duration / chunk_duration)
    
    for i in range(num_chunks):
        start_time = to_time(i * chunk_duration) if i == 0 else to_time((i * chunk_duration) - 2)
        end_time = to_time(((i+1) * chunk_duration) + 2)
        output = Path(f'{folder}/{title}_{i}.mp3')
        cmd = ['ffmpeg', '-i', filename, '-ss', str(start_time), '-to', str(end_time), 
               '-c', 'copy', output]
        subprocess.run(cmd, check=True)
        files.append(Path(output))
    os.remove(filename)
    os.system("cls")
    print("Split file")
    return files

def transcribe_audio(filename):
    os.environ["REQUESTS_CA_BUNDLE"] = "C:/Users/calvi/3D Objects/test/Baltimore CyberTrust Root.crt"
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def process_videos(video_urls):
    for i, video_url in enumerate(video_urls):
        title = download_video(video_url)[:-4]
        nice_title = "_".join(search_array[i].split(" "))
        files = split_file(Path(f"{folder}/{youtube_audio_name}"),nice_title)
        os.system("cls")
        print(title)
        print("\n".join(str(each) for each in files))
        if input(f"Transcribe {title}? ") == "y":
            for k, file in enumerate(files):
                print("\nTranscribing audio...")
                start = datetime.datetime.now()
                result = transcribe_audio(file)
                end = datetime.datetime.now()
                print(result)
                with (open(f"downloads/{Path(file).stem}_text.txt", "w")) as f:
                    f.write(result["text"])
                with (open(f"downloads/{Path(file).stem}_segments.txt", "w")) as f:
                    f.write(str(result))
                print(f"Transcription took {end-start}\n")
                # Clean up the downloaded files
                os.remove(file)

folder = "downloads"
youtube_audio_name = "ytAudio.mp3"
search_array = ["how to breathe correctly"]

openai.api_key = "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"
process_videos(find_videos("huberman", search_array))
