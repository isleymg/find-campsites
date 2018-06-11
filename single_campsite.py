from selenium import webdriver

HODGDON_URL = "https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70929&calarvdate=06/08/2018&sitepage=true&startIdx=1"

browser = webdriver.Chrome()
browser.get(HODGDON_URL)
