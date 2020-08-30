import ctypes
import sys
import subprocess
import os
import argparse
import multiprocessing

from datetime import datetime
from datetime import timedelta
from os import path
from types import SimpleNamespace

def reencode(f, args):
	"""Re-encode a file with given arguments"""
	start = datetime.now()

	if not path.exists(f):
		print("ERROR: file not found, skipping")
		return

	# Deconstruct old filename to create the new one
	directory, name = path.split(f)
	basename, ext = path.splitext(name)
	# Replace extension if specified
	file_new = path.join(directory, basename + "_." + (ext if not args.extension else args.extension) )
	
	ctypes.windll.kernel32.SetConsoleTitleW("Re-encoding " + name)

	ffmpeg(f, args,
		["-c:v", "libx265", "-ac", "2"],
		file_new
	)

	# Calculate the size difference
	size_old = get_size(f)
	size_new = get_size(file_new)
	size_delta = (size_old - size_new) / size_old * 100

	print('\nRe-encoded "{}"'.format(basename))
	print("Reduced by {:.2f}% ({} -> {} KiB)".format(size_delta, size_old, size_new))

	# Remove un-encoded file
	os.remove(f)
	os.rename(file_new, f)

	# Print timing info
	end = datetime.now()
	print("\nFinished at", end.strftime("%H:%M:%S"), "taking", (end-start), "\n")

def ffmpeg(file_in, args, params, file_out):
	"""Run the actual ffmpeg process"""
	subprocess.run(["ffmpeg", 
		"-i", file_in,
		"-y", 
		"-threads", args.threads, 
		"-hide_banner", 
		"-loglevel", args.loglevel]
		+params
		+[file_out]
	)

def get_size(file):
	"""Calculate a file size in KiB"""
	return int(os.path.getsize(file) / 1024.0)

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Wrap ffmpeg to encode files so I don\'t have to type as much.')

	parser.add_argument('input', nargs='+', help='the input(s) given.')

	parser.add_argument('-e', '--extension', nargs=1, default=None, metavar='EXT',
		help='Optionally change the file type(s).')

	parser.add_argument('-l', '--list', action='store_const', default=False, const=True, 
		help='Indicate the input is a list of files to process.')

	parser.add_argument('-q', '--quiet', action='store_const',
		default=False, const=True,
		help='Hide the ffmpeg output.')
	parser.add_argument('-t', '--threads', type=int, default=4, metavar='N',
		help='Number of CPU threads to use. Default is 4.')

	args = parser.parse_args()

	# Normalise loglevel parameter
	args.loglevel = "warning" if args.quiet else "info"

	if args.list:
		with open(args.input[0], 'r') as filelist:
			for f in filelist:
				reencode(f.rstrip(), args)

	else:
		for f in args.input:
			reencode(f, args)
		
