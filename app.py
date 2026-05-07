from flask import Flask, render_template, url_for, request, session, redirect
from auth import signIn, signUp
from models import db, Reel, History
from functools import wraps
from shortReel_save_process import createReel
from blogGenerator import createBlog
from captionsGenerator import createCaptions
from hashtagGenerator import createHashtags
from videoScriptsGen import createVideoScripts
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid
import os
import json

load_dotenv() #it loads all the variables written inside the .env file

UPLOAD_FOLDER = 'user_uploads_reelGen'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) #This ensure that UPLOAD_FOLDER not there then creates it automatically exist_ok=True if exist then ok move ahead

#now we will connect the db instance with flask app and create all tables
db.init_app(app)
with app.app_context() : #db is outside the flask env and to allow the db to know which flask app we are talking about we use app.app_context()
    db.create_all()

#creating decorator for signin required compulsory
def signin_required(func) :
    @wraps(func)
    def decorated_function(*args, **kwargs) :
        if 'user_id' not in session :
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    return decorated_function

@app.route('/')
def home() :
    return render_template("home.html")

@app.route('/sign-in', methods=['GET','POST'])
def signin() :
    return signIn()

@app.route('/sign-up', methods=['GET','POST'])
def signup() :
    return signUp()

@app.route('/sign-out')
def signout() :
    session.pop('user_id')
    session.pop('name')
    return redirect(url_for('home'))

@app.route('/dashboard')
@signin_required
def dashboard() :
    return render_template("dashboard.html")

@app.route('/short-reel-generator', methods=['GET','POST'])
@signin_required
def shortReelGen() :
    # my_id = uuid.uuid4()
    if request.method == 'POST' :
        return createReel()
    
    #if we redirect POST->GET request then url must have my_id thats why used .args
    my_id = request.args.get('my_id')
    if not my_id : 
        my_id = uuid.uuid4()  #unique id create for identification for first time get request 

    reel = None
    reel = Reel.query.filter_by(uuid=str(my_id)).first()

    return render_template("shortReelGenerator.html", my_id=my_id, reel=reel)

@app.route('/reel-status/<rec_id>')
@signin_required
def reel_status(rec_id) :
    reel = Reel.query.filter_by(uuid=rec_id).first()

    return {
        "status":reel.status,
        "video": f"/static/reels/{rec_id}/reel.mp4" if reel.video_path else None
    }

@app.route('/reel-history')
@signin_required
def reel_history() :
    reels = Reel.query.filter_by(user_id=session.get('user_id')).order_by(Reel.created_at.desc()).limit(50).all()
    all_reels = []
    for reel in reels :
        if reel.status == 'completed' :
            all_reels.append({
                'reel_id': reel.id,
                'reel_path': reel.video_path,
                'reel_created_at': reel.created_at
            })
    print(all_reels)
    return render_template('reelHistory.html', reels=all_reels)

@app.route('/delete/<int:id>', methods=['POST'])
@signin_required
def delete_reel(id) :
    reel = Reel.query.get_or_404(id) # means check in db this id present if yes give or show 404 error

    #now delete the reel from the reel_database which matches the id
    db.session.delete(reel) # DELETE FROM reel WHERE id = id(given by us)
    db.session.commit()

    return redirect(url_for('reel_history'))

@app.route('/blog-generator', methods=['GET','POST'])
@signin_required
def blogGenerator() :
    if request.method == 'POST' :
        return createBlog()
    
    id = request.args.get('id', type=int)

    return render_template("blogGenerator.html", blog_id=id)

@app.route('/blog-status/<int:id>')
def blog_status(id) :
    blog = History.query.filter_by(id=id).first()

    return {
        "status":blog.status,
        "response": blog.response if blog.response else None
    }

@app.route('/captions-generator', methods=['GET','POST'])
@signin_required
def captionGenerator() :
    if request.method == 'POST' :
        return createCaptions()
    
    id = request.args.get('id', type=int)

    return render_template("captionsGen.html", caption_id=id)

@app.route('/caption-status/<int:id>')
def caption_status(id) :
    caption = History.query.filter_by(id=id).first()
    
    return {
        "status":caption.status,
        "response": json.loads(caption.response) if caption.response else None
    }

@app.route('/hashtag-generator', methods=['GET','POST'])
@signin_required
def hashtagGenerator() :
    if request.method == 'POST' :
        return createHashtags()
    
    #
    id = request.args.get('id', type=int)

    return render_template("hashtagGen.html", hashtag_id=id)

@app.route('/hashtag-status/<int:id>')
def hashtag_status(id) :
    hashtag = History.query.filter_by(id=id).first()
    
    return {
        "status":hashtag.status,
        "response": json.loads(hashtag.response) if hashtag.response else None
    }

@app.route('/video-script-gen', methods=['GET','POST'])
@signin_required
def videoScriptsGen() :
    if request.method == 'POST' :
        return createVideoScripts()
    
    id = request.args.get('id', type=int)

    return render_template("videoScriptsGen.html", video_script_id=id)

@app.route('/video-script-status/<int:id>')
def video_script_status(id) :
    video_script = History.query.filter_by(id=id).first()
    
    return {
        "status":video_script.status,
        "response": video_script.response if video_script.response else None
    }

@app.route('/history')
@signin_required
def history() :
    histories = History.query.filter_by(user_id=session.get('user_id')).order_by(History.created_at.desc()).limit(50).all()
    all_history = []
    for history in histories :
        if history.status == 'completed' :
            all_history.append({
                'topic': history.topic,
                'tag': history.tag,
                'created_at' : history.created_at 
            })
    print(all_history)
    return render_template('history.html', histories=all_history)

if __name__ == '__main__' :
    app.run()