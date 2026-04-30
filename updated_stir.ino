const int motors[] = {6, 9, 10, 11};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(motors[i], OUTPUT);
    analogWrite(motors[i], 0);
  }
}

void loop() {
  if (Serial.available()) {

    int motorIndex = Serial.parseInt();  // 0–3
    int speed = Serial.parseInt();       // 0–255

    speed = constrain(speed, 0, 255);

    if (motorIndex >= 0 && motorIndex <= 4) {
      analogWrite(motors[motorIndex], speed);
    }
  }
}
