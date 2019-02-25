import os
import requests
CurrentLocationAndWeather = 'CurrentLocationAndWeather.txt'


def main():
    # Using the GEOIP-DB website url, get the location information for the current IP address and save to the the
    # variable 'url' # in JSON format. Parse the variable and create 4 more variables to be used to get weather
    # data in the next section.
    IpLocation = (requests.get('https://geoip-db.com/json')).json()
    latitude = IpLocation["latitude"]
    longitude = IpLocation["longitude"]
    country = IpLocation["country_name"]
    city = IpLocation["city"]

    weatherUrl_part1 = "https://api.openweathermap.org/data/2.5/weather?lat="
    weatherUrl_part2 = "&units=metric&appid=42576a539c72dd7b5efaca6e382402c9"
    weatherUrl = weatherUrl_part1 + str(latitude) + "&lon=" + str(longitude) + weatherUrl_part2


    # Open the url and save the results to a json variable 'url1'
    # Prepare a variable containing a string with  the location and temperature information
    # Write that variable to an output text file 'CurrentLocationAndWeather.txt'

    TemperatureInfo = (requests.get(weatherUrl)).json()

    temp = (TemperatureInfo["main"])["temp"]
    ResultString_pt1 = "Your current location is: "
    ResultString_pt2 = " and the current temperature is: "
    ResultString_pt3 = " degrees celsius"
    ResultString = ResultString_pt1 + city + "," + country + ResultString_pt2 + str(temp) + ResultString_pt3
    f = open(CurrentLocationAndWeather, 'w')
    f.write("%s\r\n" % ResultString)

    # Create a list of 10 cities
    ListOfCities = 'London,GB', 'Paris,FR', 'Sydney,AU', 'Tokyo,JP', 'New York,US', 'Atlanta,US', 'Moscow,RU'
    ListOfCities += 'Rio de Janeiro,BR', 'Nairobi,KE', 'Mexico City,MX'

    # Prepare a url variable 'CityWeatherUrl' containing a url that will return weather information for each
    # city in the list using a loop in the next section

    for citycombo in ListOfCities:
        CityWeatherUrl_part1 = "https://api.openweathermap.org/data/2.5/weather?q="
        CityWeatherUrl_part2 = "&units=metric&appid=42576a539c72dd7b5efaca6e382402c9"
        CityWeatherUrl = CityWeatherUrl_part1 + str(citycombo) + CityWeatherUrl_part2

        # Open the CityWeatherUrl and save the results to the json variable 'url2'
        # Referencing the json variable sections, create  2 more variables to be used to get the
        # Full Country Name in the next section

        CityWeatherData = (requests.get(CityWeatherUrl)).json()
        cityname = CityWeatherData["name"]
        countrycode = (CityWeatherData["sys"])["country"]

        # Prepare a url variable 'CountryURL' to be used to get the Full Country Name

        CountryURL = "https://restcountries.eu/rest/v2/alpha/" + str(countrycode)

        # Open the CountryURL url and retrieve the CountryName

        CountryNameData = (requests.get(CountryURL)).json()
        CountryName = CountryNameData["name"]

        # Build an Output String that will include the city and country names and the local temperature
        # and append it to the above text file 'CurrentLocationAndWeather.txt'

        temp = (CityWeatherData["main"])["temp"]
        tmpString_pt1 = "The weather in "
        tmpString_pt2 = " degrees celsius."
        OutputString = tmpString_pt1 + cityname + ", " + CountryName + " is " + str(temp) + tmpString_pt2
        print(OutputString)
    os._exit(0)


if __name__ == "__main__":
    main()
