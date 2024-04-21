from brightest_region_finder import BrightestRegionFinder
import numpy as np
import torch
import cv2
from PIL import Image
import time

class VideoProcessor:
    def __init__(self, model, processor, video_path, output_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.processor = processor
        self.video_path = video_path
        self.output_path = output_path

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print(f'cap: {cap}, fps: {fps}, frame_count: {frame_count}, width: {width}, height: {height}')

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))
        print(f'fourcc: {fourcc}, out: {out}')
        current_frame = 0
        start = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            # print(f'ret: {ret}, frame: {frame}')
            if not ret:
                break
            
            if current_frame % 1 == 0:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                inputs = self.processor(images=image, return_tensors="pt").to(self.device)

                # print(f'image: {image}, inputs: {inputs}')

                with torch.no_grad():
                    outputs = self.model(**inputs)
                    predicted_depth = outputs.predicted_depth
                    # print(f'outputs: {outputs}, predicted_depth: {predicted_depth}')

                prediction = torch.nn.functional.interpolate(
                    predicted_depth.unsqueeze(1),
                    size=image.size[::-1],
                    mode="bicubic",
                    align_corners=False,
                )

                prediction = prediction.cpu()
                output = prediction.squeeze().numpy()
                formatted = (output * 255 / np.max(output)).astype("uint8")
                depth = cv2.cvtColor(np.array(Image.fromarray(formatted)), cv2.COLOR_GRAY2BGR)
                direction = BrightestRegionFinder.find_brightest_region(depth)
                cv2.putText(depth, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # print(f'formatted: {formatted}, depth: {depth}, direction: {direction}')
                out.write(depth)
                cv2.imshow('Frame', depth)
                cv2.waitKey(1)

                print(f'Processed frame {current_frame} of {frame_count}')

            current_frame += 1

        end = time.time()
        print(f'Execution time: {end - start} s')
        print(f'Speed: {current_frame / (end - start)} FPS')

        cap.release()
        out.release()
