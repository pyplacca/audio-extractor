from moviepy.editor import VideoFileClip
from utils import extensions
from pathlib import Path
import subprocess
import sys
import os
import re

'''
Audio Extractor 1.0.0
Command line version

The last argument is considered to be the destination folder, and therefore can
accept several source files. ie. source1, source2, source..., destination.
If more than one argument is passed, the last is assumed to be the destination folder.
To override this behaviour, include --use-default to use the default destination as the destination folder

'''

_, *sources = sys.argv
OVERRIDE_DST = False

# identify destination folder
if '--use-default' not in sources and len(sources) > 1:
	OVERRIDE_DST = True
	specified_destination = Path(sources.pop())


def extract_and_save(file, save_at):
	video_file = VideoFileClip(file)
	# save audio
	audio = video_file.audio
	if audio:
		basename = f'{os.path.basename(file).rsplit(".", 1)[0]}.mp3'
		destination = save_at.joinpath(basename)
		overwrite = True

		if destination.exists():
			# get user prompt if the file exists
			prompt = input(
				f'{basename!r} already exists in the destination '
				'folder.\nWould you like to overwrite this file? (y/n): '
			)
			overwrite = prompt.lower() == 'y'

		# overwrite existing file if user response is True
		if overwrite:
			audio.write_audiofile(destination.as_posix())
		else:
			print('Overwrite canceled!')

		# clear garbage
		del video_file, audio
		return overwrite
	else:
		print(f'Sorry! A problem was encountered. '
			f'Could not extract audio from {file!r}')

def parse_files(directory, level=1):
	output = []
	for file in directory:
		if os.path.exists(file):
			if os.path.isfile(file):
				if is_video_file(file):
					output += file,
			else:
				if level == 1:
					output += parse_files(map(
						lambda item: os.path.join(file, item),
						os.listdir(file)
					), level+1)
	return output

def get_destination(count):
	import time
	# create a destination folder
	current_time = time.strftime('%d.%m.%y', time.localtime())
	destination = Path(os.path.join(
		os.environ['USERPROFILE'],
		'Documents',
		'AudioExtractor'
	))

	if OVERRIDE_DST:
		destination = specified_destination

	if count > 1:
		compiled = input(
			f"\nYou're about to save multiple files to {destination.as_posix()!r}"
			"\nWould you like to proceed (p) or create (c) a new folder?: "
		).lower()

		if compiled == 'c':
			dn = input('Please enter the folder name. You can press enter to skip (We will create one for you): ')
			import random
			destination = destination.joinpath(
				dn or \
				f'Extracts{current_time}.{random.randrange(101, 500)}'
			)
			del random

	del time

	return destination

def is_video_file(fp):
	_, ext = os.path.splitext(os.path.basename(fp))
	return ext.lower() in extensions['video']


if sources:
	sources = parse_files(sources)

	if sources:
		print('\nFiles prepared for extraction;')

		for i, file in enumerate(sources, start=1):
			print(f'{i}. {os.path.basename(file)!r}')

		number_of_files = len(sources)
		folder = get_destination(number_of_files)
		print(f'\nExtracting to {folder.as_posix()!r}')

		proceed = input('\nWould you like to proceed? (y/n): ').lower()
		if proceed == 'y':
			folder.mkdir(exist_ok=True, parents=True)
			# start extraction
			extracted = 0
			for n, src in enumerate(sources, start=1):
				print(f'Extracting {n} of {number_of_files}')

				# check if video file exits
				if not os.path.exists(src):
					# continue if it doesn't
					print(f'{src!r} does not exist.')
					continue

				# extract audio
				result = extract_and_save(src, folder)
				extracted += bool(result)

			print(f'Extraction complete! {extracted} '
				f'file{["s", ""][extracted == 1]} extracted.')

			# os.startfile(folder)
			if extracted:
				subprocess.run(f'explorer.exe /select, {folder.resolve()}')

			# clear garbage
			del sources, folder
		# sys.exit()
	else:
		print('This directory is not or contains no video files.')
