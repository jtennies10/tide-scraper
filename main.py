from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from daylightlowtides import DaylightLowTides
from lowtide import LowTide

def scrape_location_low_tides(location):
    '''
    Returns an array of LowTide objects that occur during the daytime
    '''
    driver = webdriver.Firefox()
    
    #navigate to the tide site and input the passed in location
    driver.get('https://www.tide-forecast.com/')
    driver.implicitly_wait(3)
    location_element = driver.find_element_by_id("location")
    location_element.send_keys(location)
    location_element.send_keys(Keys.RETURN)
    daylight_low_tides = []

    tide_elements = driver.find_elements_by_xpath("//div[@class='tide-table__tide-data']")
    for tide_elem in tide_elements:
        #retrieve the sunrise and sunset times for the day
        tide_extra_data_table = tide_elem.find_element_by_xpath("./table[@class='tide-table__tide-data--sun-moon not_in_print']/tbody")
        sunrise_time = _get_military_time(
            tide_extra_data_table.find_element_by_xpath("./tr/td[contains(text(), 'Sunrise')]/span").get_attribute('innerHTML'))
        sunset_time = _get_military_time(
            tide_extra_data_table.find_element_by_xpath("./tr/td[contains(text(), 'Sunset')]/span").get_attribute('innerHTML'))

        #retrieve the tide_data_table and all of it's low tide table rows
        tide_data_table = tide_elem.find_element_by_xpath("./table/tbody[@class='tide-table__tide-data--tides']")
        low_tides = tide_data_table.find_elements_by_xpath("./tr[./td[contains(text(), 'Low Tide')]]")
        for tide in low_tides:
            time = tide.find_element_by_xpath("./td/b").get_attribute('innerHTML')
            military_time = _get_military_time(time)

            if military_time < sunrise_time or military_time > sunset_time:
                continue

            date = tide.find_element_by_xpath("./td/span").get_attribute('innerHTML')
            height = tide.find_element_by_xpath("./td[@class='two-units-length-value']/b").get_attribute('innerHTML')

            fulltime = '%s %s' % (time, date)
            daylight_low_tides.append(LowTide(fulltime, height))

    driver.close()

    return daylight_low_tides


def _get_military_time(s):
    '''
        Takes a string representing a time and converts it to military time, represented as an integer from 0 to 2399
    '''
    time = s[:-2].strip() #returns the time, no AM or PM
    time_mod = s[-2:].strip() #returns AM or PM 
    hour, minute = time.split(':')
    military_time = 0
    if time_mod == 'AM' and hour == '12':
        military_time = int(minute)
    elif time_mod == 'PM':
        if hour == '12':
            military_time = int(hour) * 100 + int(minute)
        else:
            military_time = int(hour) * 100 + 1200 + int(minute)
    else:
        military_time = int(hour) * 100 + int(minute)

    return military_time

if __name__ == '__main__':
    locations = []

    with open('locations.txt', 'r') as f:
        locations = f.read().split('\n')

    scraped_data = []

    for loc in locations:
        scraped_data.append(DaylightLowTides(loc, scrape_location_low_tides(loc)))

    with open('scraped_data.txt', 'w') as f:
        for loc_data in scraped_data:
            print(str(loc_data.low_tides))
            f.write(str(loc_data))

    