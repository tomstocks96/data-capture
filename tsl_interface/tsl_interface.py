import pandas as pd
import requests, time, datetime, logging, os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

class TslInterface:
    def __init__(self, session_url:str, scrape_agent_url: str):
        self.session_url = session_url
        self.scrape_agent_url = scrape_agent_url
        self.logger = logging.getLogger(__name__)

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
        command_executor=self.scrape_agent_url,
        options=options
        )
        #maximize the window size
        self.driver.maximize_window()
        self.logger.info('driver initiated')
        #navigate to browserstack.com
        self.driver.get(url=self.session_url)
        self.logger.info('driver loaded webpage')
        time.sleep(3)
        # try: 
        #     self.driver.find_element(by='id', value='acceptTerms').click()
        # except NoSuchElementException:
        #     self.logger.error(f'T&C accept button could not be found')
        #     raise


    def _get_metadata(self) -> dict:
        time.sleep(1)
        try:
            series = self.driver.find_element(by=By.XPATH, value='//h1[contains(@class, "seriesName")]').text
        except NoSuchElementException:
            self.logger.warn(f'series metadata could not be found')
            raise

        try:
            session = self.driver.find_element(by=By.XPATH, value='//h2[contains(@class, "sessionName")]').text
        except NoSuchElementException:
            self.logger.warn(f'session metadata could not be found')
            raise

        try:
            
            circuit = os.environ.get('CIRCUIT', 'Unspecified')
        except NoSuchElementException:
            self.logger.warn(f'circuit metadata could not be found')
            raise

        try:
            weather_conditions = self.driver.find_element(by=By.XPATH, value='//div[contains(@class, "weather widget")]/span').text
        except NoSuchElementException:
            self.logger.warn(f'weather metadata could not be found')
            raise

        try:
            circuit_conditions = self.driver.find_element(by=By.XPATH, value='//div[contains(@class, "track widget")]/span').text
        except NoSuchElementException:
            self.logger.warn(f'circuit metadata could not be found')
            raise

        try:
            track_status = self.driver.find_element(by=By.XPATH, value='//div[contains(@class, "statusText")]').text
        except NoSuchElementException:
            self.logger.warn(f'circuit metadata could not be found')
            raise
        
        
        session_date = datetime.datetime.now().date()
        metadata = {
            'series': series,
            'session': session,
            'circuit': circuit,
            'date': session_date,
            'weather_conditions': weather_conditions,
            'circuit_conditions': circuit_conditions,
            'track_status': track_status
        }
    
        return metadata
        

    def _get_table(self) -> pd.DataFrame:
        table = self.driver.find_element(by=By.XPATH, value='//table[contains(@class, "result-table banded sticky")]')
        
        time.sleep(1)
        html = table.get_attribute('outerHTML')
        table = pd.read_html(html)
        table = table[0]

        return table
    
