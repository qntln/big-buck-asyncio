import asyncio
import logging


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


	async def run(self) -> None:
		'''
		Wrapper which allow us to terminate session object
		'''
		pass


	async def terminate(self) -> None:
		'''
		Close writer and clenaup after session
		'''
		pass
