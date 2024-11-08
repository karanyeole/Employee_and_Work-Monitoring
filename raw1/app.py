from flask import Flask, render_template, Response, request, jsonify, session,redirect, url_for
from flask_session import Session
import threading
import cv2
import capture_img
import train  # Assuming train.py contains the trainer function
import os
from train import fetch_games

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize the session
Session(app)

cap = cv2.VideoCapture(0)
training_status = {'status': 'not_started'}

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return redirect(url_for('get_names'))

@app.route('/get_names')
def get_names():
    print("get_names route accessed")
    games = fetch_games()  # Fetching game data using the function from train.py
    print("Games fetched:", games)  # Debug line
    return render_template('index.html', games=games)


@app.route('/new_user_registration')
def new_user_registration():
    return render_template('new_user_registration.html')

@app.route('/capture_image', methods=['POST'])
def capture_image():
    full_name = request.form.get('full_name')
    session['full_name'] = full_name  # Store full_name in session
    threading.Thread(target=capture_img.capture_images, args=(cap, 'person'+"/"+full_name, 10, full_name)).start()
    return render_template('capture_image.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def training_thread(full_name):
    global training_status
    training_status['status'] = 'in_progress'
    train.trainer(full_name)
    training_status['status'] = 'completed'

@app.route('/start_training', methods=['POST'])
def start_training():
    full_name = session.get('full_name')  # Retrieve full_name from session
    if full_name:
        threading.Thread(target=training_thread, args=(full_name,)).start()  # Start the training thread
        return jsonify({'status': 'started'})
    else:
        return jsonify({'status': 'error', 'message': 'Full name not found in session'}), 400

@app.route('/check_training_status', methods=['GET'])
def check_training_status():
    return jsonify(training_status)

@app.route('/wait')
def wait():
    return render_template('wait.html')

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    selected_game = request.form.get('game')
    print(f"Selected game: {selected_game}")
    # Call your function to start monitoring with the selected game
    # start_monitoring(selected_game) # Replace with your actual function
    return jsonify({'status': 'started', 'game': selected_game})

if __name__ == '__main__':
    app.run(debug=True)
