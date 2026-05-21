"""
stirrer.py — magnetic stirrer controller for the Tecan rack stirrer boards.

Three Arduino boards, each driving 4 zones (motors).  Boards 1-3 cover racks
1-2, 3-4, 5-6 respectively. Each zone covers 8 tubes spanning two adjacent
racks (4 tubes from each rack, contiguous rows).

Wire format: 'Zn:val\\n' (n = zone 1-4 on that board, val = 0-255 PWM).
"""

import serial
import time


class StirrerController:
    PORTS = {
        "windows": ["COM3", "COM4", "COM5"],
        "mac":     ["/dev/cu.usbmodem11201",
                    "/dev/cu.usbserial-1130",
                    "/dev/cu.usbserial-1140"],
    }
    BAUDRATE         = 9600
    SERIAL_TIMEOUT_S = 1.0
    ARDUINO_RESET_S  = 2.0   # delay after opening port for board to reboot
    SPEED_FLOOR_PCT  = 40    # below this the motors hum without spinning
    SPEED_CEIL_PCT   = 100

    def __init__(self, os_type: str = "windows"):
        self._os_type = os_type
        self._boards: dict = {}     # board_num -> serial.Serial
        self._connected = False

    def connect(self):
        """Open all three serial ports. Safe to call multiple times."""
        if self._connected:
            return
        ports = self.PORTS[self._os_type]
        for i, p in enumerate(ports, start=1):
            self._boards[i] = serial.Serial(
                port=p, baudrate=self.BAUDRATE, timeout=self.SERIAL_TIMEOUT_S,
            )
        time.sleep(self.ARDUINO_RESET_S)
        self._connected = True
        print(f"  [stirrer] Connected: {ports}")

    def disconnect(self):
        for n, s in list(self._boards.items()):
            try:
                s.close()
            except Exception:
                pass
        self._boards.clear()
        self._connected = False
        print("  [stirrer] Disconnected.")

    def set_zone(self, board: int, zone: int, speed: float):
        """Set one zone. speed in percent; 0 stops, values 1..floor are
        raised to SPEED_FLOOR_PCT, anything above ceil is clamped."""
        if not self._connected:
            raise RuntimeError("Stirrer not connected. Call connect() first.")
        if board not in self._boards:
            raise ValueError(f"Unknown board {board}; have {list(self._boards)}")
        if zone not in (1, 2, 3, 4):
            raise ValueError(f"Zone must be 1-4, got {zone}")

        # 0 is a literal stop. Anything between 1 and the floor would
        # stall the motor — raise it to the floor so the caller gets a
        # spinning bar instead of a buzzing one.
        if speed <= 0:
            speed_pct = 0.0
        else:
            speed_pct = max(self.SPEED_FLOOR_PCT, min(self.SPEED_CEIL_PCT, speed))

        pwm = int(round((speed_pct / 100.0) * 255))
        cmd = f"Z{zone}:{pwm}\n".encode()
        self._boards[board].write(cmd)
        print(f"  [stirrer] board={board} zone={zone} -> {speed_pct:.0f}% ({pwm}/255)")

    def set_zones(self, zone_map: dict):
        """Batch set: {(board, zone): speed_pct, ...}. See per-call docs above."""
        for (board, zone), speed in zone_map.items():
            self.set_zone(board, zone, speed)

    def start_all(self, speed: float):
        """Spin every zone on every board at the same speed."""
        plan = {(b, z): speed for b in self._boards for z in (1, 2, 3, 4)}
        self.set_zones(plan)

    def stop_all(self):
        """Stop every zone. Sends speed=0 (which the firmware should
        interpret as analogWrite(pin, 0))."""
        plan = {(b, z): 0 for b in self._boards for z in (1, 2, 3, 4)}
        self.set_zones(plan)

    # ── Tube → (board, zone) mapping (Option A: motors straddle two racks) ──

    @staticmethod
    def tube_to_zone(tube_num: int) -> tuple:
        """Return (board, zone) for a flat tube number 1-96.

        Mapping (8 tubes per zone, straddling two adjacent racks):
            board 1 covers tubes  1-32   (racks 1-2)
            board 2 covers tubes 33-64   (racks 3-4)
            board 3 covers tubes 65-96   (racks 5-6)
        Within each board, zone covers rows 1-4, 5-8, 9-12, 13-16 of each rack.
        """
        assert 1 <= tube_num <= 96, f"tube_num must be 1-96, got {tube_num}"
        board = (tube_num - 1) // 32 + 1
        row   = (tube_num - 1) % 16
        zone  = row // 4 + 1
        return board, zone