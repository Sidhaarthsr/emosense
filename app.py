import cv2
from flask import Flask, request, jsonify
import numpy as np
from frame_processor import FrameProcessor
import base64
import math

app = Flask(__name__)
frame_processor = FrameProcessor()

baseline_pir_range_low = 4/12
baseline_pir_range_high = 8/12

@app.route('/pir', methods=['POST'])
def upload_image():
    data = request.get_json()
    base64_image = data.get('image')
    PIR = calculate_PIR(base64_image)
    
    adjustment = adjust_value(PIR)

    return jsonify({'PIR': PIR, 'adjustment': adjustment})


def adjust_value(ratio):
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

if __name__ == '__main__':
    app.run(debug=True)
