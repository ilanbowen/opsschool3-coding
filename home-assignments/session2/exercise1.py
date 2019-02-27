import requests
import json
from collections import Counter

city="dublin"
units="c"
#units="f"

weatherurl_pt1 = "https://api.openweathermap.org/data/2.5/"
today = "weather?q="
threeday = "forecast?q="

weatherurl_pt1a = weatherurl_pt1 + today
weatherurl_pt1b = weatherurl_pt1 + threeday

weatherurl_celsius = "&units=metric"
weatherurl_fahrenheit = "&units=imperial"
weatherurl_appkey = "&appid=42576a539c72dd7b5efaca6e382402c9"

weatherurlb = weatherurl_pt1b + city + weatherurl_celsius + weatherurl_appkey

if units=="c":
    weatherurl = weatherurl_pt1a + city + weatherurl_celsius + weatherurl_appkey
    unitsname = "celsius"
elif units=="f":
    weatherurl = weatherurl_pt1a + city + weatherurl_fahrenheit + weatherurl_appkey
    unitsname = "fahrenheit"

#print(weatherurl)
weatherresult = (requests.get(weatherurl)).json()

tempdescription = str(((weatherresult["weather"])[0])['description'])
mintemp = str((weatherresult["main"])["temp_min"])
maxtemp = str((weatherresult["main"])["temp_max"])
cityname = str(weatherresult["name"])

str_pt1 = "The weather in "
str_pt2 = " today is "
str_pt3 = " with temperatures trailing from "
outputstring = str_pt1 + cityname + str_pt2 + tempdescription + str_pt3 + mintemp + "-" + maxtemp + " " + unitsname

print(outputstring)
print("")
print("Forecast for the next 3 days:")
print("")

weatherresultb = (requests.get(weatherurlb)).json()
#print(weatherurlb)

weatherresultb = (requests.get(weatherurlb)).json()
weather_result_list = weatherresultb["list"]
weather_result_city = (weatherresultb["city"])['name']
#print(weather_result_city)

#print(weather_result_list_first)

#with open('data2.txt', 'w') as outfile:
#    json.dump(weather_result_list_first, outfile)

index=0
daily_min=0
daily_max=0
descriptionlist1=[]
datetext1=""

for x in range(0, 8):
    weather_result_list_item = weather_result_list[index]
    datetext = (weather_result_list_item["dt_txt"]).split(' ')[0]
    datetext1 = (weather_result_list_item["dt_txt"])
    tempdescription = str(((weather_result_list_item["weather"])[0])['description'])
    descriptionlist1.append(tempdescription)
    if daily_min==0:
        first_daily_min = (weather_result_list_item["main"])["temp_min"]
        daily_min = first_daily_min
    elif daily_min > (weather_result_list_item["main"])["temp_min"]:
        daily_min = (weather_result_list_item["main"])["temp_min"]

    if daily_max==0:
        first_daily_max = (weather_result_list_item["main"])["temp_max"]
        daily_max = first_daily_max
    elif daily_max < (weather_result_list_item["main"])["temp_max"]:
        daily_max = (weather_result_list_item["main"])["temp_max"]

    mintemp = str((weather_result_list_item["main"])["temp_min"])
    maxtemp = str((weather_result_list_item["main"])["temp_max"])
    forecaststring = datetext1 + ' ' + tempdescription + str_pt3 + mintemp + "-" + maxtemp + " " + unitsname
#    print(forecaststring)
    index+=1

daily_min = str(daily_min)
daily_max = str(daily_max)
cnt_ = Counter(descriptionlist1)
most_common_description = ((cnt_.most_common(1))[0])[0]
forecaststring = datetext + ' ' + most_common_description + str_pt3 + daily_min + "-" + daily_max + " " + unitsname
print(forecaststring)


index=8
daily_min=0
daily_max=0
descriptionlist2=[]

for x in range(0, 8):
    weather_result_list_item = weather_result_list[index]
    datetext = (weather_result_list_item["dt_txt"]).split(' ')[0]
    datetext1 = (weather_result_list_item["dt_txt"])
    tempdescription = str(((weather_result_list_item["weather"])[0])['description'])
    descriptionlist2.append(tempdescription)
    if daily_min==0:
        first_daily_min = (weather_result_list_item["main"])["temp_min"]
        daily_min = first_daily_min
    elif daily_min > (weather_result_list_item["main"])["temp_min"]:
        daily_min = (weather_result_list_item["main"])["temp_min"]

    if daily_max==0:
        first_daily_max = (weather_result_list_item["main"])["temp_max"]
        daily_max = first_daily_max
    elif daily_max < (weather_result_list_item["main"])["temp_max"]:
        daily_max = (weather_result_list_item["main"])["temp_max"]

    mintemp = str((weather_result_list_item["main"])["temp_min"])
    maxtemp = str((weather_result_list_item["main"])["temp_max"])
    forecaststring = datetext1 + ' ' + tempdescription + str_pt3 + mintemp + "-" + maxtemp + " " + unitsname
#    print(forecaststring)
    index+=1

daily_min = str(daily_min)
daily_max = str(daily_max)
cnt_ = Counter(descriptionlist2)
most_common_description = ((cnt_.most_common(1))[0])[0]
forecaststring = datetext + ' ' + most_common_description + str_pt3 + daily_min + "-" + daily_max + " " + unitsname
print(forecaststring)

index=16
daily_min=0
daily_max=0
descriptionlist3=[]

for x in range(0, 8):
    weather_result_list_item = weather_result_list[index]
    datetext = (weather_result_list_item["dt_txt"]).split(' ')[0]
    datetext1 = (weather_result_list_item["dt_txt"])
    tempdescription = str(((weather_result_list_item["weather"])[0])['description'])
    descriptionlist3.append(tempdescription)
    if daily_min==0:
        first_daily_min = (weather_result_list_item["main"])["temp_min"]
        daily_min = first_daily_min
    elif daily_min > (weather_result_list_item["main"])["temp_min"]:
        daily_min = (weather_result_list_item["main"])["temp_min"]

    if daily_max==0:
        first_daily_max = (weather_result_list_item["main"])["temp_max"]
        daily_max = first_daily_max
    elif daily_max < (weather_result_list_item["main"])["temp_max"]:
        daily_max = (weather_result_list_item["main"])["temp_max"]

    mintemp = str((weather_result_list_item["main"])["temp_min"])
    maxtemp = str((weather_result_list_item["main"])["temp_max"])
    forecaststring = datetext1 + ' ' + tempdescription + str_pt3 + mintemp + "-" + maxtemp + " " + unitsname
#    print(forecaststring)
    index+=1

daily_min = str(daily_min)
daily_max = str(daily_max)
cnt_ = Counter(descriptionlist3)
most_common_description = ((cnt_.most_common(1))[0])[0]
forecaststring = datetext + ' ' + most_common_description + str_pt3 + daily_min + "-" + daily_max + " " + unitsname
print(forecaststring)

#13/11/2018 Cloudy with temperatures trailing from 6-12 celsius.
#14/11/2018 Sunny with temperatures trailing from 9-13 celsius.
#15/11/2018 Sunny with temperatures trailing from 10-14 celsius.
