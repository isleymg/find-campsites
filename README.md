# Campsite Availability Scraping
### Forked from https://github.com/bri-bri/yosemite-camping
See Brian Hansen's README for information on his yosemite-camping script works. Credit goes to him for the idea and base functions.

This script produces a similar output to bri-bri/yosemite-camping by creating a session at recreation.gov and searching for hard-coded campsites during a specified date range.

### Changes In This Repo
Modifications were made to the original script because the search result pages at recreation.gov have changed from mostly static webpages to dynamically generated webpages.
The original method of only using the Requests module isn't able to grab all of the page content, and returns the message "Your browser does not support JavaScript!".

This updated scraper uses the Selenium module and headless Chrome webdriver to programatically control a browser and automate location and date inputs.

# Use Case
Did you miss the Yosemite campsite reservation day this month and now you're refreshing campground pages hoping someone cancels their reservation?
This script is useful for searching for Yosemite campsites after the first booking window for each month, when most campsites are full and you want to be notified when someone cancels their reservation.


# Instructions

Install requirements:
```
pip install -r requirements.txt
```
Use:
Open config.yml and edit campgrounds and dates to be searched.

Adding campgrounds:
I listed the more popular yosemite campsites in the config file. You can find other campsites and their parkID by going to www.recreation.gov, searching for your campsite, and finding the parkID in the URL.
For example: https://www.recreation.gov/camping/wawona/r/campgroundDetails.do?contractCode=NRSO&parkId=70924
    Enter into config.yaml:
      70924: wawona

Adding dates:
start_date is a mandatory input. If no end_date is specified, it will populate with the date of the next day and will search for just one night of camping.
Dates take input as YYYY-MM-DD.

Running the script: `python campsites.py`

