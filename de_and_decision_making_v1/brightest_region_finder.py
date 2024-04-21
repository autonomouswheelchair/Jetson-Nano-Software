from brightness_calculator import BrightnessCalculator

class BrightestRegionFinder:
    @staticmethod
    def find_brightest_region(frame):
        # Divide the frame into three regions (left, middle, right)
        height, width = frame.shape[:2]
        third_width = width // 3
        
        # print(f'frame: {frame}, height: {height}, width: {width}, third_width: {third_width}')

        # Calculate brightness of each region
        left_brightness = BrightnessCalculator.calculate_brightness(frame[:, :third_width])
        middle_brightness = BrightnessCalculator.calculate_brightness(frame[:, third_width:2*third_width])
        right_brightness = BrightnessCalculator.calculate_brightness(frame[:, 2*third_width:])

        # Find the region with the least brightness
        min_brightness = min(left_brightness, middle_brightness, right_brightness)

        # print(f'left_brightness: {left_brightness}, middle_brightness: {middle_brightness}, right_brightness: {right_brightness}, min_brightness: {min_brightness}')

        # Determine direction based on the brightest region
        if min_brightness == left_brightness:
            direction = "LEFT"
        elif min_brightness == right_brightness:
            direction = "RIGHT"
        else:
            direction = "STRAIGHT"

        return direction
