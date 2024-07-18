from flask import *
from study.forms import *
from study.db_models import *
from flask_login import login_required, current_user, login_user, logout_user
from study import *

def flash_message(message, category):
    flash(message, category)

# APP routes
def register_routes(app):
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')

    # Register Route
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

            new_user = User(username=username, email=email, password=password, confirmed=False)
            db.session.add(new_user)
            db.session.commit()
            send_confirmation_email(new_user.email)
            flash_message('A confirmation email has been sent via email. Please confirm your email to log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)
    
    # Email Confirmation Route
    @app.route('/confirm/<token>')
    def confirm_email(token):
        try:
            email = confirm_token(token)
        except:
            flash_message('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('resend_confirmation'))

        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash_message('Account already confirmed. Please log in.', 'success')
        else:
            user.confirmed = True
            db.session.commit()
            flash_message('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('login'))
    
    # Re-send Confirmation Route
    @app.route('/resend_confirmation', methods=['GET', 'POST'])
    def resend_confirmation():
        form = ResendConfirmationForm()
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            if user and not user.confirmed:
                send_confirmation_email(user.email)
                flash_message('A new confirmation email has been sent.', 'success')
            else:
                flash_message('Email not found or already confirmed.', 'danger')
        return render_template('resend_confirmation.html', form=form)
    
    # Login Route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                if not user.confirmed:
                    flash_message('Please confirm your email address first.', 'warning')
                    return redirect(url_for('resend_confirmation'))
                login_user(user)
                flash_message('User logged in successfully!', 'success')
                return redirect(url_for('dashboard' if user.profile else 'profile'))
            else:
                flash_message('Invalid username or password. Please try again.', 'danger')
                return render_template('login.html', form=form)
        return render_template('login.html', form=form)

    # Create Profile Route
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        user = User.query.filter_by(username=current_user.username).first()
        if user.profile:
            return redirect(url_for('dashboard'))

        form = ProfileForm()
        if form.validate_on_submit():
            new_profile = Profile(
                username=user.username,
                school=form.school.data,
                primary_language=form.primary_language.data,
                secondary_languages=",".join(form.secondary_languages.data),
                days=",".join(form.days.data),
                times=",".join(form.times.data),
                strong_subjects=",".join(form.strong_subjects.data),
                weak_subjects=",".join(form.weak_subjects.data)
            )
            db.session.add(new_profile)
            db.session.commit()
            flash('Profile created successfully!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('profile.html', form=form)
    
    # Update Profile Route
    @app.route('/profile/update', methods=['GET', 'POST'])
    @login_required
    def profileupdate():

        user = Profile.query.filter_by(username=current_user.username).first_or_404()
        form=ProfileForm(obj=user)

        if form.validate_on_submit():
            user.school = form.school.data
            user.primary_language = form.primary_language.data
            user.secondary_languages = ",".join(form.secondary_languages.data)
            user.days = ",".join(form.days.data)
            user.times = ",".join(form.times.data)
            user.strong_subjects = ",".join(form.strong_subjects.data)
            user.weak_subjects = ",".join(form.weak_subjects.data)
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile'))

        return render_template('updateprofile.html', form=form, user=user)
    
    # View Profile Route
    @app.route('/profile/view')
    @login_required
    def view_profile():
        user = Profile.query.filter_by(username=current_user.username).first_or_404()
        email = User.query.filter_by(username=current_user.username).first().email
        return render_template('view_profile.html', user=user, email=email)
    
    # Delete Profile Route
    @app.route('/profile/delete', methods=['GET','POST'])
    @login_required
    def delete_profile():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        flash_message('Your profile has been deleted!', 'success')
        return redirect(url_for('home'))
    
    # Dashboard Route
    @app.route('/dashboard')
    @login_required
    def dashboard():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        if not current_user.confirmed:
            flash_message('Please confirm your account!', 'warning')
            return redirect(url_for('resend_confirmation'))
        return render_template('dashboard.html', user=user)
    
    # Logout Route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash_message('Logged out successfully!', 'success')
        return redirect(url_for('home'))