from flask import render_template, redirect, request, session, url_for, flash, current_app
from models import db, History
from openai import OpenAI
from datetime import datetime
import threading
from dotenv import load_dotenv
import time 
import json
import os

load_dotenv()

key= key= os.getenv("API_KEY")
client = OpenAI(api_key=key)


def generate_response(prompt, id, app) :
    time.sleep(7)
    
    with app.app_context() :
        #now we will set status to generating output
        video_script = History.query.filter_by(id=id).first()
        video_script.set_status('generating output')
        db.session.commit()

        try :
            response = client.responses.create(
                model="gpt-5-mini",
                input = [
                    {'role': 'system', 'content': 'You are video scripts generator according to the prompt provided'},
                    {'role': 'user', 'content': prompt}
                ]
            )

            video_script.set_response(response.output_text)
            video_script.set_status('completed')
            video_script.set_created_at(datetime.now())

        except Exception as e :
            print("Error", e)
            video_script.set_status('failed')
        finally :
            db.session.commit()

    print(response.output_text)


def createVideoScripts() :
    video_script_topic = request.form.get('video_script_topic')
    video_script_style = request.form.get('video_script_style')
    video_duration = request.form.get('video_duration')
    print(video_script_topic)
    print(video_script_style)
    print(video_duration)


    #Fetch the values and store in the db
    video_script = History(
        topic = video_script_topic,
        tag = "Video Script",
        status = 'processing',
        created_at = None,
        user_id = session.get('user_id')
    )

    db.session.add(video_script)
    db.session.commit()


    if video_script_topic == '' or video_script_style == '' or video_duration == '' :
        flash('Some Fields are empty')
        return redirect(url_for('videoScriptsGen')) 

    prompt = f"""
                Generate a high-quality, production-ready video script.

                Topic: {video_script_topic}
                Style: {video_script_style}
                Duration: {video_duration}

                CRITICAL DURATION RULE (VERY IMPORTANT):

                - The script MUST strictly match the given duration
                - Assume speaking speed = 130–150 words per minute

                - If duration is:
                  * 10–15 minutes → generate approx 1300–2200 words
                  * 5–10 minutes → generate approx 700–1500 words
                  * Short → adjust accordingly

                - EXPAND content properly:
                  * Add detailed explanations
                  * Add examples
                  * Add mini stories
                  * Add transitions between ideas
                  * Do NOT keep sections short

                - If output feels short → it is WRONG

                ---

                STRUCTURE INSTRUCTION:

                - Divide script into sections covering FULL duration:

                Hook → Intro → Main Content (multiple parts) → Ending

                - Use EXACT format:

                [Section Name | Time Range]
                Script: ...
                Visual: ...
                Add-on: ...

                ---

                HTML RULES:

                - Output ONLY HTML
                - Do NOT include <html>, <head>, <body>

                - Wrap each section inside <section>

                - Use:
                <h2>[Hook | 0–5 sec]</h2>

                - Use:
                <p><strong>Script:</strong> ...</p>
                <p><strong>Visual:</strong> ...</p>
                <p><strong>Add-on:</strong> ...</p>

                ---

                SPACING RULE (VERY IMPORTANT):

                - After EACH <section>, add:
                <br>

                - This is mandatory
                - Do NOT skip spacing
                - Do NOT merge sections

                ---

                CONTENT DEPTH RULES:

                - For long durations:
                  * Each main section MUST be detailed
                  * Include explanations, reasoning, examples
                  * Include smooth transitions between parts

                - Avoid:
                  ❌ short paragraphs
                  ❌ surface-level explanation

                ---

                ENGAGEMENT RULES:

                - Strong hook is mandatory
                - Use curiosity triggers:
                  "But here’s the catch..."
                  "Most people don’t realize this..."

                ---

                VISUAL RULES:

                - Do NOT use raw terminal UI
                - Prefer:
                  - Code snippets
                  - Step visuals
                  - Overlays
                  - Before vs after

                ---

                ADD-ON RULES:

                - Suggest:
                  - Music
                  - Editing cues
                - Keep concise

                ---

                STRICT OUTPUT REQUIREMENTS:

                - Output ONLY HTML
                - Follow format EXACTLY
                - Include <br> after every section
                - Ensure script length matches duration strictly
                """
    #This will run the generate_blog in the background so that we can render page fast and start the polling
    app = current_app._get_current_object()
    thread = threading.Thread(target=generate_response, args=(prompt, video_script.id, app))
    thread.start()

    #redirect make POST->GET request
    return redirect(url_for('videoScriptsGen', id=video_script.id))