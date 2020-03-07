import requests
from logger import logger

url = 'https://data.nhi.gov.tw/resource/mask/maskdata.csv'

def get_maskdata():
    logger.info('=== processing ===')
    # download file
    logger.info('=== downloading files ===')
    r = requests.get(url)
    try:
        with open('./data/maskdata.csv','wb') as f:
            f.write(r.content)
            logger.info('[get_data] open maskdata.csv -> Success')
            logger.info('=== download completed ===')
            return True
    except:
        logger.error('[get_data] open maskdata.csv -> Failed')
        logger.warning('=== download failed ===')
        return False