import logging
from controller import Controller

DEBUG = True

if DEBUG:
	logging.basicConfig(filename='example.log', level=logging.DEBUG)
else:
	logging.basicConfig(filename='example.log', level=logging.INFO)


if __name__ == "__main__":
	logging.info('Starting...')
	c = Controller(debug=DEBUG)
	c.run()