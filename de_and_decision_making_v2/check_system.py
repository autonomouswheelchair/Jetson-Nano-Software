import os
import datetime
import csv
import psutil
import serial
from rplidar import RPLidar
import cv2

class CheckSystem:
    @staticmethod
    def check_system(os_name, rplidar_port, arduino_port, baudrate, timeout):
        return_value = True
        # Define the log file path
        if os_name == "Windows":
            log_file_path = "D:/system_check_log.csv"

        # Check if the log file exists and create it with headers if it doesn't
        if not os.path.isfile(log_file_path):
            with open(log_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Sr. No.", "Date of Performance", "Time of Performance", "Battery Status", "CPU Status", "RPLIDAR Status", "Arduino Uno Status", "L293D Motor Controller Status", "Ultrasonic Sensor Status", "Camera Status"])

        # Get the current date and time
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Initialize variables to hold status messages
        battery_status = ""
        cpu_status = ""
        rplidar_status = ""
        arduino_status = ""
        motor_controller_status = ""
        ultrasonic_sensor_status = ""
        camera_status = ""
        arduino = None

        if os_name == 'Windows':
            # Checking Battery
            try:
                battery_info = psutil.sensors_battery()
                battery_percentage = battery_info[0]
                battery_time_remaining = battery_info[1] # Time remaining in seconds
                battery_status = f"Battery: {battery_percentage}%, Time Remaining: {battery_time_remaining} hours"
                if battery_percentage < 20:
                    print('Low battery; cannot proceed further.')
                    return_value = False
                print(battery_status)
            except Exception as e:
                battery_status = f"Error checking battery: {e}"
                return_value = False
                print(battery_status)

            # Checking CPU usage
            try:
                cpu_usage = psutil.cpu_percent()
                cpu_status = f"CPU Usage: {cpu_usage}%"
                print(cpu_status)
            except Exception as e:
                cpu_status = f"Error checking CPU usage: {e}"
                return_value = False
                print(cpu_status)

            # Checking RPLIDAR
            try:
                lidar = RPLidar(rplidar_port) # Adjust the device path as necessary
                info = lidar.get_info()
                health = lidar.get_health()
                if info and health:
                    rplidar_status = "RPLIDAR connected and healthy"
                else:
                    rplidar_status = "RPLIDAR is not functioning as expected"
                    return_value = False
                lidar.stop()
                lidar.disconnect()
                print(rplidar_status)
            except Exception as e:
                rplidar_status = f"Error checking RPLIDAR: {e}"
                return_value = False
                print(rplidar_status)

            # Checking: Arduino Uno, L293D Motor Controller, Ultrasonic Sensor
            try:
                arduino = serial.Serial(arduino_port, baudrate, timeout)
                print("Arduino connected")

                # Send commands to test L293D Motor Controller and Ultrasonic Sensor
                arduino.write(b'TEST_MOTOR_CONTROLLER\n') # Send command with newline
                response = arduino.readline().decode('utf-8').strip()
                if response == "Motor Controller Test Complete":
                    motor_controller_status = "L293D Motor Controller is working"
                else:
                    motor_controller_status = "L293D Motor Controller test failed"
                    return_value = False
                arduino.write(b'TEST_ULTRASONIC_SENSOR\n') # Send command with newline
                response = arduino.readline().decode('utf-8').strip()
                if "Ultrasonic Sensor Distance:" in response:
                    ultrasonic_sensor_status = "HC-SR04 Ultrasonic Sensor is working"
                else:
                    ultrasonic_sensor_status = "HC-SR04 Ultrasonic Sensor test failed"
                    return_value = False
                arduino.close()
                arduino_status = "Arduino connected"
                print(arduino_status)
                print(motor_controller_status)
                print(ultrasonic_sensor_status)
            except Exception as e:
                arduino_status = f"Error!!! Arduino not connected on {arduino_port}: {e}"
                return_value = False
                print(arduino_status)
                print(motor_controller_status)
                print(ultrasonic_sensor_status)

        elif os_name == 'Linux':
            # Checking Battery for Linux
            try:
                battery_info = psutil.sensors_battery()
                battery_percentage = battery_info.percent
                battery_time_remaining = battery_info.secsleft if battery_info.secsleft is not None else "Unknown"
                battery_status = f"Battery: {battery_percentage}%, Time Remaining: {battery_time_remaining} seconds"
                if battery_percentage < 20:
                    print('Low battery; cannot continue further')
                    return_value = False
                print(battery_status)
            except Exception as e:
                battery_status = f"Error checking battery: {e}"
                return_value = False
                print(battery_status)

            # Checking CPU usage for Linux
            try:
                cpu_usage = psutil.cpu_percent()
                cpu_status = f"CPU Usage: {cpu_usage}%"
                print(cpu_status)
            except Exception as e:
                cpu_status = f"Error checking CPU usage: {e}"
                return_value = False
                print(cpu_status)

            # Checking RPLIDAR
            try:
                lidar = RPLidar(rplidar_port) # Adjust the device path as necessary
                info = lidar.get_info()
                health = lidar.get_health()
                if info and health:
                    rplidar_status = "RPLIDAR connected and healthy"
                else:
                    rplidar_status = "RPLIDAR is not functioning as expected"
                    return_value = False
                lidar.stop()
                lidar.disconnect()
                print(rplidar_status)
            except Exception as e:
                rplidar_status = f"Error checking RPLIDAR: {e}"
                return_value = False
                print(rplidar_status)

            # Checking: Arduino Uno, L293D Motor Controller, Ultrasonic Sensor
            try:
                arduino = serial.Serial(arduino_port, baudrate, timeout)
                print("Arduino connected")

                # Send commands to test L293D Motor Controller and Ultrasonic Sensor
                arduino.write(b'TEST_MOTOR_CONTROLLER\n') # Send command with newline
                response = arduino.readline().decode('utf-8').strip()
                if response == "Motor Controller Test Complete":
                    motor_controller_status = "L293D Motor Controller is working"
                else:
                    motor_controller_status = "L293D Motor Controller test failed"
                    return_value = False
                arduino.write(b'TEST_ULTRASONIC_SENSOR\n') # Send command with newline
                response = arduino.readline().decode('utf-8').strip()
                if "Ultrasonic Sensor Distance:" in response:
                    ultrasonic_sensor_status = "HC-SR04 Ultrasonic Sensor is working"
                else:
                    ultrasonic_sensor_status = "HC-SR04 Ultrasonic Sensor test failed"
                    return_value = False
                arduino.close()
                arduino_status = "Arduino connected"
                print(arduino_status)
                print(motor_controller_status)
                print(ultrasonic_sensor_status)
            except Exception as e:
                arduino_status = f"Error!!! Arduino not connected on {arduino_port}: {e}"
                return_value = False
                print(arduino_status)
                print(motor_controller_status)
                print(ultrasonic_sensor_status)

        else:
            print('OS other than Windows and Linux are not currently supported.')
            return_value = False
        # Check USB Webcam
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                camera_status = "USB Webcam connected"
            else:
                camera_status = "USB Webcam not connected"
                return_value = False
            print(camera_status)
        except Exception as e:
            camera_status = f"Error checking USB Webcam: {e}"
            return_value = False
            print(camera_status)

        # Append the statuses to the log file
        with open(log_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([len(open(log_file_path).readlines()), current_date, current_time, battery_status, cpu_status, 
                            rplidar_status, arduino_status, motor_controller_status, ultrasonic_sensor_status, camera_status])
            
        return (arduino, return_value)