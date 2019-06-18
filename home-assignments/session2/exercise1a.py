from pyowm import OWM
import click
import re

#`python cli.py --city dublin --forecast TODAY -c`

API_key = '42576a539c72dd7b5efaca6e382402c9'
owm_object = OWM(API_key)
citycountrycode = 'IE'


@click.command()
@click.option('--city')
@click.option('--forecast', default='TODAY')
@click.option('-c', 'unitsname', flag_value='celsius')
@click.option('-f', 'unitsname', flag_value='fahrenheit')
def getweatherdisplay(city, forecast, unitsname):
    cityid = getcityid(city)
    match = re.search("^TODAY$", forecast)
    if match:
        outputstring = getsinglelineoutputstring(cityid, unitsname)
        print(outputstring)
    else:
        match = re.search("^TODAY\+[1-5]$", forecast)
        if match:
            outputstring = getsinglelineoutputstring(cityid, unitsname)
            print(outputstring)
            forecastparamater = city + "," + citycountrycode
            fc = owm_object.three_hours_forecast(forecastparamater)
            f = fc.get_forecast()
            interval = f.get_interval()
            print(interval)
            lst = f.get_weathers()
            for weather in f:
                print(weather.get_reference_time('iso'), weather.get_status())
        else:
            print("Syntax error. Valid syntax: 'TODAY' or 'TODAY+x', where x is a number between 1-5 (e.g.: TODAY+3)")


def getsinglelineoutputstring(cityid,unitsname):
    observedweather_owmobject = owm_object.weather_at_id(cityid)
    weathertemppair = getweatherandtemp(observedweather_owmobject, unitsname)
    outputstring = formatoutputstring(weathertemppair, unitsname)
    return outputstring


def getcityid(city):
    owm_cityid_registry = owm_object.city_id_registry()
    citysearch_resultslist = owm_cityid_registry.ids_for(city, matching='like')
    cityid = ""
    for cityresult in citysearch_resultslist:
        citynamelength = len((cityresult[1]).split())
        if cityresult[2] == citycountrycode and citynamelength == 1:
            cityid = cityresult[0]
    return cityid


def getweatherandtemp(observedweather_owmobject,unitsname):
    w = observedweather_owmobject.get_weather()
    tempdescription = w.get_detailed_status()
    tempmin = (w.get_temperature(unitsname))['temp_min']
    tempmax = (w.get_temperature(unitsname))['temp_max']
    l = observedweather_owmobject.get_location()
    cityname = l.get_name()
    weathertemppair=[cityname, tempdescription, tempmin, tempmax]
    return weathertemppair


def formatoutputstring(weathertemppair, unitsname):
    str_pt1 = "The weather in "
    str_city = weathertemppair[0]
    str_pt2 = " today is "
    str_desc = weathertemppair[1]
    str_pt3 = " with temperatures trailing from "
    str_min = str(weathertemppair[2])
    str_max = str(weathertemppair[3])
    outputstring = str_pt1 + str_city + str_pt2 + str_desc + str_pt3 + str_min + "-" + str_max + " " + unitsname
    return outputstring


if __name__ == '__main__':
    getweatherdisplay()
