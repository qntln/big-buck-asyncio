import asyncio
import bz2
import logging

import player.codec
import player.terminal


class Session:
	'''
	Session represent one client
	also separate sessions can replay different files
	'''

	def __init__(self, session_id: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, filename: str):
		self._logger = logging.getLogger('{}[{}]'.format(self.__class__.__name__, session_id))
		self.session_id = session_id
		self.filename = filename
		self._writer = writer
		self._reader = reader

		self._run_future = None # type: asyncio.Future


	async def run(self) -> None:
		'''
		Run loop which will stream frame by frame to writer
		'''
		self._logger.debug('Reading file = %s', self.filename)
		with bz2.BZ2File(self.filename, 'rb') as file:
			await self._clear_screen()

			metadata = player.codec.get_file_metadata(file)
			sleep_time = 1.0 / metadata.frame_rate

			for frame in player.codec.get_frames(file, metadata):
				# Move cursor to top left corner
				self._writer.write(player.terminal.RESET_CURSOR)
				self._writer.write(frame)
				await self._writer.drain()

				await asyncio.sleep(sleep_time)

			await self._clear_screen()


	async def _clear_screen(self) -> None:
		'''
		Write clearing of screen
		'''
		# First white all empty lines
		self._writer.write(player.terminal.CLEAR)
		# And then reset cursor to upper left
		self._writer.write(player.terminal.RESET_CURSOR)
		await self._writer.drain()
