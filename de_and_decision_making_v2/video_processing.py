import cv2
import numpy as np
from PIL import Image
import torch
from find_brightest_region import FindBrightestRegion
from serial_write import SerialWrite

class VideoProcessing:
    @staticmethod
    def video_processing(frame, model, device, transform, arduino):
        input_batch = transform(frame).to(device)
        with torch.no_grad():
            prediction = model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=(frame.shape[0], frame.shape[1]),
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        output = prediction.cpu().numpy()
        formatted = (output * 255 / np.max(output)).astype("uint8")
        depth = cv2.cvtColor(np.array(Image.fromarray(formatted)), cv2.COLOR_GRAY2BGR)
        direction = FindBrightestRegion.find_brightest_region(depth)
        if direction == "LEFT":
            SerialWrite.serial_write(arduino, 120, 60) 
        elif direction == "RIGHT":
            SerialWrite.serial_write(arduino, 60, 120) 
        else:
            SerialWrite.serial_write(arduino, 120, 120)

        try:
            cv2.imshow("Frame", depth)
        except:
            pass