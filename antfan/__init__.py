import antfan
import logging

# create logger
logger = logging.getLogger('antfan')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
