#!/usr/bin/env python3.5
# This is basic usage of streaming server
# it allows to stream one asci encoded video file to multiple clients
#
# It will automatically listen on 0.0.0.0 port 8000
# Usage:
#  ./main.py ./data/video.asci.bz2
#

# Update import path to parent directory be importable
import os, os.path, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))


import asyncio
import logging

import player.server


logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)


def main(input_file: str) -> None:
	server = player.server.PlayerServer('0.0.0.0', 8800, input_file)

	loop = asyncio.get_event_loop()
	loop.run_until_complete(server.start())

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		logger.warning('Interrupted')
	finally:
		logger.info('Exiting')
		loop.run_until_complete(server.stop())
		loop.stop()


if __name__ == '__main__':
	try:
		input_file = sys.argv[1]
	except IndexError:
		print('You have to provide file which will be replayed.', file=sys.stderr)
		exit(1)
	else:
		if os.path.exists(input_file):
			main(input_file)
		else:
			print('Replay file must exists', file=sys.stderr)
			exit(1)
