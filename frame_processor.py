import cv2
import numpy as np

class FrameProcessor:
    def __init__(self):
        pass

    def process_frame(self, frame, threshold_value, contour_color, line_color):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to the grayscale image
        blur = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        
        # Apply thresholding to the blurred image
        _, threshold = cv2.threshold(gray_frame, threshold_value, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours on the blurred image
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours based on circularity, handling division by zero
        contours = sorted(contours, key=lambda x: cv2.contourArea(x) / cv2.arcLength(x, True) if cv2.arcLength(x, True) > 0 else 0, reverse=True)

        # Initialize height variable
        height = None

        # Check if there are at least two contours
        if len(contours) >= 2:
            # Calculate bounding box of the contour
            x, y, w, h = cv2.boundingRect(contours[0])
            
            # Calculate the height of the contour
            height = h

            # Draw the contours
            cv2.drawContours(frame, [contours[0]], -1, contour_color, 3)

            # Calculate the center point of the contour
            center_x = x + w // 2
            center_y = y + h // 2

            # Draw a vertical line passing through the center point
            cv2.line(frame, (center_x, y), (center_x, y + h), line_color, 2)
        
        return frame, height
