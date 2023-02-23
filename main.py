import requests, time, datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from tsl_interface.tsl_interface import TslInterface

if __name__ == '__main__':
    url = 'https://livetiming.tsl-timing.com/230812?_gl=1*um61uw*_ga*MTA1MzIxMTgzOC4xNjc2NjQwMDk1*_ga_B9ZGX55TXH*MTY3NzEzODM5My4yLjEuMTY3NzE0MDgwMi4wLjAuMA..'
    tsl_interface = TslInterface()

    print("Test Execution Started")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("start-maximized") # // open Browser in maximized mode
    options.add_argument("disable-infobars") # // disabling infobars
    options.add_argument("--disable-extensions") # // disabling extensions
    options.add_argument("--disable-gpu") # // applicable to windows os only
    options.add_argument("--disable-dev-shm-usage") # // overcome limited resource problems
    options.add_argument("--no-sandbox") # // Bypass OS security model
    driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
    )
    #maximize the window size
    driver.maximize_window()
    print("Test Execution Started")
    time.sleep(3)
    #navigate to browserstack.com
    driver.get("https://livetiming.tsl-timing.com/230812?_gl=1*um61uw*_ga*MTA1MzIxMTgzOC4xNjc2NjQwMDk1*_ga_B9ZGX55TXH*MTY3NzEzODM5My4yLjEuMTY3NzE0MDgwMi4wLjAuMA..")
    time.sleep(2)
    print("Test Execution Started")
    #click on the Get started for free button
    driver.find_element(by='id', value='acceptTerms').click()

    table = driver.find_element(by='id', value='ResultsTableContainer')
    time.sleep(3)
    subtable = table.find_element(by='id', value='tablebody')

    html = subtable.get_attribute('outerHTML')
    timestamp= datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

    data = pd.read_html(html)
    data = data[0]
    data.to_csv(f'./test-data/scrapes/{timestamp}.csv')

    html = driver.page_source

    time.sleep(3)
    #close the browser
    driver.close()
    driver.quit()
    print("Test Execution Successfully Completed!")