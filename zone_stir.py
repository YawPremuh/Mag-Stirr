import serial
import time

arduino = serial.Serial(port='/dev/cu.usbmodem11201', baudrate=9600, timeout=1)
# Mac/Linux: port='/dev/ttyUSB0'
time.sleep(2)  # let Arduino reset

def set_zone(zone, speed):
    """zone: 1-4, speed: 0-100%"""
    speed = max(0, min(100, speed)) 
    command = f"Z{zone}:{(speed/100) * 255}\n"
    arduino.write(command.encode())

def stop_all():
    arduino.write(b"STOP\n")

# --- Example usage ---
set_zone(1, 78)   # zone 1 
set_zone(2, 60)   # zone 2 
set_zone(3, 70)   # zone 3 
set_zone(4, 60)   # zone 4
time.sleep(3)
#stop_all()

