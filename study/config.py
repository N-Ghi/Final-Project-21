class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///study.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'goodliferda@gmail.com'
    MAIL_PASSWORD = 'goodlife@2024'
    MAIL_DEFAULT_SENDER = 'no-reply@studybuddy.com'
    
    SECRET_KEY = 'your_secret_key'