import platform
from check_system import CheckSystem
from initialize_model import InitializeModel
from video_processing import VideoProcessing
import cv2, torch

class Main:
    def input(os_name):
        locations = ['B101', 'b101', 'B102', 'b102', 'B103', 'b103', 'B104', 'b104', 'B105', 'b105', 'B106', 'b106', 'B107', 'b107', 'B108', 'b108',
                    'B109', 'b109', 'B110', 'b110', 'B111', 'b111', 'B112', 'b112', 'B113', 'b113', 'B114', 'b114', 'B115', 'b115', 'B116', 'b116',
                    'B117', 'b117', 'B118', 'b118', 'B119', 'b119', 'Foyer', 'foyer', 'Library', 'library']
        while True:
            start_location = input('\n\n\nEnter Start Location: ')
            end_location = input('Enter Goal Location: ')
            if start_location not in locations:
                print('Start Location not found. Please enter again.')
            elif end_location not in locations:
                print('End Location not found. Please enter again.')
            else:
                break

        option = int(input('Enter \'1\' for default Port Number, Baud Rate and Time Out for Arduino Board and default Port Number for RPLIDAR else \'0\': '))
        print(os_name)
        
        if option == 1:
            if os_name == 'Windows':
                rplidar_port = 'COM3'
                arduino_port = 'COM4'
            elif os_name == 'Linux':
                rplidar_port = '/dev/ttyUSB0'
                arduino_port = '/dev/ttyACM0'
            baudrate = 9600
            timeout = .1
        else:        
            rplidar_port = input('Enter Port of Computer to which the RPLIDAR is connected: ')
            arduino_port = input('Enter Port of Computer to which the Arduino Board is connected: ')
            baudrate = int(input('Enter the Baudrate: '))
            timeout = float(input('Enter the timeout: '))
        
        return (start_location, end_location, rplidar_port, arduino_port, baudrate, timeout)

    def main():
        
        print('---------------------------------------------------------------------------------------------------------------------------')
        print('-------------------------------------------- AUTONOMOUS MANEUVERING WHEELCHAIR --------------------------------------------')
        print('--------------------------------------------          SYSTEM PROGRAM           --------------------------------------------')
        print('---------------- AUTHORS: AATMAJ K. MHATRE aatmaj.m@somaiya.edu, SUSHANT M. NAIR sushant.nair@somaiya.edu -----------------')
        print('----------------        PROJECT GUIDE: DR. PRASANNA J. SHETE, DEPARTMENT OF COMPUTER ENGINEERING          -----------------')
        print('---------------- © K J SOMAIYA COLLEGE OF ENGINEERING, SOMAIYA VIDYAVIHAR UNIVERSITY, ALL RIGHTS RESERVED -----------------')
        print('---------------------------------------------------------------------------------------------------------------------------')
        print('---------------------------------------------------------------------------------------------------------------------------')
        print('---------------------------------------------------------------------------------------------------------------------------')

        os_name = platform.system()
        start_location, end_location, rplidar_port, arduino_port, baudrate, timeout = input(os_name)

        arduino, return_value = CheckSystem.check_system(os_name, rplidar_port, arduino_port, baudrate, timeout)
        print(f'System Check Result: {return_value}, arduino: {arduino}')
        if return_value:
            model, device = InitializeModel.initialize_model()
            print(f'model: {model}, device: {device}')
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
            transform = midas_transforms.small_transform
            video_capture = cv2.VideoCapture(0)
            print(f'midas_transforms: {midas_transforms}, transform: {transform}, vieo_capture: {video_capture}')

            while True:
                ret, frame = video_capture.read()
                print(f'ret: {ret}, frame: {frame}')
                if not ret:
                    break
                VideoProcessing.video_processing(frame, model, device, transform, arduino)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            video_capture.release()
            cv2.destroyAllWindows()
        else:
            print(f'Please check the system_check_log.csv file, correct the fault and try again.')

if __name__ == "__main__":
    Main.main()