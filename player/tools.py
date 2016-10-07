import time


class StopWatch:
	'''
	Measure time in given block in seconds with microseconds precision
	Measured time can be accessed using `time` attribute
	'''

	def __init__(self):
		self._start = time.monotonic()
		self.time = 0.0 # type: float


	def lap(self) -> float:
		'''
		Return time in seconds from last lap
		'''
		lap = time.monotonic() - self._start
		self._start = time.monotonic()
		return max(0, lap)


	def __enter__(self):
		self._start = time.monotonic()


	def __exit__(self, exc_type, exc_val, exc_tb):
		self.time = time.monotonic() - self._start
