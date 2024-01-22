const int TRIGPIN = 3;          
const int ECHOPIN = 2;
long timer;
int jarak;
int height_ = 634;
void setup()
{
  Serial.begin(115200);
  pinMode(ECHOPIN, INPUT);
  pinMode(TRIGPIN, OUTPUT);
}

void loop()
{
  digitalWrite(TRIGPIN, LOW);                   
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);                  
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);                   

  timer = pulseIn(ECHOPIN, HIGH);
  jarak = timer/58;
  delay(10);

//  Serial.print("Jarak = ");
  Serial.println((jarak*10)+124);
//  Serial.print(" cm");
}
