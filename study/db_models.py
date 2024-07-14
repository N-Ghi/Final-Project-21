from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    profile = db.relationship('Profile', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def get_id(self):
        return self.username

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username', ondelete='CASCADE', onupdate='CASCADE', name='fk_profile_user_username'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    strong_subjects = db.Column(db.String(255), nullable=False) 
    weak_subjects = db.Column(db.String(255), nullable=False)  
    primary_language = db.Column(db.String(50), nullable=False)
    secondary_languages = db.Column(db.String(200))
    days = db.Column(db.String(50), nullable=False)
    times = db.Column(db.String(50), nullable=False)
    strong_subjects = db.Column(db.String(255), nullable=False)
    weak_subjects = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', back_populates='profile')