from flask_sqlalchemy import SQLAlchemy
import bcrypt 

db = SQLAlchemy()

#Parent Class
class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password) :
        self.password = bcrypt.hashpw( 
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password) :
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )

#Child Class: 1
class Reel(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), nullable=False)
    user_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    video_path = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.String(50), nullable=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def set_status(self, status) :
        self.status = status

    def set_video_path(self, video_path) :
        self.video_path = video_path

    def set_created_at(self, created_at) :
        self.created_at = created_at


#Child Class: 2
class History(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def set_status(self, status) :
        self.status = status
    
    def set_created_at(self, created_at) :
        self.created_at = created_at

    def set_response(self, response) :
        self.response = response
