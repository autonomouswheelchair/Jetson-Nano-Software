import os
import torch
from transformers import DPTImageProcessor, DPTForDepthEstimation
import cv2
import numpy as np
from PIL import Image

model_name = "Intel/dpt-hybrid-midas"
model_dir = "/models"  # Change this to the directory where the volume is mounted

# Create the models directory if it doesn't exist
os.makedirs(model_dir, exist_ok=True)

# Check if the model exists in the model directory
if not os.path.exists(os.path.join(model_dir, model_name)):
    # If not, download the model
    model = DPTForDepthEstimation.from_pretrained(model_name)
    processor = DPTImageProcessor.from_pretrained(model_name)
    # Save the model and processor
    model.save_pretrained(os.path.join(model_dir, model_name))
    processor.save_pretrained(os.path.join(model_dir, model_name))
else:
    # If it does, load the model and processor from the directory
    model = DPTForDepthEstimation.from_pretrained(os.path.join(model_dir, model_name))
    processor = DPTImageProcessor.from_pretrained(os.path.join(model_dir, model_name))

# Get the current working directory
current_directory = os.getcwd()

# Construct the path to the video file
video_path = os.path.join(current_directory, "c_b407_video.mp4")

# Now you can use video_path to access the video file
print("Video path:", video_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(torch.cuda.is_available())

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

current_frame = 0
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break

    # Convert frame to PIL Image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Prepare image for the model
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        # Get depth prediction
        outputs = model(**inputs)
        predicted_depth = outputs.predicted_depth

    # Interpolate to original size
    prediction = torch.nn.functional.interpolate(
        predicted_depth.unsqueeze(1),
        size=image.size[::-1],
        mode="bicubic",
        align_corners=False,
    )

    # Move prediction tensor to CPU for visualization
    prediction = prediction.cpu()

    # Visualize the prediction
    output = prediction.squeeze().numpy()
    formatted = (output * 255 / np.max(output)).astype("uint8")
    depth = cv2.cvtColor(np.array(Image.fromarray(formatted)), cv2.COLOR_GRAY2BGR)

    # Write the depth-enhanced frame to the output video
    out.write(depth)

    current_frame += 1
    if current_frame % 2 == 0:  # Print every 10 frames to reduce overhead
        print(f'Processed frame {current_frame} of {frame_count}')
        break

# Release the video file and writer object, and close windows
cap.release()
out.release()
cv2.destroyAllWindows()
