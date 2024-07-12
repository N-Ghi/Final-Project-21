from flask import *
from study.forms import *
from study.db_models import *

def flash_message(message, category):
    flash(message, category)
#APP routes
def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')
    
    #Register Route
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            
            if existing_user:
                flash_message('Username or email already exists. Please choose a different one.', 'danger')
                return render_template('register.html', form=form)
            else:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash_message('User registered successfully!', 'success')
                session['username'] = new_user.username
                return redirect(url_for('profile'))
        return render_template('register.html', form=form)
    
    #Login Route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['username'] = user.username
                flash_message('User logged in successfully!', 'success')
                if user.profile:
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('profile'))
            else:
                flash_message('Invalid username or password. Please try again.', 'danger')
                return render_template('login.html', form=form)
        return render_template('login.html', form=form)
    
    #Profile Route
    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'username' not in session:
            return redirect(url_for('login'))

        user = User.query.filter_by(username=session['username']).first()
        if user.profile:
            return redirect(url_for('dashboard'))
        
        form = ProfileForm()

        if form.validate_on_submit():
            school = form.school.data
            primary_language = form.primary_language.data
            secondary_languages = form.secondary_languages.data
            days = form.days.data
            times = form.times.data
            strong_subjects = form.strong_subjects.data
            weak_subjects = form.weak_subjects.data

            new_profile = Profile(school=school,
                                  primary_language=primary_language, secondary_languages=secondary_languages,
                                  days=days, times=times
                                  , strong_subjects=",".join(form.strong_subjects.data),
                                  weak_subjects=",".join(form.weak_subjects.data))
            db.session.add(new_profile)
            db.session.commit()
            flash_message('Profile created successfully!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('profile.html', form=form)
    
    #Dashboard Route
    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('dashboard.html')