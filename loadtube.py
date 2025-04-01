import yt_dlp
import librosa
import numpy as np
from mutagen.id3 import ID3, TBPM
from mutagen.mp3 import MP3
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def download_audio(youtube_url, output_path='output.mp3'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    # Rename the downloaded file to output.mp3
    for file in os.listdir():
        if file.startswith("audio") and file.endswith(".mp3"):
            os.rename(file, output_path)
            break
    
    return output_path

def analyze_bpm(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = round(float(tempo[0])) if len(tempo) > 0 else 0  # Eğer tempo boşsa 0 ata
    return bpm

def process_download():
    youtube_url = url_entry.get()
    if not youtube_url:
        status_label.config("Error", "Please enter a link from Youtube")
        return
    
    status_label.config(text="Downloading...")
    root.update()
    
    try:
        audio_file = download_audio(youtube_url)
        bpm = analyze_bpm(audio_file)
        
        # BPM bilgisini ID3 etiketi olarak ekleyelim
        audio = MP3(audio_file, ID3=ID3)
        if audio.tags is None:
            audio.tags = ID3()
        audio.tags.add(TBPM(encoding=3, text=str(bpm)))
        audio.save()
        
        status_label.config(text=f"Downloaded successfully! BPM: {bpm}")
    except Exception as e:
        status_label.config(text="Error, please try again.")

# Tkinter GUI oluşturma
root = tk.Tk()
root.title("Loadtube - MP3 Downloader & BPM Analyzer")
root.geometry("400x250")

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="YouTube Link:").grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(frame, width=40)
url_entry.grid(row=0, column=1, padx=5, pady=5)

download_button = tk.Button(root, text="Download", command=process_download)
download_button.pack(pady=10)


status_label = tk.Label(root, text="", fg="blue")
info_label = tk.Label(root, text="You can see your MP3 file as 'output.mp3'", fg="black")
info_label.pack(pady=5)
status_label.pack(pady=5)


contact_label = tk.Label(root, text="Contact me from Instagram, iristo.tech", fg="green")
contact_label.pack(pady=5)

root.mainloop()
