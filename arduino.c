//code for the laser microcontroller

int inputPin = 2;
int outputPin = 0 ;
void setup() {
  pinMode(outputPin, OUTPUT);
}
void loop() {
  digitalWrite(outputPin, digitalRead(inputPin));
  delay(1);
}
