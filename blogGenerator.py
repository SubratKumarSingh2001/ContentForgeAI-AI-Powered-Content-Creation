from flask import render_template, redirect, request, session, url_for, flash, current_app
from models import db, History
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import os
import threading
import time 

load_dotenv()

key= os.getenv("API_KEY")
client = OpenAI(api_key=key)


def generate_response(prompt, id, app) :
    time.sleep(7)
    
    with app.app_context() :
        #now we will set status to generating output
        blog = History.query.filter_by(id=id).first()
        blog.set_status('generating output')
        db.session.commit()

        try :
            response = client.responses.create(
                model="gpt-5-mini",
                input = [
                    {'role': 'system', 'content': 'You are creative blog generator according to the prompt provided'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            blog.set_response(response.output_text)
            blog.set_status('completed')
            blog.set_created_at(datetime.now())

        except Exception as e :
            print("Error", e)
            blog.set_status('failed')
        finally :
            db.session.commit()

    print(response.output_text)


def createBlog() :
    blog_topic = request.form.get('blog_topic')
    keywords = request.form.get('keywords')
    add_details = request.form.get('details')
    print(blog_topic)
    print(keywords)
    print(add_details)

    #Fetch the values and store in the db
    blog = History(
        topic = blog_topic,
        tag = "Blog",
        status = 'processing',
        created_at = None,
        user_id = session.get('user_id')
    )

    db.session.add(blog)
    db.session.commit()


    if blog_topic == '' or keywords == '' or add_details == '' :
        flash('Some Fields are empty')
        return redirect(url_for('blogGenerator')) 

    prompt = f"""
            Write a high-quality blog article.

            Topic: {blog_topic}
            Mandatory Keywords: {keywords}
            Additional Instructions: {add_details}

            Core Rules:
            - Use all keywords naturally at least once
            - SEO optimized
            - Human readable and engaging tone
            - No keyword stuffing
            - Original content

            STRUCTURE INSTRUCTION (IMPORTANT):
            - Return output ONLY in clean HTML format
            - Do NOT include any explanations or extra text outside HTML
            - Use semantic HTML tags appropriately

            - The structure of the article MUST adapt based on "Additional Instructions"
            - If no structure is specified, follow a natural blog flow with a strong opening, logical progression, and a clear ending

            HTML USAGE RULES:
            - Use <h1> only for the main title (once)
            - Use <h2> for section headings when needed
            - Use <h3> for subheadings if required
            - Use <p> for all paragraphs
            - Use <ul><li> for bullet points if needed
            - Use <strong> to highlight important terms

            READABILITY & SPACING:
            - Keep paragraphs short (4-5 lines max)
            - Ensure proper separation between sections
            - Avoid large blocks of text
            - Maintain clean and readable structure

            BEHAVIOR RULE:
            - Follow "Additional Instructions" strictly for structure and formatting
            - If headings are not requested, minimize their usage
            - If bullet points are not requested, avoid them
            - Do NOT force any structure unnecessarily

            OUTPUT REQUIREMENT:
            - Return ONLY HTML content that can be directly injected inside an existing webpage
            - Do NOT include <html>, <head>, or <body> tags
            - Do NOT include </html>, </body>, or any full document structure
            - Do NOT include any explanations or text outside HTML
         
            """
    #This will run the generate_blog in the background so that we can render page fast and start the polling
    app = current_app._get_current_object()
    thread = threading.Thread(target=generate_response, args=(prompt, blog.id, app))
    thread.start()

    #redirect make POST->GET request
    return redirect(url_for('blogGenerator', id=blog.id))