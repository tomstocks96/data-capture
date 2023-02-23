import pandas as pd
import requests

class TslInterface:
    def __init__(self) -> None:
        pass    
    
    def get_timing_board(self, url):
        pass

    def _get_html(self, url: str) -> str:
        page = requests.get(url=url)
        return page
    
