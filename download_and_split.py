from lalalai import batch_process
from handle_secrets import secrets
from handle_youtube import download_from_youtube
import os
from pathlib import Path

file = str(Path(os.getcwd(), download_from_youtube("https://www.youtube.com/watch?v=cZH_NA93kd8", "downloads", mode="audio", quality="highest", okay_with_webm=False)))
batch_process(secrets["lalalai"], file)