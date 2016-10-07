#!/usr/bin/env python2
#
# WARNING: make sure you have enough space on your drive
#          this script will create temporary frame representation of video being coded
#          for a 1280x720@25 10 minutes length video it creates a 17GB of frames!
#
# This script is used to convert video files
# to compressed asci files which contains all frames at 25 frames per seconds
#
# These files have maximum length of 75 characters per line.
#
# To run this script you will need python2.7 environment with `requirements.txt` installed.
# Also this script uses `avconv` from libav-tools package by default to extract frames
#
# Then to convert video file to asciart the [img2txt.py](https://github.com/hit9/img2txt) script is used.
#
# Usage:
#	./convert.py <input file> <output file>
#

from __future__ import print_function

import sys
import glob
import time
import os.path
import tempfile
import subprocess


# Default extract command to get separated frames from input video file
# This requires three arguments filename, frame rate, temp directory where to store frames
EXTRACT_COMMAND = 'avconv -i "{:s}" -r {:d} -vsync 1 "{:s}/frame_%10d.png"'

# Command for converting image frame to asci characters
CONVERT_COMMAND = 'img2txt.py "{:s}" --ansi --maxLen {:d} --targetAspect 0.5'

# How many convert processes would be spawned
NUMBER_OF_CONVERT_PROCESSES = 3

# Header format
# All values here are integers and has fixed size
# all numbers are 10 digits length
# Header: '+<frame rate>#<number of frames>#<line length>#<frame height>;'
HEADER = '+{:010d}#{:010d}#{:010d}#{:010d};\n'


class UsageException(RuntimeError):
	''' Exception raised when wrong usage of this script '''


def _getFrameFiles(directory):
	'''
	Get list of absolute path to frame files

	:param directory: directory where to look for frames
	:return: List[str]
	'''
	files = list(glob.glob(os.path.join(directory, 'frame_*.png')))
	files.sort()
	return files


def _convertFrames(files, output_file, max_length):
	'''
	Convert bulk of files to asci and append to output file
	convert each file in separated process

	:param files: iterable of files which are sorted by frame number
	:param output_file: output file handler which will be appended
	:param max_length: line max length
	:return: number of lines (height) one frame has
	'''
	# TODO this would be better to implement with some
	# kind of pool but then this will be complicated because of order
	# so base implementation just spawn some process and then wait for the,
	processes = [
		(file, subprocess.Popen(
			CONVERT_COMMAND.format(file, max_length),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=True
		),)
		for file in files
	]

	for file, p in processes:
		stdout, stderr = p.communicate()
		if p.returncode != 0:
			raise RuntimeError(
				'Error during calling convert. {:s}'.format(stderr)
			)
		# Write file name of single frame for future debugging
		output_file.write((file + '\n').encode())
		output_file.write(stdout)

	return stdout.count('\n')


def convert(input_file, output_file, frame_rate = 25, max_length = 75):
	'''
	Convert input video file to asci compressed output file

	:param input_file: existing path to video file
	:param output_file: file which will be created or overridden
	:param frame_rate: what is framerate at which file should be replayed
	:param max_length: maximum length of single line in asci format
	:return: None
	'''
	temp_directory = tempfile.mkdtemp(prefix='convert')
	try:
		extract_process = subprocess.Popen(
			EXTRACT_COMMAND.format(input_file, frame_rate, temp_directory),
			shell=True
		)

		with open(output_file, 'wb') as output_file_handler:
			frame_height = 0
			number_of_frames = 0

			# Write empty metadata to begin of file. Those metadata will be overridden at finish
			output_file_handler.write(HEADER.format(
				frame_rate, number_of_frames, max_length, frame_height
			).encode())
			while True:
				files = _getFrameFiles(temp_directory)
				number_of_frames += len(files)

				# When we have no files but extract is still running
				# we sleep for a while and then loop again
				if not files and extract_process.poll() is None:
					time.sleep(0.5)
					continue

				# When extract process has ended and we have no more files we are done with converting
				if not files and extract_process.poll() is not None:
					break

				# convert bulk of files
				convert_files = [files.pop(0) for _ in range(min(NUMBER_OF_CONVERT_PROCESSES, len(files)))]
				frame_height = _convertFrames(
					convert_files,
					output_file_handler,
					max_length
				)

				# then remove already converted frames
				for f in convert_files:
					os.unlink(f)

			# once converting is done
			# we have to write the real header to the top of the file
			output_file_handler.seek(0)
			output_file_handler.write(HEADER.format(frame_rate, number_of_frames, max_length, frame_height).encode())

		# once we are done. Compress those files
		subprocess.check_call(('pbzip2', output_file,))
	finally:
		# Cleanup the temp directory
		subprocess.check_call(('rm', '-r', temp_directory,))


def main(argv):
	''' Gets arguments from argv and check if input files exists '''
	try:
		input_file, output_file = argv[1:3]
	except ValueError:
		raise UsageException('You have to provide input and output files.')
	else:
		if os.path.exists(input_file):
			convert(input_file, output_file)
		else:
			raise UsageException('Input file must exists.')


if __name__ == '__main__':
	USAGE = './convert.py <input file> <output file>'
	try:
		main(sys.argv)
	except UsageException as e:
		print('Wrong usage of script.\n'
			  'Usage: {:s}.\n\n'
			  'Error: {:s}'.format(USAGE, e), file=sys.stderr)
		exit()
