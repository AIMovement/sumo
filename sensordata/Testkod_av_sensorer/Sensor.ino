
volatile int FLsensor;
volatile int FMsensor;
volatile int FRsensor;
volatile int Lsensor;
volatile int Rsensor;

volatile int FRdig;
volatile int FLdig;
volatile int Bdig;

void readSensors(void){  
//  FLsensor = analogRead(AN_FR_LEFT_SENSOR);
//  FMsensor = analogRead(AN_FR_MID_SENSOR);
//  FRsensor = analogRead(AN_FR_RIGHT_SENSOR);
//  Lsensor = analogRead(AN_LEFT_SENSOR);
  Rsensor = analogRead(AN_RIGHT_SENSOR);
  
//  FRdig = digitalRead(DIG_FR_RIGHT_GROUND_SENSOR);
//  FLdig = digitalRead(DIG_FR_LEFT_GROUND_SENSOR);
//  Bdig = digitalRead(DIG_FR_BACK_GROUND_SENSOR);
  
//  Serial.print("FL = ");
//  Serial.println(FLsensor);
//  
//  Serial.print("FM = ");
//  Serial.println(FMsensor);
//  
//  Serial.print("FR = ");
//  Serial.println(FRsensor);
//      
//  Serial.print("L = ");
//  Serial.println(Lsensor);
  
//  Serial.print("R = ");
  Serial.println(Rsensor);
  
  
//  Serial.println(FRdig);
//  Serial.println(FLdig);
//  Serial.println(Bdig);
 

}
