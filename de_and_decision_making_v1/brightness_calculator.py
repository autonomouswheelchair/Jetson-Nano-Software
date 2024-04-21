import cv2
import numpy as np

class BrightnessCalculator:
    @staticmethod
    def calculate_brightness(frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate mean brightness
        brightness = np.mean(gray)
        # print(f'gray: {gray}, brightness: {brightness}')
        return brightness
