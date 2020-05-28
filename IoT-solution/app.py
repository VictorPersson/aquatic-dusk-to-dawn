
import board
import neopixel
import requests
import time
from datetime import datetime, timedelta
import APIKeys

location = "Malmö"
weatherURL = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={APIKeys.APIKey}"

pixels = neopixel.NeoPixel(board.D18, 30)

# Execute API call every 10 minutes
startTime = time.time()
minutes = 0


while True:
    print("Fetching API...", minutes)
    minutes += 1
    
    res = requests.get(url = weatherURL)
    data = res.json() 

    sky = data["weather"][0]["main"]
    sunrise = int(data["sys"]["sunrise"])
    sunset = int(data["sys"]["sunset"])
    
    startSunRise = (datetime.fromtimestamp(sunrise) + timedelta(hours=-1)).strftime('%H:%M:%S')
    endSunRise = (datetime.fromtimestamp(sunrise) + timedelta(hours=6)).strftime('%H:%M:%S')

    startSunSet = (datetime.fromtimestamp(sunset) + timedelta(hours=-2)).strftime('%H:%M:%S')
    endSunSet = (datetime.fromtimestamp(sunset) + timedelta(hours=1)).strftime('%H:%M:%S')

    currentTime = datetime.now().strftime('%H:%M:%S')


    if sky == "Clear sky":
        # Full birghtness
        sunRisesSunSet = (255, 99, 71)
        sunDay = (255, 215, 0)
        night = (0, 0, 0)
        step = 1
    elif sky == "Clouds" or sky == "Few clouds" or sky == "Scattered clounds" or sky == "Broken clouds":
        # Somewhat less birght / every other LED
        sunRisesSunSet = (255, 42, 0)
        sunDay = (192, 192, 192)
        night = (0, 0, 0)
        step = 2
    elif sky == "Rain" or sky == "Shower rain":
        # Less birght / every 3'rd LED
        sunRisesSunSet = (255, 42, 0)
        sunDay = (128, 128, 128)
        night = (0, 0, 0)
        step = 3
    elif sky == "Snow" or sky == "Mist":
        # Less brightness / white
        sunRisesSunSet = (255, 42, 0)
        sunDay = (0, 255, 255)
        night = (0, 0, 0)
        step = 2
    elif sky == "Thunderstorm":
        # Flash LED with less birght
        sunRisesSunSet = (255, 42, 0)
        sunDay = (255, 255, 255)
        night = (0, 0, 0)
        step = 2

    # Reset LEDS before API new update
    for led in range(0,29):
        pixels[led] = night

    if currentTime > startSunRise and currentTime < endSunRise:
        print("Sun rises, Orange")
        for led in range(0,10,step):
            pixels[led] = sunRisesSunSet
    elif currentTime > startSunSet and currentTime < endSunSet:
        print("Sun sets, Orange")
        for led in range(20,30,step):
            pixels[led] = sunRisesSunSet
    elif currentTime > endSunRise and currentTime < startSunSet:
        print("Middle of the day, normal light")
        for led in range(10,20,step):
            pixels[led] = sunDay
    elif currentTime > endSunSet or currentTime < startSunRise:
        print("Night, turning off the light")
        for led in range(0,29,step):
            pixels[led] = night

    print("Sky: ", sky)
    print("Current time" , currentTime)
    print("Sunrise start:" , startSunRise, "Sunrise end:" , endSunRise)
    print("Sunset start:" , startSunSet, "Sunset end:" , endSunSet)

    print("________________________________________")
 
    time.sleep(600.0 - ((time.time() - startTime) % 600.0))
