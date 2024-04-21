import cv2
import numpy as np

class CalculateBrightness:
    @staticmethod
    def calculate_brightness(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        return brightness