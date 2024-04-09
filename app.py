import cv2
from flask import Flask, request, jsonify
import numpy as np
from frame_processor import FrameProcessor
import base64
import math
import io
import os
import random

app = Flask(__name__)
frame_processor = FrameProcessor()
current_wc_img = ''


baseline_pir_range_low = 4/12
baseline_pir_range_high = 8/12

@app.route('/adapt-ui', methods=['POST'])
def upload_image():
    data = request.get_json()
    base64_pir_image = data.get('pir_image')
    
    PIR = calculate_PIR(base64_pir_image)

    adjustment = adjust_value(PIR)
    
    base64_webcam_image = data.get('webcam_image')
    
    brightness = calculate_brightness(base64_webcam_image)

    return jsonify({'PIR': PIR, 'adjustment': adjustment, 'brightness': brightness})



@app.route('/adapt-ui2', methods=['GET'])
def get_current_frames():

    base64_pir_image = select_random_enc_image('encoded_img')
    
    PIR = calculate_PIR(base64_pir_image)

    adjustment = adjust_value(PIR)
    
    capture_and_save_frame()

    base64_webcam_image = current_wc_img
    # print(base64_webcam_image)
    
    brightness = calculate_brightness(current_wc_img)

    return jsonify({'PIR': PIR, 'adjustment': adjustment, 'brightness': brightness})


def select_random_enc_image(folder_path):
    # List all files in the specified folder
    files = os.listdir(folder_path)
    
    # Filter the list to include only image files
    # This example assumes common image file extensions; adjust as needed
    image_files = [file for file in files if file.endswith(('.txt'))]
    
    # Check if there are any image files in the folder
    if not image_files:
        print("No image files found in the folder.")
        return None
    
    # Select a random image file
    random_image = random.choice(image_files)
    
    # Return the full path of the random image
    full_path = os.path.join(folder_path, random_image)

    # Read the content of the .txt file
    with open(full_path, 'r') as file:
        content = file.read()
    
    # Return the content of the random .txt file
    return content



def capture_and_save_frame():
    # Open the default camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Capture a single frame
    ret, frame = cap.read()

    # Check if frame is captured successfully
    if not ret:
        raise IOError("Cannot capture frame")

    # Encode the frame as a JPEG image
    is_success, buffer = cv2.imencode(".jpg", frame)
    if not is_success:
        raise IOError("Cannot encode frame")

    # Convert the byte stream to a BytesIO object
    image_bytes = io.BytesIO(buffer)
    current_wc_img = image_bytes.getvalue()
    print(current_wc_img)


def adjust_value(ratio):
    # The mid_range is considered as the baseline for optimal PIR
    baseline = 0.5
    window_size = 0.0833
    
    # Calculate the difference from the baseline
    difference = ratio - baseline
    
    # Determine the direction of adjustment (positive or negative)
    if difference >= 0:
        direction = 1  # Positive adjustment
    else:
        direction = -1  # Negative adjustment
    
    # Calculate the number of windows away from the baseline
    windows_away = math.ceil(abs(difference) / window_size)
    
    # Adjust the value based on the direction and number of windows away
    adjusted_value = direction * windows_away
    
    return adjusted_value

def calculate_PIR(base64_image):
    
    image_data = base64.b64decode(base64_image)

    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode numpy array to image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process frame using FrameProcessor class
    _, pupil_diameter = frame_processor.process_frame(img, 50, (0, 0, 255), (0, 255, 0))
    _, iris_diameter = frame_processor.process_frame(img, 120, (0, 0, 255), (0, 255, 0))

    return pupil_diameter/iris_diameter

def calculate_brightness(image_data):

    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate mean pixel value (brightness) of the grayscale image
    brightness = np.mean(gray_image)
    
    # Normalize brightness value to range from 0 to 100
    brightness_normalized = (brightness / 255) * 100
    
    return brightness_normalized

if __name__ == '__main__':
    app.run(debug=True)
