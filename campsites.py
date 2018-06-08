#!/usr/bin/env python
import argparse
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

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

START_DATES = {
    # TODO: Add functionality to search for available campsites for multiple dates
}

def buildCampgroundUrl(campground_id):
    return CAMP_URL_BASE + CAMPGROUNDS[campground_id] + CAMP_URL_PARAMS + campground_id


def findCampSites(dates):
    for campground in CAMPGROUNDS:
        arrival_date = formatDate(dates["start_date"])
        departure_date = formatDate(dates["end_date"])

        chrome_options = Options()
        chrome_options.add_argument("headless")
        chrome_options.add_argument('window-size=1200,1100')

        browser = webdriver.Chrome(chrome_options=chrome_options)

        sendSeleniumRequest(browser, campground, arrival_date, departure_date)

        site_links = getSiteListSelenium(browser)
        print('Available campgrounds in ' + CAMPGROUNDS[campground].upper().replace('-', ' '))
        for i in site_links:
            print(i)
        browser.close();
    return site_links

def getNextDay(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    next_day = date_object + timedelta(days=1)
    return datetime.strftime(next_day, "%Y-%m-%d")

def formatDate(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    date_formatted = datetime.strftime(date_object, "%a %b %d %Y")
    return date_formatted

def getSiteListSelenium(browser):
    site_links = []
    sites = browser.find_elements_by_class_name("book")
    if len(sites) > 0:
        for site in sites:
            if site.text == "See Details":
                booking_link = site.get_attribute("href")
                site_links.append(booking_link)
    return site_links

def bookSite(browser):
    # TODO: Implment functionality to programmatically book a campsite
    book_button = browser.find_element_by_id("btnbookdates")
    book_button.click()
    email_input = browser.find_element_by_class_name('TextBoxRenderer')
    email_input.send_keys("<USERNAME>")
    password_input = browser.find_element_by_id('PasswordBoxRenderer')
    password_input.send_keys('<PASSWORD>')


def sendSeleniumRequest(browser, campground, arrival_date, departure_date):
    campground_url = buildCampgroundUrl(campground)
    keep_connecting = True
    while keep_connecting:
        try:
            browser.get(campground_url)
            arrival_date_input = browser.find_element_by_id("arrivalDate")
            arrival_date_input.send_keys(arrival_date)
            departure_date_input = browser.find_element_by_id("departureDate")
            departure_date_input.send_keys(departure_date)

            submitButton = browser.find_element_by_id("filter")
            submitButton.click()
            keep_connecting = False

        except:
            print("sleeping...")
            sleep(5)
            continue


if __name__ == "__main__":
    print("---")
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_date", required=True, type=str, help="Start date [YYYY-MM-DD]")
    parser.add_argument("--end_date", type=str, help="End date [YYYY-MM-DD]")

    args = parser.parse_args()
    arg_dict = vars(args)
    if 'end_date' not in arg_dict or not arg_dict['end_date']:
        arg_dict['end_date'] = getNextDay(arg_dict['start_date'])

    sites = findCampSites(arg_dict)
    print('end.')

