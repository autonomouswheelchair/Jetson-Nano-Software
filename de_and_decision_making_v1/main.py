from video_processor import VideoProcessor
from transformers import DPTImageProcessor, DPTForDepthEstimation
import os

class Main:
    def __init__(self):
        self.model_name = "Intel/dpt-swinv2-tiny-256"
        self.model_dir = "/models"
        os.makedirs(self.model_dir, exist_ok=True)

        if not os.path.exists(os.path.join(self.model_dir, self.model_name)):
            self.model = DPTForDepthEstimation.from_pretrained(self.model_name)
            self.processor = DPTImageProcessor.from_pretrained(self.model_name)
            self.model.save_pretrained(os.path.join(self.model_dir, self.model_name))
            self.processor.save_pretrained(os.path.join(self.model_dir, self.model_name))
        else:
            self.model = DPTForDepthEstimation.from_pretrained(os.path.join(self.model_dir, self.model_name))
            self.processor = DPTImageProcessor.from_pretrained(os.path.join(self.model_dir, self.model_name))

        self.current_directory = os.getcwd()
        self.video_path = os.path.join(self.current_directory, "c_b407_video.mp4")
        self.output_path = "output_swinv2_tiny.mp4"

    def run(self):
        processor = VideoProcessor(self.model, self.processor, self.video_path, self.output_path)
        processor.process_video()

if __name__ == "__main__":
    app = Main()
    app.run()
