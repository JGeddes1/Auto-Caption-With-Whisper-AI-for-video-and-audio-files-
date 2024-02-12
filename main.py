import whisper
import hashlib
from pytube import YouTube
from datetime import timedelta
import os
import tkinter as tk
from tkinter import Entry, Button, Label, filedialog

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


def transcribe_audio_local(file_path, caption_path):
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    
    # No need to download, use the provided local file directly
    video = {"file_name": file_path, "title": os.path.basename(file_path)}
    
    transcribe = model.transcribe(video["file_name"])
    
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join(caption_path, video["title"]+".srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)


    return srtFilename

def on_submit():
    link = entry.get()
    if link.startswith('https://www.youtube.com/'):
        # If the input is a YouTube URL, download the video
        result = transcribe_audio(link)
        result_label.config(text=f"SRT file generated: {result}")
    else:
        # If the input is a local file path, transcribe it directly
        result = transcribe_audio_local(link, caption_path)
        result_label.config(text=f"SRT file generated: {result}")
 
def select_local_file():
    file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def select_output_file():
    global caption_path
    caption_path = filedialog.askdirectory(title="Select folder to put captions")

    
    captionlocation_label.config(text=f"SRT file generated: {caption_path}") 

    return caption_path

caption_path = "." 
# Tkinter GUI
root = tk.Tk()
root.title("YouTube Transcription")

# Label and Entry for YouTube URL
url_label = Label(root, text="Enter YouTube URL or select a local video:")
url_label.pack(pady=10)

entry = Entry(root, width=50)
entry.pack(pady=10)


# Button to select a local video file
select_file_button = Button(root, text="Select Local File", command=select_local_file)
select_file_button.pack(pady=10)
# Button to select output path of captions
select_caption_button = Button(root, text="Select Output location for  File", command=select_output_file)
select_caption_button.pack(pady=10)

# Button to trigger the transcription
submit_button = Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Label to display the result
result_label = Label(root, text="")
result_label.pack(pady=10)
# Label to display the output location for captions
captionlocation_label = Label(root, text="")
captionlocation_label.pack(pady=10)

root.mainloop()