from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from prediction import predict_class
import pandas as pd 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random string in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
db = SQLAlchemy(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login1.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        user_text = request.form['user_text']
        # Pass the user input to the backend script and get the result
        predicted_class, class_probs = predict_class(user_text)
        return render_template('dashboard1.html', user_text=user_text, predicted_class=predicted_class, class_probs=class_probs)
    return render_template('dashboard1.html')

@app.route('/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    try:
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('dashboard'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('dashboard'))
        
        if file and file.filename.endswith('.csv'):
            # Read the CSV file
            df = pd.read_csv(file)

            if 'text' not in df.columns:
                flash('CSV file must contain a "text" column.', 'error')
                return redirect(url_for('dashboard'))
            
            results = []
            for _, row in df.iterrows():
                text = row['text']
                predicted_class, class_probs = predict_class(text)
                results.append({
                    'text': text,
                    'suicidal_prob': class_probs['suicidal'] * 100,  # Convert to percentage
                    'non_suicidal_prob': class_probs['non-suicidal'] * 100  # Convert to percentage
                })

            return render_template('dashboard1.html', batch_results=results)

        flash('Invalid file format. Please upload a CSV file.', 'error')
        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

#Routing for the Quiz part
@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    answers = [
        int(request.form.get('q1',0)),
        int(request.form.get('q2',0)),
        int(request.form.get('q3',0)),
        int(request.form.get('q4',0)),
        int(request.form.get('q5',0)),
        int(request.form.get('q6',0)),
        int(request.form.get('q7',0)),
        int(request.form.get('q8',0)),
        int(request.form.get('q9',0)),
        int(request.form.get('q10',0)),
        
    ]
    total_score = sum(answers)

    if total_score<= 9:
        interpretation = "You are unlikely to be experiencing depression."
    elif total_score <= 18:
        interpretation = "You may be experiencing mild depression. It's a good idea to talk to a mental health professional."
    elif total_score <= 24:
        interpretation = "You may be experiencing moderate depression. It's recommended that you seek help from a mental health professional."
    else:
        interpretation = "You may be experiencing severe depression. It's essential that you seek help from a mental health professional as soon as possible."
    
    return render_template('result.html', score=total_score, interpretation=interpretation)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables before running the app
    app.run(host='0.0.0.0', port=8000, debug=True)
