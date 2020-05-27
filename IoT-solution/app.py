import requests, time
from datetime import datetime, timedelta
import APIKeys

location = "Malmö"
weatherURL = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={APIKeys.APIKey}"

# Execute API call every 10 minutes
startTime = time.time()
minutes = 0


while True:
    print("Fetching API...", minutes)
    minutes += 1
    
    res = requests.get(url = weatherURL)
    data = res.json() 

    sky = data["weather"][0]["main"] # "clear sky" , "few clouds", "scattered clounds", "broken clouds", "shower rain" , "rain" , "thundersctorm", "snow", "mist"
    sunrise = int(data["sys"]["sunrise"])
    sunset = int(data["sys"]["sunset"])
    
    startSunRise = (datetime.fromtimestamp(sunrise) + timedelta(hours=-1)).strftime('%H:%M:%S')
    endSunRise = (datetime.fromtimestamp(sunrise) + timedelta(hours=6)).strftime('%H:%M:%S')

    startSunSet = (datetime.fromtimestamp(sunset) + timedelta(hours=-2)).strftime('%H:%M:%S')
    endSunSet = (datetime.fromtimestamp(sunset) + timedelta(hours=1)).strftime('%H:%M:%S')

    currentTime = datetime.now().strftime('%H:%M:%S')

    if currentTime > startSunRise and currentTime < endSunRise:
        print("SUN IN TIME OF RISES, Orange")
    elif currentTime > startSunSet and currentTime < endSunSet:
        print("SUN IN TIME OF GOING OT BED, Orange")
    elif currentTime > endSunRise and currentTime < startSunSet:
        print("Middle of the day, normal light")
    elif currentTime > endSunSet or currentTime < startSunRise:
        print("IT'S NIGHT")

    print(f"Sky: {sky}")
    print(f"Current time {currentTime}")
    print(f"Sunrise start: {startSunRise}, Sunrise end: {endSunRise}")
    print(f"Sunset start: {startSunSet}, Sunset end: {endSunSet}")

    print("________________________________________")

    if sky == "Clear sky":
        # Full birghtness
        print(f"Sky is: {sky}, full brightness")
    elif sky == "Clouds" or sky == "Few clouds" or sky == "Scattered clounds" or sky == "Broken clouds":
        # Somewhat less birght / every other LED
        print(f"Sky is: {sky}, oooh, cloudy, less LEDS")
    elif sky == "Rain" or sky == "Shower rain":
        # Less birght / every other LED
        print(f"Sky is: {sky}, turn on less LEDS")
    elif sky == "Snow" or sky == "Mist":
        # Less brightness / white
        print(f"Sky is: {sky}, turn on white less LEDS")
    elif sky == "Thunderstorm":
        # Flash LED with less birght
        print(f"Sky is: {sky}, flash LEDS")


    
    time.sleep(600.0 - ((time.time() - startTime) % 600.0))



