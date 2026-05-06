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
        caption = History.query.filter_by(id=id).first()
        caption.set_status('generating output')
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
            captions_list = generated_output.split('|||')
            captions_list = [caption.strip() for caption in captions_list if caption.strip()]

            #now we have the list of all generated caption and to store this list into the string we will use json
            caption.set_response(json.dumps(captions_list))
            caption.set_status('completed')
            caption.set_created_at(datetime.now())

        except Exception as e :
            print("Error", e)
            caption.set_status('failed')
        finally :
            db.session.commit()

    print(captions_list)


def createCaptions() :
    caption_topic = request.form.get('caption_topic')
    caption_style = request.form.get('caption_style')
    print(caption_topic)
    print(caption_style)

    #Fetch the values and store in the db
    caption = History(
        topic = caption_topic,
        tag = "Caption",
        status = 'processing',
        created_at = None,
        user_id = session.get('user_id')
    )

    db.session.add(caption)
    db.session.commit()


    if caption_topic == '' or caption_style == '' :
        flash('Some Fields are empty')
        return redirect(url_for('captionGenerator')) 

    prompt = f"""
                Generate high-quality social media captions.

                User Input (Topic + Context):
                {caption_topic}

                Style: {caption_style}

                IMPORTANT UNDERSTANDING:
                - The user input contains both topic and additional context
                - Extract intent, meaning, and key details from it
                - Captions must feel relevant and specific, not generic

                STYLE DEFINITIONS (STRICT):
                - professional → polished, clear, value-driven, minimal or no emojis
                - casual → friendly, relaxed, conversational
                - inspirational → uplifting, thoughtful, emotionally meaningful
                - creative → unique, expressive, imaginative, slightly witty

                INPUT USAGE RULES:
                - Use specific details from the user input when available
                - If input includes a product, story, or situation → reflect it clearly
                - If input is short → enhance it naturally without changing meaning
                - Do NOT generate vague or generic captions
                - Do NOT invent unrelated details

                CONTENT RULES:
                - Length: 2–3 lines only
                - Keep captions clean, natural, and readable
                - Avoid clickbait or overly promotional tone

                SOFT ENGAGEMENT GUIDELINES:
                - Engagement elements are OPTIONAL and should feel natural
                - You MAY include:
                    * a thoughtful question
                    * a relatable statement
                    * a reflective closing line
                - Do NOT force calls-to-action like “comment below”, “tag someone”
                - Keep engagement subtle and organic

                EMOJI USAGE:
                - professional → none or max 1 subtle emoji
                - casual → moderate emojis allowed
                - inspirational → meaningful emojis allowed
                - creative → expressive emojis allowed

                STRICT RESTRICTIONS:
                - DO NOT include hashtags
                - DO NOT include numbering or bullet points
                - DO NOT include explanations

                OUTPUT REQUIREMENTS:
                - Generate ONLY 8 to 10 captions
                - Each caption must be unique
                - Separate each caption using this EXACT delimiter: |||
                - Do NOT use new lines for separation
                - Output ONLY plain text

                FINAL BEHAVIOR RULE:
                - Balance clarity, tone, and subtle engagement
                - Maintain consistency with selected style
                - Each caption should feel natural, context-aware, and human-written

            """
    #This will run the generate_blog in the background so that we can render page fast and start the polling
    app = current_app._get_current_object()
    thread = threading.Thread(target=generate_response, args=(prompt, caption.id, app))
    thread.start()

    #redirect make POST->GET request
    return redirect(url_for('captionGenerator', id=caption.id))