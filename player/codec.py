from typing import NamedTuple, Iterator, Iterable


Metadata = NamedTuple('Metadata', [
	('frame_rate', int),
	('frames_count', int),
	('line_length', int),
	('frame_height', int),
])


def _parse_header(data: bytes) -> Metadata:
	'''
	Parse line which contains header to object representation
	Headeline looks following:
		'+<frame rate>#<number of frames>#<line length>#<frame height>;'
	all numbers are fixed length of 10 digits
	'''
	# First convert it from bytes
	data = data.decode()
	assert data[0] == '+' and data[-1] == ';', 'Wrong metadata header'
	return Metadata(*[int(field) for field in data[1:-1].split('#')])


def _is_header_line(data: bytes) -> bool:
	'''
	Check whether data looks like metadata line
	'''
	return data.startswith(b'+') and data.endswith(b';') and b'#' in data


def get_file_metadata(file) -> Metadata:
	'''
	Read metadata from file created with convert
	this call will update file handler position right after the metadata
	'''
	metadata = _parse_header(file.read(45))
	assert file.read(1) == b'\n', 'We should have finish reading line with metadata'
	return metadata


def get_frames(stream: Iterable[bytes], metadata: Metadata) -> Iterator[bytes]:
	frame = []
	for line_number, line in enumerate(stream):
		# Skip line with metadata
		if _is_header_line(line):
			continue

		if line_number % (metadata.frame_height + 1) == 0 and line_number > 0:
			yield b''.join(frame)
			frame.clear()
			continue

		frame.append(line)
