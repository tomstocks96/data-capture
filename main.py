import requests, time, datetime, logging

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from tsl_interface.tsl_interface import TslInterface

if __name__ == '__main__':
    url = 'https://livetiming.tsl-timing.com/230812?_gl=1*um61uw*_ga*MTA1MzIxMTgzOC4xNjc2NjQwMDk1*_ga_B9ZGX55TXH*MTY3NzEzODM5My4yLjEuMTY3NzE0MDgwMi4wLjAuMA..'

    with TslInterface(session_url=url) as tsl_interface:
        while True:
            data = tsl_interface._get_table()
            time.sleep(30)

