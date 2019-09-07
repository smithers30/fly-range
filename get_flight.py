from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import os, stat
import shutil
import time
import sys
import math
import cgi
import pdb
import re
import glob

stashPrice = 0
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 30)
bestPriceURL = ''

def refresh(url=driver.current_url):
    driver.get(url)

def rmFiles(dir='images', ext='.png'):
    files = glob.glob(dir + '/*' + ext)

    for f in files:
        os.remove(f)

def performSearch():
    global stashPrice

    driver.get('https://www.google.com/flights#flt=/m/02_n7./m/0rh6k.2019-09-04*/m/0rh6k./m/02_n7.2019-09-08;c:USD;e:1;so:1;sd:1;t:f')
    # driver.get('https://www.google.com/flights#flt=/m/02_n7./m/0bld8.2019-08-30*/m/0bld8./m/02_n7.2019-09-03;c:USD;e:1;so:1;sd:1;t:f') # POLAND
    # driver.get("https://www.google.com/flights#flt=/m/01_d4./m/07dfk.2019-11-01*/m/07dfk./m/01_d4.2019-11-02;c:USD;e:1;so:1;sd:1;t:f") JAPAN
    driver.execute_script('''
        var guinnea = document.querySelector("div");

        guinnea.innerHTML = guinnea.innerHTML +
        "<style> * { -o-transition-property: none !important; -moz-transition-property: none !important; -ms-transition-property: none !important; -webkit-transition-property: none !important; transition-property: none !important; } </style>";
    ''')

    def compareResult():
        global stashPrice
        global bestPriceURL

        def getResultPrice():
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.flt-subhead1.gws-flights-results__price')))
                resultsEle = driver.find_element_by_css_selector('div.flt-subhead1.gws-flights-results__price')
                resultsEle.text

                if resultsEle and resultsEle is not None and resultsEle.text:
                    return resultsEle
                else:
                    raise Exception('None type object')
            except (TimeoutException, StaleElementReferenceException, Exception) as e:
                refresh()
                getResultPrice()

        resultPriceEle = getResultPrice()
        roundTripStr = re.sub('[^\d]', '', resultPriceEle.text).strip()
        roundTripPrice = (int(roundTripStr) if roundTripStr else 0)

        if roundTripPrice:
            priceStamp = 'images/best_price_' + str(int(time.time())) + '.png'

            if roundTripPrice < stashPrice:
                stashPrice = roundTripPrice
                driver.implicitly_wait(5)
                bestPriceURL = driver.current_url
                rmFiles()
                driver.save_screenshot(priceStamp)
            elif roundTripPrice == stashPrice:
                driver.save_screenshot(priceStamp)

        return [roundTripPrice, resultPriceEle]

    stashPrice = compareResult()[0]

    if stashPrice:
        for dept in range(0, 250):
            currURL = driver.current_url
            replStart = currURL.rfind('.') + 1
            lastDate = currURL[replStart:(replStart + 10)]
            firstDateIdx = currURL.index(currURL.split('.')[4])
            firstDate = currURL[firstDateIdx:(firstDateIdx + 10)]
            firstDateObj = datetime.strptime(firstDate, '%Y-%m-%d') + timedelta(days=1)

            driver.get(
                currURL
                    .replace(firstDate, str(firstDateObj).split(' ')[0])
                    .replace(lastDate, str(firstDateObj + timedelta(days=2)).split(' ')[0])
            )

            for rtn in range(0, 2):
                try:
                    returnEle = compareResult()[1]
                    nextBtn = driver.find_elements_by_css_selector('.gws-flights-form__next')[1]
                    nextBtn.click()
                    wait.until(
                        EC.staleness_of(returnEle)
                    )
                except:
                    print('fail')


    return stashPrice

currLow = performSearch()

if currLow:
    print('The lowest price found was: ' + '${:,.2f}'.format(currLow))
    print(bestPriceURL)
else:
    print('Price not found, adjust date range.')

driver.close()
