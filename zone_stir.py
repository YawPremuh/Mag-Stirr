import serial
import time

# Change COM port accordingly (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux/Mac)
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # wait for connection

def set_speed(speed):
    speed = max(0, min(255, speed))
    arduino.write(f"{speed}\n".encode())

# Example usage
while True:
    set_speed(255)  # full speed
    time.sleep(5)

    set_speed(100)  # slower
    time.sleep(5)

    set_speed(0)    # stop
    time.sleep(5)
