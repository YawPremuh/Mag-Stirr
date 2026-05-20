import serial
import time

coms = {'windows': ['COM3', 'COM4', 'COM5'], 
        'mac': ['/dev/cu.usbmodem11201', '/dev/cu.usbserial-1130', '/dev/cu.usbserial-1140']}


def get_arduino_port(coms, os_type):
    arduino1 = serial.Serial(port=coms[os_type][0], baudrate=9600, timeout=1)
    arduino2 = serial.Serial(port=coms[os_type][1], baudrate=9600, timeout=1) #board2
    arduino3 = serial.Serial(port=coms[os_type][2], baudrate=9600, timeout=1) #board3
    return arduino1, arduino2, arduino3

# Mac/Linux: port='/dev/ttyUSB0'
time.sleep(2)  # let Arduino reset

arduino1 , arduino2, arduino3 = get_arduino_port(coms, 'windows')  # change 'windows' to 'mac' if using Mac/Linux
boards = {
    1 : arduino1,
    2 : arduino2,
    3 : arduino3
}

def set_zone(board, zone, speed):
    """zone: 1-4, speed: 0-100%"""
    speed = max(0, min(40, speed)) 
    command = f"Z{zone}:{(speed/100) * 255}\n"
    boards[board].write(command.encode())

#function to stop all zones
def stop_all():
    for b in boards:
        for m in range(1, 4):
            boards[b].write(b"STOP\n")

#function to run all zones
#def run_all():

#function to control zones individually
def run_ind():
    #board1
    set_zone(1, 1, 39)   # zone 1 
    set_zone(1, 2, 58)   # zone 2 
    set_zone(1, 3, 39)   # zone 3 
    set_zone(1, 4, 58)   # zone 4

    #board2
    set_zone(2, 1, 60)   # zone 1 
    set_zone(2, 2, 60)   # zone 2 
    set_zone(2, 3, 60)   # zone 3 
    set_zone(2, 4, 60)   # zone 4

    #board3
    set_zone(3, 1, 60)   # zone 1 
    set_zone(3, 2, 60)   # zone 2 
    set_zone(3, 3, 60)   # zone 3 
    set_zone(3, 4, 60)   # zone 4

run_ind()
time.sleep(3)
#stop_all()

