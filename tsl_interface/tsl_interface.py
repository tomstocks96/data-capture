import pandas as pd
import requests, time, datetime, logging

import pandas as pd
from selenium import webdriver

class TslInterface:
    def __init__(self, session_url:str):
        self.url = session_url

    def __enter__(self):
        self._open_page()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        time.sleep(3)
        #close the browser
        self.driver.close()
        self.driver.quit()
        return
        
    def _open_page(self): 
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("start-maximized") # // open Browser in maximized mode
        options.add_argument("disable-infobars") # // disabling infobars
        options.add_argument("--disable-extensions") # // disabling extensions
        options.add_argument("--disable-gpu") # // applicable to windows os only
        options.add_argument("--disable-dev-shm-usage") # // overcome limited resource problems
        options.add_argument("--no-sandbox") # // Bypass OS security model
        self.driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
        )
        print('Executing')
        #maximize the window size
        self.driver.maximize_window()
        #navigate to browserstack.com
        self.driver.get(url=self.url)
        #click on the Get started for free button
        time.sleep(3)
        self.driver.find_element(by='id', value='acceptTerms').click()

    def _get_metadata(self: str) -> str:
        time.sleep(3)
        series = self.driver.find_element(by='id', value='seriesName').text
        session = self.driver.find_element(by='id', value='sessionName').text

        session_date = datetime.datetime.now().date()
        metadata = {
            'series': series,
            'session': session,
            'date': session_date
        }
        return metadata

    def _get_table(self: str) -> str:
        table = self.driver.find_element(by='id', value='ResultsTableContainer')
        sub_table = table.find_element(by='id', value='tablebody')
        
        time.sleep(3)
        html = sub_table.get_attribute('outerHTML')
        table = pd.read_html(html)
        table = table[0]

        return table
    
