import cv2
import mediapipe as mp
import time
from flask_socketio import SocketIO, emit



# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


    
def generate_frames(socketio):
    gesture_recognition = GestureRecognition(socketio)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                gesture = gesture_recognition.detect_gesture(hand_landmarks)
                gesture_recognition.update_gesture(gesture)
                duration = gesture_recognition.gesture_duration
                           
                if duration >= 5:
                    gesture_recognition.reset_duration()
                    # gesture_recognition.send_gesture_to_server(gesture)
                    gesture_recognition.on_gesture_detected(gesture)
                    

                
                cv2.putText(frame, f"{gesture} ({duration:.2f} seconds)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()





class GestureRecognition:
    def __init__(self, socketio):
        self.socketio = socketio
        self.current_gesture = None
        self.gesture_start_time = None
        self.gesture_duration = 0

    def update_gesture(self, new_gesture):
        if new_gesture != self.current_gesture:
            self.current_gesture = new_gesture
            self.gesture_start_time = time.time()
            self.gesture_duration = 0
        else:
            self.gesture_duration = time.time() - self.gesture_start_time

        return self.current_gesture, self.gesture_duration

    def detect_gesture(self, hand_landmarks):
        # Analyze hand_landmarks to determine the gesture
        extended_fingers = self.count_extended_fingers(hand_landmarks)
        
        if extended_fingers <= 1:
            return 'Rock'
        elif extended_fingers >= 4:
            return 'Paper'
        else:
            return 'Scissors'

    def count_extended_fingers(self, hand_landmarks):
        fingertip_indices = [4, 8, 12, 16, 20]
        joint_indices = [3, 6, 10, 14, 18]
        extended_fingers = 0

        for fingertip, joint in zip(fingertip_indices, joint_indices):
            if hand_landmarks.landmark[fingertip].y < hand_landmarks.landmark[joint].y:
                extended_fingers += 1

        return extended_fingers
    
    def reset_duration(self):
        self.current_gesture = None
        self.gesture_start_time = None
        self.gesture_duration = 0
        
    def on_gesture_detected(self, gesture):
        print(f"handcam.py sees {gesture}")
        self.socketio.emit('gesture_detected', {'gesture': gesture})
        return gesture
    
    # def send_gesture_to_server(self, gesture):
    #     url = 'http://127.0.0.1:5000/handle_gesture'
    #     headers = {'Content-Type': 'application/json'}
    #     data = {'gesture': gesture}
    #     try:
    #         response = requests.post(url, json=data, headers=headers)
    #         if response.status_code == 200:
    #             response_json = response.json()
    #             print("Response JSON:", response_json)
    #         else:
    #             print("Error sending gesture:", response.status_code, response.text)
    #     except requests.RequestException as e:
    #         print("Error sending gesture to server:", e)





