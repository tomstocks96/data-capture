import requests, time, datetime, logging, json

from confluent_kafka import Producer

from tsl_interface.tsl_interface import TslInterface
from table_parser.table_parser import TableParser

if __name__ == '__main__':
    url = 'https://livetiming.tsl-timing.com/230812?_gl=1*um61uw*_ga*MTA1MzIxMTgzOC4xNjc2NjQwMDk1*_ga_B9ZGX55TXH*MTY3NzEzODM5My4yLjEuMTY3NzE0MDgwMi4wLjAuMA..'
    parser = TableParser()

    kafka_producer = Producer({'bootstrap.servers': 'localhost:29092'})

    with TslInterface(session_url=url) as tsl_interface:
        metadata_in_row = ['Name', 'No']
        previous_reads = []
        while True:
            metadata = tsl_interface._get_metadata()
            table = tsl_interface._get_table()
            data = parser.parse_rows(table, metadata, metadata_in_row)

            for document in data:
                document = json.dumps(document, sort_keys=True, default=str)
                kafka_producer.produce('tsl-monitor-timings')
            kafka_producer.flush()
            
            time.sleep(5)

