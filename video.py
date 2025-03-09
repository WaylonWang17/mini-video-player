#importing the required modules to use FFMPEG, Pillow, and Google text to speech
from PIL import Image, ImageFont, ImageDraw
import subprocess
import os
from gtts import gTTS
from pydub import AudioSegment


class ShortVideoGenerator:
    def __init__(self, image_path, output_image, video_path, audio_path, text = 'Default Text'):
        '''
        Initializes all the instances
        '''
        self.i_path = image_path
        self.o_image = output_image
        self.v_path = video_path
        self.a_path = audio_path
        self.t = text
        self.final_output = self.v_path.replace(".mp4", "+audio.mp4") #saves audio file
        self.vo_path = self.v_path.replace(".mp4", "_voiceover.mp3")  #saves voiceover file

    
    def process_image(self):
        '''
        handles the image processing (loading, overlaying text, and applying transformation)
        '''
        img = Image.open(self.i_path)
        img_resized = img.resize((1600, 900))

        IMG = ImageDraw.Draw(img_resized)

        size_font = ImageFont.truetype("times.ttf", 100)

        IMG.text((500, 150), "Tom and Jerry!", font = size_font, fill=(255, 255, 0))

        img_resized.save(self.o_image, format="JPEG")

    def generate_video(self):
        '''
        Generates the video and links it with subtitle
        '''
        time = 10
        subtitle_path = self.subtitles()  # generate subtitles
        subtitle_path = os.path.abspath(subtitle_path).replace("\\", "/") #makes it compatible for windows

        ffmpeg_cmd = [ #creates video from image and overlays text caption
        "ffmpeg", "-y", 
        "-loop", "1", 
        "-i", self.o_image,
        "-vf", "drawtext=text='Tom and...':fontcolor=blue:fontsize=150:x=(w-text_w)/2:y=h-text_h:enable='between(t,0,5)', drawtext=text='Jerry!':fontcolor=brown:fontsize=150:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,5,10)'", 
        "-c:v", "libx264", 
        "-t", str(time), 
        "-pix_fmt", "yuv420p", 
        "-stream_loop", "-1",
        self.v_path
    ]
        
        subprocess.run(ffmpeg_cmd)

    def generate_audio(self):
        '''
        Adds the theme song, gtts voiceover, and video altogether
        '''
        ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", self.v_path, "-i", self.vo_path, "-i", self.a_path,
        "-filter_complex",
        "[1:a]volume=2.0[a1];"  # Make the voiceover louder
        "[2:a]volume=0.5[a2];"  # Lower the background music
        "[a1][a2]amix=inputs=2:duration=longest[aout]",  # Mix voiceover + background music
        "-map", "0:v:0", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        self.final_output
    ]
        subprocess.run(ffmpeg_cmd)

    def subtitles(self):
        '''
        creates subtitle file and returns it to generate video
        '''
        subtitle_path = self.v_path.replace(".mp4", ".srt")

        #formatted weird but its to prevent spaces and such
        subtitles = """1
00:00:00,000 --> 00:00:05,000
Tom and...

2
00:00:05,000 --> 00:00:10,000
Jerry!
"""
        with open(subtitle_path, "w", encoding="utf-8") as f:
            f.write(subtitles)

        return subtitle_path
    
    def generate_voiceover(self):
        """
        Generate voiceover narration for captions
        """
        narration_texts = [
            ("Tom and...", 5),  #text and duration
            ("Jerry!", 5)
        ]

        combined_audio = AudioSegment.silent(duration=0) #empty audio soundtrack to store combined voiceover


        for text, duration in narration_texts:
            tts = gTTS(text, lang="en") #converts text to speech
            temp_audio_path = f"temp_{text.replace(' ', '_')}.mp3"
            tts.save(temp_audio_path)
            
            #saves audio as mp3
            audio = AudioSegment.from_file(temp_audio_path)
            audio = audio[:duration * 1000]  #trim to match caption
            combined_audio += audio

            os.remove(temp_audio_path)  #clean up

        combined_audio.export(self.vo_path, format="mp3")


    def run(self):
        '''
        runs the functions
        '''
        self.process_image()
        self.generate_video()
        self.generate_voiceover()  
        self.generate_audio()
        subprocess.run([self.final_output], shell=True)  # Works for Windows

if __name__ == "__main__":
    #paths for the image, video, and audio
    image_path = r"C:\Users\waylo\OneDrive\Documents\GitHub\tomandjerry.jpg"
    output_image = r"C:\Users\waylo\OneDrive\Documents\GitHub\tom_and_jerry_resized.jpg"
    video_path = r"C:\Users\waylo\OneDrive\Documents\GitHub\output_video.mp4"
    audio_path = r"C:\Users\waylo\Downloads\Tom and Jerry Theme.mp3"
    text = "Tom and Jerry"

    generate = ShortVideoGenerator(image_path, output_image, video_path, audio_path, text)
    generate.run()