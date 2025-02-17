import cv2
import mediapipe as mp
import numpy as np
import pickle
import time
import os
from pathlib import Path

global base_dir
base_dir = Path(os.getcwd()).as_posix()  # Converts to a forward-slash path
asl_model = f"{base_dir}/sign_detection/asl_model.pkl"
output_txt = f"{base_dir}/detected_letters.txt"  # File to save detected letters
open(output_txt, "w").close()  # Clears the file at the start

def asl_rec():

    # Load the trained ASL model
    with open(asl_model, "rb") as f:
        model, label_encoder = pickle.load(f)

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # OpenCV Video Capture (Webcam)
    cap = cv2.VideoCapture(0)

    # Variables to track detected letters and time
    current_letter = None
    letter_start_time = None
    confirmed_letters = []

    def save_detected_letter(letter):
        if letter not in confirmed_letters:
            confirmed_letters.append(letter)
            print(f"Saved letter: {letter}")
            
            # Append detected letters to the file
            with open(output_txt, "a") as f:
                f.write(letter)  # Appends new letters instead of overwriting

    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                # print("Ignoring empty frame")
                continue

            # Convert frame to RGB (MediaPipe requires RGB input)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # Extract hand landmarks if detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Extract landmark features
                    landmark_list = []
                    for lm in hand_landmarks.landmark:
                        landmark_list.append(lm.x)
                        landmark_list.append(lm.y)
                        landmark_list.append(lm.z)

                    # Convert to NumPy array and reshape
                    landmark_array = np.array(landmark_list).reshape(1, -1)

                    # Predict ASL gesture
                    predicted_class = model.predict(landmark_array)
                    predicted_label = label_encoder.inverse_transform(predicted_class)[0]

                    # Check if the letter remains the same for at least 1 seconds
                    if predicted_label == current_letter:
                        if time.time() - letter_start_time >= 1:
                            save_detected_letter(predicted_label)
                    else:
                        current_letter = predicted_label
                        letter_start_time = time.time()

                    # Display prediction on screen
                    cv2.putText(frame, f"ASL: {predicted_label}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Flip the image for a selfie-view display
            cv2.imshow('ASL Real-Time Recognition', cv2.flip(frame, 1))

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    
    with open(output_txt, "r") as f:
        final_text = f.read().strip()  # Read final detected letters

    return final_text  # Return the detected text
