import asyncio
import logging

import player.session
import uuid


class PlayerServer:
	'''
	Asyncio server which will create session object for each new client
	'''

	def __init__(self, host: str, port: int, filename):
		self._logger = logging.getLogger(self.__class__.__name__)
		self.host = host
		self.port = port
		self.filename = filename

		self._server = None # type: asyncio.Server
		self._sessions = {}


	async def start(self) -> None:
		'''
		Start socket server which will stream movie
		'''
		self._logger.info('Server starting at = %s:%d', self.host, self.port)
		self._server = await asyncio.start_server(self._handle_client, self.host, self.port)


	async def stop(self) -> None:
		'''
		Stop server and all sessions
		'''
		pass


	async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
		'''
		Handle new client and create session for it
		'''
		ip_address = writer.get_extra_info('peername')
		session_id = uuid.uuid1().hex
		session = player.session.Session(session_id, reader, writer, self.filename)

		self._logger.info('New session = %s is created, from = %s', session_id, ip_address)
		self._sessions[session_id] = session

		try:
			await session.run()
		except (ConnectionResetError, BrokenPipeError,):
			pass
