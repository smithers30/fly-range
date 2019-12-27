import requests
import json
import sys
import urllib
from datetime import datetime, timedelta, date

def strDate(dateObj, addDays=0):
    return str(datetime.strptime(str(dateObj), '%Y-%m-%d') + timedelta(days=addDays)).split(' ')[0]

params = {'from': '', 'to': '', 'spread': 5, 'seek': 3, 'range': 100, 'start': strDate(date.today())}
args = sys.argv
lowPrice = 0

for key, arg in enumerate(args):
    stripVar = arg.replace('--', '')

    if stripVar in params:
        params[stripVar] = args[key + 1].upper()

if params['from'] and params['to']:
    for day in range(0, int(params['range'])):
        arrive = strDate(params['start'], params['spread'])

        for dayOut in range(0, int(params['seek']) + 1):
            asyncParams = '[[[[[[null,[["' + params['from'] + '",0]]],[null,[["' + params['to'] + '",0]]],["' + params['start'] + '"]],[[null,[["' + params['to'] + '",0]]],[null,[["' + params['from'] + '",0]]],["' + strDate(arrive, dayOut) + '"]]],null,[],null,null,null,null,1,null,2,null,null,null,null,null,true],[[[null,[],[],[],[],null,[],[]],[null,[],[],[],[],null,[],[]]]],null,"USD",null,[]],[0]]'
            url = 'http://www.google.com/async/flights/search?async=data:' + urllib.quote(asyncParams.encode("utf-8")) + ',s:s,tfg-bgr:%5B%22!HR6lHj9C6Hein_9L_R5YnfVDgE9EmCQCAAAAN1IAAAAJmQGTwQN3PvwWZNvYd4HMWByoNCmygBioNH0KHeMzTg3zT__t46hHogAda8OaO-nEj9FpftdXY1y8HoxSTYxpYyBzRAvaW5FrmbCC4WnG6qC-pfnBbliWYUPSRknXCdgMID-vTgG1kIK_U3hQs8NLjTokU9EZ_dPiSXFbDeEbFv1KwVup7HkmEn_HUhtw4nz6as03ar5dTNxHf19oS6N5UzKmo-brJqdXtoaVLw7HkgWMgXXV9U89iqcfEMoIFwjxFVFYAj9N9UJXIvJIo4lr5TyBXIqo4v1IK2I6_zlSYBJNOg_Zt2FMg1kWfpSVC6Q0lBUXVE1mzr5HX85lWT3nR49UHEpgYetX8X7j2RCWTKIKlwAy0VZOTcWgYAB2WEQtleR1bT-0_iONaJQJfnWJ1Is8V6oNcoMptze96RLhuzbxg0khJAF6fBwEpLqSOEsvBPmLHduiwOdD74ooyr5bSWSqtDfaZ3EyY6dTek_yWU0glI9YSPyfySmogaIZxhLOoX5yNyBTOQ0P96XAwM7d8Vd3fFA_zA%22%2Cnull%2Cnull%2C10%2C62%2Cnull%2Cnull%2C0%5D,_fmt:jspb'
            content = requests.get(url, allow_redirects=True).content
            flightData = json.loads(content.replace(content.split('\n')[0], '', 1))

            def recursiveArray(childAry):
                global lowPrice

                for item in childAry:
                    if type(item) == list:
                        recursiveArray(item)
                        
                    if type(item) == unicode and '$' in item and 'USD' in childAry:
                        thisLow = [priceInt for priceInt in childAry if type(priceInt) == int][0]

                        if not lowPrice or thisLow < lowPrice:
                            lowPrice = thisLow
                            print childAry, params['start'], strDate(arrive, dayOut)
                        if thisLow == lowPrice:
                            print childAry, params['start'], strDate(arrive, dayOut)

            recursiveArray(flightData[flightData.keys()[0]])

        params['start'] = strDate(params['start'], 1)









