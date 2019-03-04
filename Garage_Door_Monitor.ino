// Adafruit IO IFTTT Door Detector
// 
// Learn Guide: https://learn.adafruit.com/using-ifttt-with-adafruit-io
//
// Adafruit invests time and resources providing this open source code.
// Please support Adafruit and open source hardware by purchasing
// products from Adafruit!
//
// Written by Todd Treece for Adafruit Industries
// Copyright (c) 2018 Adafruit Industries
// Licensed under the MIT license.
//
// All text above must be included in any redistribution.

/************************** Configuration ***********************************/

// edit the config.h tab and enter your Adafruit IO credentials
// and any additional configuration needed for WiFi, cellular,
// or ethernet clients.
#include "config.h"

/************************ Example Starts Here *******************************/

// door gpio pin
#define DOOR 13
// Variables to test change in state
int curr_door;
int prev_door;
      

AdafruitIO_Feed *door = io.feed("GarageDoor");

void setup() {

  // start the serial connection
  Serial.begin(115200);

  while (!Serial);
  Serial.println("Adafruit IO Garage Door Detector");

  /// connect to io.adafruit.com
  io.connect();

  
  // wait for a connection
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

   // we are connected
  Serial.println();
  Serial.println(io.statusText());
  
  pinMode(DOOR, INPUT_PULLUP);  // internal pullup will be HIGH when magnetic switch is OPEN, LOW when CLOSED

   // if prev_door = curr_door do nothing; only send changed state

}  

void loop() {
// io.run(); is required for all sketches.
  // it should always be present at the top of your loop
  // function. it keeps the client connected to
  // io.adafruit.com, and processes any incoming data.
  io.run();
  
 // Magnetic contact switch is closed when garage door is open - registers as LOW

   curr_door = digitalRead(DOOR);
  
    if(curr_door != prev_door)
   {
    prev_door = curr_door;    
  
    
   if(curr_door == LOW) {
    Serial.println("Door IS open");
    // the switch is CLOSED/LOW when the garage door is OPEN
    door->save("OPEN");  
    }
    else {
    // the switch is OPEN/HIGH when the garage door is SHUT
    Serial.println("Door is closed!");
    door->save("SHUT"); 
    }
   }

  // Adafruit IO is rate limited for publishing, so a delay is required in
  // between feed->save events. In this example, we will wait three seconds
  // (1000 milliseconds == 1 second) during each loop.
  delay(3000);

   
}   


