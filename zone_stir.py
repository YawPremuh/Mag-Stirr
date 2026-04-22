import serial
import time

arduino = serial.Serial(port='/dev/cu.usbmodem1201', baudrate=9600, timeout=1)
# Mac/Linux: port='/dev/ttyUSB0'
time.sleep(2)  # let Arduino reset

def set_zone(zone, speed):
    """zone: 1-4, speed: 0-255"""
    speed = max(0, min(255, speed))  # clamp to valid range
    command = f"Z{zone}:{speed}\n"
    arduino.write(command.encode())

def stop_all():
    arduino.write(b"STOP\n")

# --- Example usage ---
set_zone(1, 255)   # zone 1 full speed
set_zone(2, 128)   # zone 2 half speed
set_zone(3, 200)   # zone 3 ~78% speed
set_zone(4, 255)   # zone 4 full speed
#time.sleep(3)
#stop_all()
