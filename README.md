🎥 Mini Video Player with TTS & Subtitles

📌 Project Description

This project is a Python-based video generator that creates a video from a Tom and Jerry image. It overlays captions, and adds voiceover narration using Google Text-to-Speech (gTTS). It also mixes background music and subtitles using FFmpeg.

🚀 Features

Image to Video Conversion 📷➡🎥

Text Overlay & Captions 📝

Subtitles (.srt file) 🎬

Voiceover Narration (gTTS) 🔊

Background Music Mixing 🎵

Looping Video Support 🔄

🛠️ Installation

1️⃣ Clone the Repository

git clone https://github.com/WaylonWang17/mini-video-player.git
cd mini-video-player

2️⃣ Install required modules

pip install pillow

3️⃣ Ensure FFmpeg is Installed

Windows: Download & install from FFmpeg official site

Mac: Install via Homebrew:

brew install ffmpeg

Linux: Install via package manager:

sudo apt install ffmpeg

🎬 Usage

Run the Script

python video.py

Customizing Input Files

Modify video.py to set your image, audio, and text:

image_path = "assets/tomandjerry.jpg"
audio_path = "assets/Tom_and_Jerry_Theme.mp3"
text = "Tom and Jerry"

🔧 How It Works

1️⃣ Loads an image and resizes it for video background.2️⃣ Overlays text captions at specific timestamps.3️⃣ Generates subtitles (.srt) and embeds them into the video.4️⃣ Uses Google Text-to-Speech (gTTS) to create a voiceover.5️⃣ Merges background music with the voiceover.6️⃣ Generates the final MP4 video with subtitles & narration.

🛠️ Technologies Used

Python, FFmpeg, Pillow (PIL), Google Text-to-Speech (gTTS), PyDub

