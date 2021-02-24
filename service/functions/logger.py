import logging


logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
logger.propagate = False
hand = logging.StreamHandler()
hand.setLevel(logging.INFO)
hand.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
logger.addHandler(hand)
logger.info('Logger was created')
