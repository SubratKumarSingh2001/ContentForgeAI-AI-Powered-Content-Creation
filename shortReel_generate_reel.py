from flask import current_app
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def text_to_speech_file(text: str, folder: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_flash_v2_5", # use the flash model for low latency
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )
    # Generating a unique file name for the output MP3 file
    save_file_path = os.path.join(folder, "audio.mp3")

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")


def reel_generate_ffmpeg(folder, rec_id) :
    if not(os.path.exists(os.path.join('static', 'reels', rec_id))) :
            os.mkdir(os.path.join('static', 'reels', rec_id))

    print("FOLDER:", folder)
    print("INPUT:", f"{folder}/input.txt")
    print("EXISTS:", os.path.exists(f"{folder}/input.txt"))

    command = f'''ffmpeg -f concat -safe 0 -i {folder}/input.txt -i {folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{rec_id}/reel.mp4
    '''
    subprocess.run(command, shell=True, check=True) #shell: ensure this line runs as a shell command i.e as a string(command is string) and check: ensure command doesn't throw non-zero error
