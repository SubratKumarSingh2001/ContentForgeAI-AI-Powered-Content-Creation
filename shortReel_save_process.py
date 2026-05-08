from flask import render_template, url_for, request, redirect, flash, session, current_app 
from shortReel_generate_reel import text_to_speech_file, reel_generate_ffmpeg
from werkzeug.utils import secure_filename
from models import db, Reel
from datetime import datetime
from PIL import Image
import threading
import time
import os

def process_reel_files(rec_id, app) :
    ''' 
    This method is executed by the thread which runs in the background and due to which this method don't have context related to the flask i.e context: means which app to refer and which request
    flask work in an environment and within this env all the current_app, request, sessions all features are accessible. Its like a telling the method, which execute outside the flask env to refer
    this flask app and all its features like db, current_app, session etc.
    Temporarily giving this method access to the flask app features (Important without this method wont recognize to consider which flask app)
    '''

    with app.app_context() :
        reel = Reel.query.filter_by(uuid=rec_id).first()
        #to show the uploading status
        time.sleep(7)

        reel.set_status('processing')
        db.session.commit()

        #to show the processing status
        time.sleep(10)
        
        folder = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        try :
            print("STEP 1 - Before TTS")
            #Step:1 User_Description -> audio conversion
            with open(os.path.join(folder, "user_desc.txt"), 'r') as f :
                text = f.read()
            text_to_speech_file(text, folder) 

            print("STEP 2 - After TTS")
            #Step:2 Reel_Generation
            reel_generate_ffmpeg(folder, rec_id)

            print("STEP 3 - After FFmpeg")
        
            reel.set_status('completed')
            reel.set_video_path(f'static/reels/{rec_id}/reel.mp4')
            reel.set_created_at(datetime.now().strftime("%d %b %Y, %I:%M %p"))
            print("STATUS UPDATED TO COMPLETED")
        except Exception as e:
            print("Error: ", e)
            reel.set_status('failed')
            print("STATUS UPDATED TO FAILED")
        finally :
            db.session.commit()
    

def createReel() :
    #It captures the user files and text description 
    rec_id = request.form.get('uuid')
    user_desc = request.form.get('text')
    durations = request.form.getlist('duration')

    #store the status of reel
    reel= Reel(
        uuid=rec_id,
        user_description=user_desc,
        status="uploading",
        video_path=None,
        user_id=session.get('user_id') #Reel belong to the current logged-in user
    )
    db.session.add(reel)
    db.session.commit()

    input_files = []
    for key, file in request.files.items() :
        #Upload the files
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('shortReelGen'))
        if file : 
            filename = secure_filename(file.filename)
            os.makedirs(
                os.path.join(current_app.config['UPLOAD_FOLDER'], rec_id),
                exist_ok=True
            )
            #Want to store the compressed image files 
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], rec_id, filename)
            img = Image.open(file) 
            #Resize 
            img.thumbnail((720,1280))
            #compress and save file
            img.save(save_path, optimize=True, quality=70)

            input_files.append(filename)
        
        #Capture the text description and save it to the file 
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], rec_id, 'user_desc.txt'), 'w') as f :
            f.write(user_desc)
    
    for i in range(len(input_files)) :
        input_file = input_files[i]
        duration = durations[i]
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], rec_id, 'input.txt'), 'a') as f :
            f.write(f"file '{input_file}'\n duration {duration}\n")
    
    #Thread runs program in background parallel execution so that we can redirect url fast
    app = current_app._get_current_object() #Used actually to get the actual instance of flask app i.e app inside app.py 
    thread = threading.Thread(target=process_reel_files, args=(rec_id, app))
    thread.start()

    return redirect(url_for('shortReelGen', my_id=rec_id)) #redirect: redirect form POST -> new GET request to same webpage

