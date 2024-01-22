#include "Adafruit_VL53L0X.h"
#define WINDOW_SIZE 10 
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
int INDEX = 0;
int VALUE = 0;
int SUM = 0;
int READINGS[WINDOW_SIZE];
int AVERAGED = 0;
int height_ = 654;

void setup() {
  Serial.begin(115200);
  while (! Serial) {
    delay(1);
  }
//  Serial.println("Adafruit VL53L0X test");
  if (!lox.begin()) {
    Serial.println(0);
    while(1);
  }
  Serial.println(1); 
}


void loop() {
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false); 

  if (measure.RangeStatus != 4) { 
//    Serial.print("Distance (mm): "); 
//    Serial.println(measure.RangeMilliMeter - 20);
    SUM = SUM - READINGS[INDEX];       // Remove the oldest entry from the sum
    VALUE = measure.RangeMilliMeter - 20;        // Read the next sensor value
    READINGS[INDEX] = VALUE;           // Add the newest reading to the window
    SUM = SUM + VALUE;                 // Add the newest reading to the sum
    INDEX = (INDEX+1) % WINDOW_SIZE;   // Increment the index, and wrap to 0 if it exceeds the window size
  
    AVERAGED = SUM / WINDOW_SIZE; 
//    Serial.print("Distance (mm): "); 
    Serial.println(height_-AVERAGED);
  } else {
    Serial.println(" out of range ");
  }
  

  delay(100);
}
