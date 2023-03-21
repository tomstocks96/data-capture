import json, logging
from typing import List

import pandas as pd

class TableParser:
   def __init__(self):
      self.previous_reads = []
      self.logger = logging.getLogger(__name__)
   
   def isNaN(self, num):
      return num != num

   def parse_rows(self, table: pd.DataFrame, 
                  metadata: dict = {}) -> List[dict]:
      self.logger.info('parsing dataframe')
      data = []
      self.logger.debug(f'metadata is {metadata}')
      self.logger.debug(f'received table: {table.head(3)}')
      doc_array = [row.dropna().to_dict() for index,row in table.iterrows()]
      self.logger.debug(f'created json array: {doc_array[:2]}')

      for doc in doc_array:
         doc.update(metadata)
         self.logger.debug(f'checking keys for sector 3 time: {doc.keys()}')

         if 'S3' in doc.keys() and doc.get('S3','') != 'IN PIT':
            laps = doc['Laps']
            self.logger.debug(f'S3 time detected, laps went from {laps} to {laps - 1}')
            doc['Laps'] = doc['Laps'] - 1
            
         if doc not in self.previous_reads:
            self.logger.debug(f'new document {doc}')
            data.append(doc)
         else:
            self.logger.debug(f'previously seen document')
      
      self.previous_reads = doc_array.copy()
      return data
