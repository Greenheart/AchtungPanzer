import logging
from controller import Controller

logging.basicConfig(filename='example.log', level=logging.DEBUG)

if __name__ == "__main__":
	logging.info('Starting...')
	c = Controller()
	c.run()