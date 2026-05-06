from flask import render_template, redirect, request, session, url_for, flash, current_app
from models import db, History
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import threading
import time 
import json
import os

load_dotenv()

key= os.getenv("API_KEY")
client = OpenAI(api_key=key)


def generate_response(prompt, id, app) :
    time.sleep(7)
    
    with app.app_context() :
        #now we will set status to generating output
        hashtag = History.query.filter_by(id=id).first()
        hashtag.set_status('generating output')
        db.session.commit()

        try :
            response = client.responses.create(
                model="gpt-5-mini",
                input = [
                    {'role': 'system', 'content': 'You are creative captions generator according to the prompt provided'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            generated_output = response.output_text
            hashtags_list = generated_output.split('|||')
            hashtags_list = [hashtag.strip() for hashtag in hashtags_list if hashtag.strip()]

            #now we have the list of all generated hashtag and to store this list into the string we will use json
            hashtag.set_response(json.dumps(hashtags_list))
            hashtag.set_status('completed')
            hashtag.set_created_at(datetime.now())

        except Exception as e :
            print("Error", e)
            hashtag.set_status('failed')
        finally :
            db.session.commit()

    print(hashtags_list)


def createHashtags() :
    hashtag_topic = request.form.get('hashtag_topic')
    keywords = request.form.get('keywords')
    print(hashtag_topic)
    print(keywords)

    #Fetch the values and store in the db
    hashtag = History(
        topic = hashtag_topic,
        tag = "Hashtag",
        status = 'processing',
        created_at = None,
        user_id = session.get('user_id')
    )

    db.session.add(hashtag)
    db.session.commit()


    if hashtag_topic == '' or keywords == '' :
        flash('Some Fields are empty')
        return redirect(url_for('hashtagGenerator')) 

    prompt = f"""
                Generate high-performing, high-reach social media hashtags.

                Content Niche / Topic:
                {hashtag_topic}

                Keywords:
                {keywords}

                IMPORTANT UNDERSTANDING:
                - "Niche/Topic" defines the main category
                - "Keywords" define the specific focus
                - Hashtags MUST align with both

                HASHTAG STRATEGY (VERY IMPORTANT):
                - Generate a balanced mix:
                    * High-reach hashtags (broad, popular)
                    * Medium-reach hashtags (moderate competition)
                    * Niche hashtags (targeted, high-conversion)

                - Prioritize hashtags that:
                    * Improve discoverability
                    * Attract the right audience
                    * Are commonly searched or used

                ENGAGEMENT OPTIMIZATION:
                - Prefer hashtags that are:
                    * Actively used in the niche
                    * Relevant to audience intent
                    * Likely to increase visibility and interaction
                - Avoid dead, spammy, or banned hashtags

                CONTENT RULES:
                - Each hashtag must start with #
                - Keep hashtags clean and readable
                - No special characters (except #)
                - No repetition

                STRICT RESTRICTIONS:
                - DO NOT include explanations
                - DO NOT include sentences or captions
                - DO NOT include numbering or bullet points

                OUTPUT REQUIREMENTS:
                - Generate EXACTLY 18 hashtags
                - Separate each hashtag using this EXACT delimiter: |||
                - Do NOT use spaces or new lines for separation
                - Output ONLY plain text

                FINAL BEHAVIOR RULE:
                - Focus on reach + relevance + audience targeting
                - Ensure hashtags help maximize visibility and engagement

            """
    #This will run the generate_blog in the background so that we can render page fast and start the polling
    app = current_app._get_current_object()
    thread = threading.Thread(target=generate_response, args=(prompt, hashtag.id, app))
    thread.start()

    #redirect make POST->GET request
    return redirect(url_for('hashtagGenerator', id=hashtag.id))