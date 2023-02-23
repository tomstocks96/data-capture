import requests, time, datetime, logging
from typing import List

import pandas as pd
from selenium import webdriver

class TableParser:
    def __init__(self):
       pass

    def parse_rows(self, table: pd.DataFrame, 
                   metadata: dict = {}, 
                   metadata_in_row: List[str] = []) -> List[dict]:
        
      unpivoted_data = []
      doc_array = table.to_dict(orient='records')

      for doc in doc_array:
         for column_name in metadata_in_row:
               metadata[column_name] = doc.get(column_name,'')
               doc.pop(column_name,None)

         for data_column in doc:
               unpivoted_doc = dict(metadata)
               unpivoted_doc['key'] = data_column
               unpivoted_doc['value'] = doc[data_column]
               if unpivoted_doc['value'] != 'NaN':
                  unpivoted_data.append(unpivoted_doc)
   
      return unpivoted_data
