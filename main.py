import re
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
    
    caption_file_name = re.sub(r'\.[^.]+$', '', video["title"]) 
    print("This is caption_file name: " + caption_file_name)

    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join(caption_path,caption_file_name +".srt")
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

    
    captionlocation_label.config(text=f"Output location for captions: {caption_path}") 

    return caption_path

caption_path = "." 

# Create the main window
root = tk.Tk()
root.title("Video Caption Transcription")

# Frame for input section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Label and Entry for YouTube URL
url_label = Label(input_frame, text="Enter YouTube URL or select a local video:")
url_label.grid(row=0, column=0, pady=5, padx=5)

entry = Entry(input_frame, width=50)
entry.grid(row=0, column=1, pady=5, padx=5)

# Button to select a local video file
select_file_button = Button(input_frame, text="Select Local Video File", command=select_local_file)
select_file_button.grid(row=1, column=0, columnspan=2, pady=10)

# Frame for output section
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

# Button to select output path of captions
select_caption_button = Button(output_frame, text="Select Output Location for Caption File", command=select_output_file)
select_caption_button.grid(row=1, column=1, pady=10)

# Button to trigger the transcription
submit_button = Button(output_frame, text="Submit", command=on_submit)
submit_button.grid(row=1, column=2, pady=5, padx=5)

# Result label
result_label = Label(root, text="")
result_label.pack(pady=10)

# Caption location label
captionlocation_label = Label(root, text="")
captionlocation_label.pack(pady=10)

root.mainloop()