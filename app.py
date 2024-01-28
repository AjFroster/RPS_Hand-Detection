from flask import Flask, request, render_template, session, Response, jsonify, redirect, url_for
import rps
from handcam import generate_frames  # Importing the generate_frames function
from flask_socketio import SocketIO, emit
from threading import Thread

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# App Initialization
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for production


# App Routing
# Home Route
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_score' not in session:
        session['user_score'] = 0
        session['computer_score'] = 0

    return render_template('index.html', user_score=session['user_score'], computer_score=session['computer_score'])

# Handles HTML Webcam Video Reed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(socketio), mimetype='multipart/x-mixed-replace; boundary=frame')

# Handles gesture detected from handcam
@app.route('/handle_gesture', methods=['POST'])
def handle_gesture():
    print("handle_gesture entered.")
    # Extract data from the POST request 
    gesture_data = request.json
    player_gesture = gesture_data.get('gesture')
    
    print(f"Flask sees {player_gesture}" )
    
    result = rps.play_game(player_gesture)
    print(result)
    if "win" in result.lower():
        session['user_score'] += 1
    elif "lose" in result.lower():
        session['computer_score'] += 1
    else:
        pass
        
    print(f"user = {session['user_score']}, computer = {session['computer_score']}")
    return render_template('index.html', user_score=session['user_score'], computer_score=session['computer_score'])

    # Redirect to the result page
    # return redirect(url_for('show_result', result=result))

# Shows result 
@app.route('/result/<result>')
def show_result(result):
    # Render the result.html template with the result
    return render_template('result.html', result=result)






if __name__ == '__main__':
    app.run(debug=True)
