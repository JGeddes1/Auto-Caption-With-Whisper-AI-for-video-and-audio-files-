import whisper
import hashlib
from pytube import YouTube
from datetime import timedelta
import os

def download_video(url):
    print("Start downloading", url)
    yt = YouTube(url)

    hash_file = hashlib.md5()
    hash_file.update(yt.title.encode())

    file_name = f'{hash_file.hexdigest()}.mp4'

    yt.streams.first().download("", file_name)
    print("Downloaded to", file_name)

    return {
        "file_name": file_name,
        "title": yt.title
    }

def transcribe_audio(path):
    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    video = download_video(path)
    transcribe = model.transcribe(video["file_name"])
    os.remove(video["file_name"])
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join(r"F:\Coding projects 2024\python\Whisper AI stuff", "subtitle.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

link = "https://www.youtube.com/watch?v=2KA0UWiTMWI&feature=youtu.be"
result = transcribe_audio(link)