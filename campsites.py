#!/usr/bin/env python
import argparse
import copy
import requests
# from seleniumrequests import Chrome
from selenium import webdriver

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
from datetime import datetime, timedelta

CAMP_URL_BASE = "https://www.recreation.gov/camping/"
CAMP_URL_PARAMS = "/r/campsiteSearch.do?site=all&type=9&minimal=no&search=site&contractCode=NRSO&parkId="


CAMPGROUNDS = {
    # '70925': 'upper-pines',
    # '70928': 'lower-pines',
    # '70927': 'north-pines',
    # '70926': 'tuolumne-meadows',
    # '70930': 'crane-flat',
    '70929': 'hodgdon-meadow'
}

def buildCampgroundUrl(campground_id):
    return CAMP_URL_BASE + CAMPGROUNDS[campground_id] + CAMP_URL_PARAMS + campground_id


def findCampSites(dates):
    for campground in CAMPGROUNDS:
        arrival_date = formatDate(dates["start_date"])
        departure_date = formatDate(dates["end_date"])

        browser = webdriver.Chrome()
        content_raw = sendSeleniumRequest(browser, campground, arrival_date, departure_date)

        sites = getSiteListSelenium(browser)
    return sites


def getNextDay(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    next_day = date_object + timedelta(days=1)
    return datetime.strftime(next_day, "%Y-%m-%d")

def formatDate(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    date_formatted = datetime.strftime(date_object, "%a %b %d %Y")
    return date_formatted

def getSiteListSelenium(browser):
    sites = browser.find_elements_by_class_name("book")
    if len(sites) > 0:
        sites[0].click()
        bookSite(browser)
    else:
        return

def bookSite(browser):
    book_button = browser.find_element_by_id("btnbookdates")
    book_button.click()

    email_input = browser.find_element_by_class_name('TextBoxRenderer')
    email_input.send_keys("isleymgao@gmail.com")
    password_input = browser.find_element_by_id('PasswordBoxRenderer')


def sendSeleniumRequest(browser, campground, arrival_date, departure_date):
    campground_url = buildCampgroundUrl(campground)

    resp = requests.get(campground_url)
    if resp.status_code != 200:
        raise Exception("FailedRequest",
                        "ERROR, %d code received from %s".format(resp.status_code, campground_url))
    else:
        browser.get(campground_url)

        arrival_date_input = browser.find_element_by_id("arrivalDate")
        arrival_date_input.send_keys(arrival_date)
        departure_date_input = browser.find_element_by_id("departureDate")
        departure_date_input.send_keys(departure_date)

        submitButton = browser.find_element_by_id("filter")
        submitButton.click()


if __name__ == "__main__":
    print("--Looking for campsites--")
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--start_date", required=True, type=str, help="Start date [YYYY-MM-DD]")
    # parser.add_argument("--end_date", type=str, help="End date [YYYY-MM-DD]")
    #
    # args = parser.parse_args()
    # arg_dict = vars(args)
    # if 'end_date' not in arg_dict or not arg_dict['end_date']:
    #     arg_dict['end_date'] = getNextDay(arg_dict['start_date'])

    # sites = findCampSites(arg_dict)
    sites = findCampSites({'start_date': '2018-09-28', 'end_date': '2018-09-30'})
    print(sites)
    if sites:
        print('found: ')
        for site in sites:
            print (site)
            # "&arrivalDate={}&departureDate={}" \
            # .format(
            #         urllib.quote_plus(formatDate(arg_dict['start_date'])),
            #         urllib.quote_plus(formatDate(arg_dict['end_date'])))
    print('end.')

