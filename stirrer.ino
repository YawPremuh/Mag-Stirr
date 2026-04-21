// Motor pins
const int motor1 = 9;
const int motor2 = 10;
const int motor3 = 11;
const int motor4 = 6;   // NEW motor

void setup()
{
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);  // NEW
}

void loop()
{
  runZone1(255); // speed: 0–255
  runZone2(255);
  runZone3(255);
  runZone4(255); // NEW
}

// Functions
void runZone1(int speed)
{
  analogWrite(motor1, speed);
}

void runZone2(int speed)
{
  analogWrite(motor2, speed);
}

void runZone3(int speed)
{
  analogWrite(motor3, speed);
}

void runZone4(int speed)   // NEW
{
  analogWrite(motor4, speed);
}
