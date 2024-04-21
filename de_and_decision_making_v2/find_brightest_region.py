from calculate_brightness import CalculateBrightness
class FindBrightestRegion:
    @staticmethod
    def find_brightest_region(frame):
        height, width = frame.shape[:2]
        third_width = width // 4
        left_brightness = CalculateBrightness.calculate_brightness(frame[:, :third_width])
        middle_brightness = CalculateBrightness.calculate_brightness(frame[:, third_width:width-third_width])
        right_brightness = CalculateBrightness.calculate_brightness(frame[:, width-third_width:])
        min_brightness = min(left_brightness, middle_brightness, right_brightness)
        if min_brightness == left_brightness:
            direction = "LEFT"
        elif min_brightness == right_brightness:
            direction = "RIGHT"
        else:
            direction = "STRAIGHT"
        return direction
