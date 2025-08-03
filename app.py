from flask import Flask, render_template, request, redirect, url_for, session, Response
from ultralytics import YOLO
import cv2

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load YOLO model
model = YOLO("model.pt")

def check_credentials(username, password):
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[0] == username and parts[1] == password:
                    return True
    except FileNotFoundError:
        return False
    return False

def user_exists(username):
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                if line.split(':')[0] == username:
                    return True
    except FileNotFoundError:
        return False
    return False

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Run YOLO detection
            results = model.predict(frame, conf=0.5)
            
            # Render detections
            annotated_frame = results[0].plot()
            
            # Convert to JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Routes

@app.route('/')
def index():
    return redirect(url_for('intro'))

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if check_credentials(username, password):
            session['logged_in'] = True
            return redirect(url_for('home'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error = 'Passwords do not match'
        elif user_exists(username):
            error = 'Username already exists'
        else:
            with open('users.txt', 'a') as f:
                f.write(f'{username}:{password}\n')
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to login page after logout


@app.route('/webcam')
def webcam():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('webcam.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
