# Campsite Availability Scraping
### Forked from https://github.com/bri-bri/yosemite-camping
See Brian Hansen's README for information on his yosemite-camping script works. Credit goes to him for the idea and base functions.

This script produces a similar output to bri-bri/yosemite-camping by creating a session at recreation.gov and searching for hard-coded campsites during a specified date range.

Modifications were made to the original script because the search result pages at recreation.gov have changed from mostly static webpages to dynamically generated webpages.
The original method of only using the Requests module isn't able to grab all of the page content, and returns the message "Your browser does not support JavaScript!".

This updated scraper uses the Selenium module and headless Chrome webdriver to programatically control a browser and automate location and date inputs.

# Use Case
This script is useful for searching for Yosemite campsites after the first booking window for each month, when most campsites are full and you want to be notified when someone cancels their reservation.


# Instructions (same as bri-bri/yosemite-camping)

Install requirements:
```
pip install -r requirements.txt
```
Use: `python campsites.py --start_date 2015-04-24 --end_date 2015-04-25`

Best use is to set a crontab on a ~5 minute interval (I've found that a 10-minute interval is too long because the campsites will be taken by the time I'm able to act on the alert).

`campsites.sh` demos a simple bash script wrapping the python script and opening a text file if results are found that could be set up to be triggered through cron.

