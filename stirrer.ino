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
  runZone1(255); // zone1
  runZone2(255); //zone2
  runZone3(255); //zone3
  runZone4(255); // zone4
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
