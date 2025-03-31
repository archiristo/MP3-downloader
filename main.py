import yt_dlp
import librosa
import numpy as np
from mutagen.id3 import ID3, TPE1, TIT2, TBPM
from mutagen.mp3 import MP3
import os
import soundfile as sf

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
    print(f"İndirilen şarkının BPM değeri: {bpm}")

if __name__ == "__main__":
    youtube_url = input("YouTube Linki: ")
    audio_file = download_audio(youtube_url)
    analyzebpm = analyze_bpm(audio_file)

    # BPM bilgisini ID3 etiketi olarak MP3'e kaydet
    output_filename = 'output.mp3'
    audio = MP3(output_filename, ID3=ID3)
    if audio.tags is None:
        audio.tags = ID3()

    audio.tags.add(TBPM(encoding=3, text=str(analyzebpm)))
    audio.save()

    print(f"{output_filename} dosyasına BPM bilgisi eklendi.")
