import cv2
import numpy as np

# Function to calculate brightness of a frame
def calculate_brightness(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate mean brightness
    brightness = np.mean(gray)
    return brightness

# Function to find the brightest region
def find_brightest_region(frame):
    # Divide the frame into three regions (left, middle, right)
    height, width = frame.shape[:2]
    third_width = width // 3

    # Calculate brightness of each region
    left_brightness = calculate_brightness(frame[:, :third_width])
    middle_brightness = calculate_brightness(frame[:, third_width:2*third_width])
    right_brightness = calculate_brightness(frame[:, 2*third_width:])

    # Find the region with the least brightness
    min_brightness = min(left_brightness, middle_brightness, right_brightness)

    # Determine direction based on the brightest region
    if min_brightness == left_brightness:
        direction = "LEFT"
    elif min_brightness == right_brightness:
        direction = "RIGHT"
    else:
        direction = "STRAIGHT"

    return direction

# Open video capture
cap = cv2.VideoCapture('/Users/aatmaj/sem-VI-mini-project/midas.mp4')

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))


while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # Find the brightest region
    direction = find_brightest_region(frame)

    # Display direction
    cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow('Frame', frame)

    # Write the frame to the output video
    out.write(frame)
    # Exit if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    cv2.waitKey(0)

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
