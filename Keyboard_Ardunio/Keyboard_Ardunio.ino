#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_NeoPixel.h>

const int numButtons = 6; // Number of buttons

struct buttons{
  int pin;
  int Red;
  int Blue;
  int Green;
  String Output;
};

const buttons keyboardBtns[6] = {
  {0, 255, 0, 0, "Youtube"}, // Red - p0
  {1, 173, 216, 230, "Prime"}, // Light Blue - p1
  {2, 0, 255, 0, "Gmail"}, // Green - p2
  {3, 72, 61, 139, "Zoro"}, // Dark Blue - p3
  {4, 255, 165, 0, "Buffstreams"}, // Orange - p4
  {5, 0, 0, 255, "Discord"}, //Blue - p5
};

const uint8_t I2C_Address = 0x20;

Adafruit_NeoPixel strip (6, 1, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);

  strip.begin();
  strip.show();

  for (int i =0; i < numButtons; i++){
    strip.setPixelColor(i, keyboardBtns[i].Red, keyboardBtns[i].Blue, keyboardBtns[i].Green);
    strip.show();
    delay(200);
    strip.clear();
  }
  strip.clear();

  Wire.begin();

  // Wire.beginTransmission(I2C_Address);
  // Wire.write(0xFF); 
  // Wire.endTransmission();
}

void loop() {

  Wire.requestFrom(I2C_Address, 1);

  if (Wire.available())
  {
    byte buttonStates = Wire.read();

    for (int i = 0; i < 6; i++) {
      bool notPressed = bitRead(buttonStates, i);
      if (!notPressed) {
        Serial.println(keyboardBtns[i].Output);
        strip.setPixelColor(i, keyboardBtns[i].Red, keyboardBtns[i].Blue, keyboardBtns[i].Green);
        strip.show();
        delay(200);
        strip.clear();
        strip.show();
      }
    }
  }
  
  delay(100);
}