import asyncio
import contextlib
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
		self._logger.info('Server stopping')

		self._server.close()
		await self._server.wait_closed()

		# Because dict cannot be changed during iteration
		# we have to convert keys to list
		for session_id in list(self._sessions.keys()):
			self._logger.info('Terminating session = %s', session_id)
			await self._killSession(session_id)


	async def _killSession(self, session_id: str) -> None:
		'''
		Kill session and free it's resources
		'''
		try:
			session = self._sessions[session_id]
		except KeyError:
			# Session was already killed
			pass
		else:
			await session.terminate()

			# The session could be removed during termination
			with contextlib.suppress(KeyError):
				del self._sessions[session_id]


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
		finally:
			await self._killSession(session_id)
			self._logger.info('Session = %s was closed from = %s', session_id, ip_address)
