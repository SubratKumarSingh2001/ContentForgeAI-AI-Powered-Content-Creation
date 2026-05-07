from flask import current_app
from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

key = os.getenv("API_KEY")
client = OpenAI(api_key=key)

def text_to_speech_file(text: str, folder: str) -> str:
      # Ensure folder exists
    os.makedirs(folder, exist_ok=True)

    save_file_path = os.path.join(folder, "audio.mp3")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text
    ) as response:

        response.stream_to_file(save_file_path)

    print(f"{save_file_path}: Audio file generated successfully!")


def reel_generate_ffmpeg(folder, rec_id) :
    # Ensure reel output folder exists
    os.makedirs(
        os.path.join('static', 'reels', rec_id),
        exist_ok=True
    )

    print("FOLDER:", folder)
    print("INPUT:", f"{folder}/input.txt")
    print("EXISTS:", os.path.exists(f"{folder}/input.txt"))

    command = f'''ffmpeg -f concat -safe 0 -i {folder}/input.txt -i {folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{rec_id}/reel.mp4
    '''
    subprocess.run(command, shell=True, check=True) #shell: ensure this line runs as a shell command i.e as a string(command is string) and check: ensure command doesn't throw non-zero error
