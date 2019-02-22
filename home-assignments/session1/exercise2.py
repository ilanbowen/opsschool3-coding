import os
import urllib.request
import json

def main():
# Using the GEOIP-DB website url, get the location information for the current IP address and save to the the variable 'url' # in JSON format. Parse the variable and create 4 more variables to be used to get weather data in the next section.

    with urllib.request.urlopen("https://geoip-db.com/json") as url: 
        data = json.loads(url.read().decode())
        latitude = data["latitude"]
        longitude = data["longitude"]
        country = data["country_name"]
        city = data["city"]

# Create a url variable based partly on latitude and longitude information gained from the previous section that will return 
# results in metric format

        weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&units=metric&appid=42576a539c72dd7b5efaca6e382402c9"

# Open the url and save the results to a json variable 'url1'
# Prepare a variable containing a string with  the location and temperature information
# Write that variable to an output text file 'CurrentLocationAndWeather.txt'

        with urllib.request.urlopen(weatherUrl) as url1:
            data1 = json.loads(url1.read().decode())
            temp = (data1["main"])["temp"]
            ResultString = "Your current location is: " + city + "," + country + " and the current temperature is: " + str(temp) + " degrees celsius"
            f = open('CurrentLocationAndWeather.txt', 'w')
            f.write("%s\r\n" % ResultString)

# Create a list of 10 cities
            ListOfCities = 'London,GB','Paris,FR','Sydney,AU','Tokyo,JP','New York,US','Atlanta,US','Moscow,RU','Rio de Janeiro,BR','Nairobi,KE','Mexico City,MX'

# Prepare a url variable 'CityWeatherUrl' containing a url that will return weather information for each city in the list
# using a loop in the next section

            for citycombo in ListOfCities:
                CityWeatherUrl = "https://api.openweathermap.org/data/2.5/weather?q=" + str(citycombo) + "&units=metric&appid=42576a539c72dd7b5efaca6e382402c9"

# Open the CityWeatherUrl and save the results to the json variable 'url2'
# Referencing the json variable sections, create  2 more variables to be used to get the Full Country Name in the next section

                with urllib.request.urlopen(CityWeatherUrl) as url2:
                    data2 = json.loads(url2.read().decode())
                    cityname = data2["name"]
                    countrycode = (data2["sys"])["country"]

# Prepare a url variable 'CountryURL' to be used to get the Full Country Name					

                    CountryURL = "https://restcountries.eu/rest/v2/alpha/" + str(countrycode)

# Open the CountryURL url and retrieve the CountryName					
					
                    CountryNameData = urllib.request.urlopen(CountryURL)
                    ParsedCountryNameData = json.loads(CountryNameData.read().decode())
                    CountryName = ParsedCountryNameData["name"]
					
# Build an Output String that will include the city and country names and the local temperature and append it to the above
# text file 'CurrentLocationAndWeather.txt'

                    temp = (data2["main"])["temp"]
                    OutputString = "The weather in " + cityname + ", " + CountryName + " is " + str(temp) + " degrees celsius."
                    print(OutputString)
                    f = open('CurrentLocationAndWeather.txt', 'a')
                    f.write("%s\r\n" % OutputString)
            os._exit(0)

if __name__ == "__main__":
    main()
