class SerialWrite:
    @staticmethod
    def serial_write(arduino, a, b):
        arduino.write(bytes(f"{a}, {b}", 'utf-8'))
        while True:
            check = arduino.readline().strip().decode('utf-8')
            if check:
                print(check)
                break
        while True:
            check2 = arduino.readline().strip().decode('utf-8')
            if check2:
                print(check2)
                break
        print()