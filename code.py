import sys
import subprocess
import os
import locale
import argparse
import multiprocessing

from datetime import datetime
from datetime import timedelta
from os import path
from types import SimpleNamespace

def reencode(f, args):
	start = datetime.now()

	if not path.exists(f):
		print("ERROR: file not found, skipping")
		return

	# Construct temp name for processing
	dirn, base = path.split(f)
	name, ext = path.splitext(base)
	newf = path.join(dirn, name + "_" + ext)

	# Run ffmpeg
	subprocess.run(["ffmpeg", 
		"-i", f, 
		"-c:v", "libx265",
		"-c:a", "copy", 
		"-ac", "2", 
		"-threads", args.threads, 
		"-hide_banner", 
		"-loglevel", args.loglevel,
		"-y", 
		newf
	])

	# Calculate the size difference
	oldsize = int(os.path.getsize(f) / 1024.0)
	newsize = int(os.path.getsize(newf) / 1024.0)
	delta = (oldsize - newsize) / oldsize * 100

	print('\nRe-encoded "{}"'.format(base))
	print("Reduced by {:.2f}%".format(delta))

	print(locale.format_string("\nOld Size: %12d KiB", oldsize, grouping=True))
	print(locale.format_string("New Size: %12d KiB", newsize, grouping=True))

	# Remove which ever is bigger
	if oldsize > newsize:
		os.remove(f)
		os.rename(newf, f)
		print("File replaced")
	else:
		os.remove(newf)
		print("File not replaced")

	# Print timing info
	end = datetime.now()
	end_time = end.strftime("%H:%M:%S")
	duration = (end-start)
	print("\nFinished at", end_time, "taking", duration, "\n")

parser = argparse.ArgumentParser(description='Wrap ffmpeg to encode files so I don\'t have to type as much.')

parser.add_argument('input', nargs='+', help='the input(s) given.')

parser.add_argument('-l', '--list', action='store_const', default=False, const=True, 
	help='Indicate the input is a list of files to process.')

parser.add_argument('-p', '--percentage', type=int, default=50, choices=range(0,101),
	metavar='0-100',
	help='(Sort of) the percentage of the cpu to use. Gets rounded to number of cores.')
parser.add_argument('-q', '--quiet', action='store_const',
	default=False, const=True,
	help='Hide the ffmpeg output.')
args = parser.parse_args()

# Normalise parameters to ffmpeg params
cpus = multiprocessing.cpu_count()
args.threads = str( int(args.percentage/100.0 * cpus) % (cpus + 1))
args.loglevel = "warning" if args.quiet else "info"

if args.list:
	with open(args.input[0], 'r') as filelist:
		for f in filelist:
			reencode(f.rstrip(), args)

else:
	for f in args.input:
		reencode(f, args)
	