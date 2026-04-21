// Motor pins
const int motor1 = 9;
const int motor2 = 10;
const int motor3 = 11;

void setup()
{
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);

  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0)
  {
    int speed = Serial.parseInt(); // read speed from Python

    speed = constrain(speed, 0, 255);

    runZone1(speed);
    runZone2(speed);
    runZone3(speed);
  }
}

void runZone1(int speed) { analogWrite(motor1, speed); }
void runZone2(int speed) { analogWrite(motor2, speed); }
void runZone3(int speed) { analogWrite(motor3, speed); }