const int motor1 = 9;
const int motor2 = 10;
const int motor3 = 11;
const int motor4 = 6;

void setup() {
  Serial.begin(9600);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);
}

void runZone1(int speed) { analogWrite(motor1, speed); }
void runZone2(int speed) { analogWrite(motor2, speed); }
void runZone3(int speed) { analogWrite(motor3, speed); }
void runZone4(int speed) { analogWrite(motor4, speed); }

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if      (cmd.startsWith("Z1:")) { runZone1(cmd.substring(3).toInt()); }
    else if (cmd.startsWith("Z2:")) { runZone2(cmd.substring(3).toInt()); }
    else if (cmd.startsWith("Z3:")) { runZone3(cmd.substring(3).toInt()); }
    else if (cmd.startsWith("Z4:")) { runZone4(cmd.substring(3).toInt()); }
    else if (cmd == "STOP") {
      runZone1(0); runZone2(0); runZone3(0); runZone4(0);
    }
  }
}
