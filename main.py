import requests, time, datetime, logging, json, sys, os, argparse

from confluent_kafka import Producer

from tsl_interface.tsl_interface import TslInterface
from table_parser.table_parser import TableParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', default='docker')
    
    args = parser.parse_args()
    
    if args.environment == 'host':
        KAFKA_URL = 'localhost:9092'
        AGENT_URL = 'http://localhost:4444/wd/hub'
        SCRAPE_URL = 'https://livetiming.tsl-timing.com/231541'
        
    elif args.environment == 'docker':
        KAFKA_URL = 'kafka:29092'
        AGENT_URL = 'http://scrape-agent:4444/wd/hub'
        SCRAPE_URL = os.environ['SCRAPE_URL']
    else:
        raise ValueError('Environment argument is not a supported value. Should be one of "docker", "host"')
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    parser = TableParser()

    # sleep to allow scrape agent to boot
    logger.info('Internal set up done, sleeping to ensure dependency availability')
    time.sleep(5)

    kafka_producer = Producer({'bootstrap.servers': KAFKA_URL})

    logger.info('starting scrape loop')
    with TslInterface(session_url=SCRAPE_URL, scrape_agent_url=AGENT_URL) as tsl_interface:
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
            time.sleep(8)

