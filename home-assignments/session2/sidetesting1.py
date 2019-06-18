from pyowm import OWM
import click
import re
import math
from collections import Counter

API_key = '42576a539c72dd7b5efaca6e382402c9'
owm_object = OWM(API_key)
citycountrycode = 'IE'
usagemsg = "Usage: python cli.py --city <CITYNAME> --forecast <TODAY / TODAY+x> [-c, -f]"
forecasterrmsg = "Usage: --forecast <TODAY / TODAY+x> (where x is between 1-5 (e.g.: TODAY+3))"
supportsonlydublinmsg = "Currently this script only supports Dublin Ireland, so the only valid city value is 'dublin'"
#forecastedrequesteddaysgreaterthanavailable = "The maximum available forecast days available is " + \
#                                              availableforecastdays + ". Displaying " + availableforecastdays


@click.command()
@click.option('--city')
@click.option('--forecast')
@click.option('-c', 'unitsname', flag_value='celsius')
@click.option('-f', 'unitsname', flag_value='fahrenheit')
def getweatherdisplay(city, forecast, unitsname):
    argumentcheck = validatearguments(city, forecast, unitsname)
    errormsg = argumentcheck[0]
    cityid = argumentcheck[1]
    forecasttype = argumentcheck[2]
    if errormsg:
        print(errormsg)
    else:
        forecastcurrentstring = getsinglelineoutputstring(cityid, unitsname)
        if forecasttype == "current":
            print(forecastcurrentstring)
        elif forecasttype == "future":
            print(forecastcurrentstring)
            forecastdays = int(forecast.split('+')[1])
            forecastitemslist = getforecastfuturestring(city, citycountrycode, forecastdays, unitsname)
            availableforecastdays = str(len(forecastitemslist))

            if forecastdays > int(len(forecastitemslist)):
                print("The maximum available forecast days available is " + \
                                              availableforecastdays + ". Displaying " + availableforecastdays)

            for forecastitem in forecastitemslist:
                print(forecastitem)


def getforecastfuturestring(city, citycountrycode, forecastdays, unitsname):
    forecastedrequesteddaysgreaterthanavailable=''
    forecastobject = owm_object.three_hours_forecast((city + "," + citycountrycode))
    forecastresultslist = (forecastobject.get_forecast()).get_weathers()
    tomorrowfirstitem_listindexnum = getfirstindexnum(forecastresultslist)
    futurelistonly = forecastresultslist[tomorrowfirstitem_listindexnum:-1]
    frac, whole = math.modf(len(futurelistonly) / 8)
    futurelistforecastdaysavailable = [whole, frac]

    if forecastdays > int(futurelistforecastdaysavailable[0]):
        forecastdaystoprocess = int(futurelistforecastdaysavailable[0])
    else:
        forecastdaystoprocess = int(forecastdays)

    formattedweather = getformattedweatherperday(futurelistonly, forecastdaystoprocess, unitsname)
    return formattedweather

def getformattedweatherperday(futurelistonly, forecastdaystoprocess, unitsname):
    totaldayslistindex = 0
    formattedlist=[]

    for i in range(forecastdaystoprocess):
        onedaylistchunk = futurelistonly[totaldayslistindex:(totaldayslistindex + 8)]
        forecastdayoutputstring = processweatherdatarange(onedaylistchunk, unitsname)
        formattedlist.append(forecastdayoutputstring)
        totaldayslistindex = totaldayslistindex + 9

    return formattedlist


def getfirstindexnum(forecastresultslist):
    firstquerydate = ((forecastresultslist[0]).get_reference_time('iso')).split(' ')[0]

    listcounter = 0
    datebeingchecked = firstquerydate

    while datebeingchecked == firstquerydate:
        datebeingchecked = ((forecastresultslist[listcounter]).get_reference_time('iso')).split(' ')[0]
        listcounter += 1
    listcounter -= 1
    return listcounter


def processweatherdatarange(onedaylistchunk, unitsname):
    index = 0
    dailymin = 0
    dailymax = 0
    descriptionlist = []
    datetext = ""

    loopstart = 1

    for x in range(0, 8):
        weather_result_list_item = onedaylistchunk[index]
        datetext = weather_result_list_item.get_reference_time('iso').split(' ')[0]
        tempdescription = weather_result_list_item.get_detailed_status()
        descriptionlist.append(tempdescription)
        temperature = (weather_result_list_item.get_temperature(unitsname))['temp']
        if loopstart:
            dailymin = temperature
            dailymax = temperature
            loopstart = 0
        else:
            if dailymin > temperature:
                dailymin = temperature
            if dailymax < temperature:
                dailymax = temperature
        index += 1
    most_common_description = (((Counter(descriptionlist)).most_common(1))[0])[0]
    forecaststring = datetext + ' ' + most_common_description + " with temperatures trailing from " + str(dailymin) + \
                     "-" + str(dailymax) + " " + unitsname
    return forecaststring


def validatearguments(city, forecast, unitsname):
    returnmsg = ['', '', '']
    if not city or not forecast or not unitsname:
        returnmsg = (usagemsg, '', '')
    else:
        cityid = getcityid(city)
        if cityid != 2964574:
            returnmsg = (supportsonlydublinmsg, '', '')
        else:
            match1 = re.search("^TODAY$", forecast)
            match2 = re.search("^TODAY\+[1-5]$", forecast)
            if match1:
                returnmsg = ('', cityid, 'current')
            if match2:
                returnmsg = ('', cityid, 'future')
            if not match1 and not match2:
                returnmsg = (forecasterrmsg, '', '')
    return returnmsg


def getcityid(city):
    owm_cityid_registry = owm_object.city_id_registry()
    citysearch_resultslist = owm_cityid_registry.ids_for(city, matching='like')
    cityid = ""
    for cityresult in citysearch_resultslist:
        citynamelength = len((cityresult[1]).split())
        if cityresult[2] == citycountrycode and citynamelength == 1:
            cityid = cityresult[0]
    return cityid


def getsinglelineoutputstring(cityid, unitsname):
    observedweather_owmobject = owm_object.weather_at_id(cityid)
    weathertemppair = getweatherandtemp(observedweather_owmobject, unitsname)
    outputstring = formatoutputstring(weathertemppair, unitsname)
    return outputstring


def getweatherandtemp(observedweather_owmobject, unitsname):
    w = observedweather_owmobject.get_weather()
    tempdescription = w.get_detailed_status()
    tempmin = (w.get_temperature(unitsname))['temp_min']
    tempmax = (w.get_temperature(unitsname))['temp_max']
    l = observedweather_owmobject.get_location()
    cityname = l.get_name()
    weathertemppair=[cityname, tempdescription, tempmin, tempmax]
    return weathertemppair


def formatoutputstring(weathertemppair, unitsname):
    outputstring = "The weather in " + weathertemppair[0] + " today is " + weathertemppair[1] + \
                   " with temperatures trailing from " + str(weathertemppair[2]) + "-" + str(weathertemppair[3]) \
                   + " " + unitsname
    return outputstring


if __name__ == '__main__':
    getweatherdisplay()
