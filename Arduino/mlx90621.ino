#include <SPI.h>
#include <Time.h>
#include <Arduino.h>
#include <Wire.h>
#include "wireMLX90621.h" 

MLX90621 sensor; // create an instance of the Sensor class

void setup(){
  Serial.begin(57600);
  sensor.initialise (16);
  Serial.setTimeout(50);
 }
void loop(){
  sensor.measure(true); //get new readings from the sensor
  Serial.println(0);
  
  for(int y=0;y<4;y++){ //go through all the rows  
    for(int x=0;x<16;x++){ //go through all the columns
      int16_t valueAtXY= sensor.irData[y+x*4]; // extract the temperature at position x/y
       //Serial.println(sensor.getTemperature(y+x*4));
       Serial.print(sensor.getTemperature(y+x*4));
       Serial.print("  ");
    }
    //Serial.println(" ");
    
  }
 
  //Serial.print ("ambient ");
 // Serial.println(sensor.getTemperature(0));
    Serial.println("\n");

  //Serial.print(sensor.getTemperature(9));
   //Serial.print ("ptat ");
   //Serial.println(sensor.ptat);
   //Serial.print ("cpix ");
   //Serial.println(sensor.cpix);
  //  tft.setCursor(10, 20);
  // Serial.print ("a.common");
  // Serial.println(sensor.a_common);
//delay(0.1);
};
