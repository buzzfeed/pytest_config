import logging
import sys

level = logging.DEBUG

logger = logging.getLogger('pytest_config')
logger.setLevel(level)

formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(level)

handler.setFormatter(formatter)
logger.addHandler(handler)
