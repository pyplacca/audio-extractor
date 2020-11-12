from moviepy.editor import VideoFileClip
import time
import sys
import os

'''
Audio Extractor 1.0.0

The last argument is considered to be the destination folder, and therefore can
accept several source files. ie. source1, source2, source..., destination.
If only two arguments are passed, it is assumed that both arguments are source
(contains source files) and destination folders respectively

Command line version
'''
# try:
_, *sources = sys.argv
# except ValueError:
# 	sources = folder = None

# if not sources and folder:
# 	sources, folder = [folder], None

def extract_and_save(file, save_at):
	video_file = VideoFileClip(file)
	# save audio
	audio = video_file.audio
	if audio:
		basename = f'{os.path.basename(file).rsplit(".", 1)[0]}.mp3'
		destination = os.path.join(save_at, basename)
		overwrite = True

		if os.path.exists(destination):
			# get user prompt if the file exists
			prompt = input(f'{basename!r} already exists in the destination'
				'folder.\nWould you like to overwrite this file? (y/n): ')
			overwrite = prompt.lower() == 'y'

		# overwrite existing file if user response is True
		if overwrite:
			audio.write_audiofile(destination)
		else:
			print('Overwrite canceled!')

		# clear garbage
		del video_file, audio
		return overwrite
	else:
		print(f'Sorry! A problem was encountered. '
			'Could not save audio from {file!r}')

def parse_files(directory):
	output = []
	for file in directory:
		if os.path.exists(file):
			if os.path.isfile(file):
				output += file,
			else:
				output += parse_files(map(
					lambda item: os.path.join(file, item),
					os.listdir(file)
				))
	return output

def create_destination(count):
	# create a destination folder
	current_time = time.strftime('%d.%m.%y', time.localtime())
	original = os.path.join(
		os.environ['USERPROFILE'],
		'Documents',
		'AudioExtractor'
	)

	if not os.path.exists(original):
		os.mkdir(original)

	if count > 1:
		import random
		return os.path.join(
			original,
			f'Extracts{current_time}.{random.randrange(101, 500)}'
		)
		del random

	del time

	return original


if sources:
	sources = parse_files(sources)

	print('\nFiles prepared for extraction;')

	for i, file in enumerate(sources, start=1):
		print(f'{i}. {os.path.basename(file)!r}')
	# print(f'Saving to {folder!r}')

	proceed = input('Would you like to proceed? (y/n): ').lower()
	if proceed == 'y':
		number_of_files = len(sources)
		folder = create_destination(number_of_files)

		# create directory if it doesn't exist
		if not os.path.exists(folder):
			os.mkdir(folder)

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
			f'file{["", "s"][extracted > 1]} extracted.')

		os.startfile(folder)

		# clear garbage
		del sources, folder
	# sys.exit()
