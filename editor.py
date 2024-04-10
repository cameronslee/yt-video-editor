# editor.py

VIDEO_URL = "https://www.youtube.com/watch?v=JN3KPFbWCy8"

from pytube import YouTube

def download_video():
    yt = YouTube(VIDEO_URL)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

FILENAME = "JN3KPFbWCy8.csv"

import pandas as pd

df = pd.read_csv(FILENAME)

# mac booshit
# https://github.com/Zulko/moviepy/issues/1158
import platform
import os
if platform.system() == 'Darwin':
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import VideoFileClip

# TODO create cover picture for video with save_frame
# myclip.save_frame("frame.jpeg", t='01:00:00') # frame at time t=1h

INPUT_DIR = "./input_data/"
VIDEO_FILE_PATH = INPUT_DIR + "Elon Musk War AI Aliens Politics Physics Video Games and Humanity  Lex Fridman Podcast 400.mp4"

from tqdm import tqdm
FADE_DURATION = 3
OUTPUT_DIR = "./output_data/"

def process_row(row):
    start = row['start']
    end = row['end']

    # label video with top three entities from embeddings
    label = row['top_three_entities']
    v = VideoFileClip(VIDEO_FILE_PATH)
    v2 = v.subclip(start,end)

    fade_duration = 3  # Duration of the fade-out effect in seconds
    v3 = v2.fadein(fade_duration) 

    v4 = v3.audio_fadein(fade_duration)
    v5 = v4.audio_fadeout(fade_duration)
    v6 = v5.fadeout(fade_duration)

    output_path = OUTPUT_DIR + "output_" + label + ".mp4"

    v6.write_videofile(output_path, codec="libx264", audio_codec="aac")


tqdm.pandas(desc="Generating Clips")

df.progress_apply(process_row, axis=1)
