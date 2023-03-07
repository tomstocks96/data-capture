import requests, time, datetime, logging, json, sys, os

from confluent_kafka import Producer

from tsl_interface.tsl_interface import TslInterface
from table_parser.table_parser import TableParser

if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #scrape_url = os.environ['SCRAPE_URL']
    scrape_url = 'https://livetiming.tsl-timing.com/231018'

    parser = TableParser()

    kafka_producer = Producer({'bootstrap.servers': 'kafka:29092'})

    logger.info('starting scrape loop')
    with TslInterface(session_url=scrape_url) as tsl_interface:
        while True:
            logger.info('getting metadata')
            metadata = tsl_interface._get_metadata()
            logger.info('getting table')
            table = tsl_interface._get_table()
            logger.info('parsing table')
            data = parser.parse_rows(table, metadata)
    
            logger.info('parsing rows')
            for document in data:
                document_to_produce = dict(document)
                document_to_produce['scrape_timestamp'] = datetime.datetime.now()
                document_to_produce = json.dumps(document_to_produce, sort_keys=True, default=str)

                logger.debug(f'producing document {document_to_produce}')
                kafka_producer.produce('tsl-monitor-timings', document_to_produce.encode('utf-8'), 'timing'.encode('utf8'))
                
            kafka_producer.flush()
            
            logger.info('sleeping before next scrape')
            time.sleep(30)

