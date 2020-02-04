#include <FastLED.h>
#define LED_PIN 7
#define NUM_LEDS 2


CRGB leds[NUM_LEDS];


void setup() {
  FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, NUM_LEDS);
}


void loop() {
    for (int i = 0; i < NUM_LEDS; i++) {
      
      leds[i] = CRGB(90, 20, 100);
      FastLED.show();
      
      delay(300);
      leds[i] = CRGB(20, 150, 2);

      delay(300);
      leds[i] = CRGB(25, 0, 93);
      
  }
}
