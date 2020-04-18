import sys
import subprocess
import os
import locale

from datetime import datetime
from datetime import timedelta
from os import path

"""
Python script to process a file with ffmpeg, giving information afterwards

python code.py [N] '/path/to/file.ext' [q]
N = rough percentage of CPU to use, 4 to use 50% with 8 threads, 2 for 25%
  4 is the default if not passed
3rd argument is empty for verbose, anything else for quiet mode
"""

start = datetime.now()

if len(sys.argv) == 2: # 1 param = path
	f = path.normpath(sys.argv[1])
	threads = "4"
else: # more = threads, path, [q]
	threads = sys.argv[1]
	f = path.normpath(sys.argv[2])

if not path.exists(f):
	raise IOError('Given file does not exist')

dirn, base = path.split(f)
name, ext = path.splitext(base)

newf = path.join(dirn, name + "_" + ext)

loglevel = "info"
if len(sys.argv) == 4:
	loglevel = "warning"

subprocess.run(["ffmpeg", 
	"-i", f, 
	"-c:v", "libx265",
	"-c:a", "copy", 
	"-ac", "2", 
	"-threads", threads, 
	"-hide_banner", 
	"-loglevel", loglevel, 
	newf
])

oldsize = int(os.path.getsize(f) / 1024.0)
newsize = int(os.path.getsize(newf) / 1024.0)
delta = (oldsize-newsize)/oldsize*100

locale.setlocale(locale.LC_ALL, 'en_GB')

print('\nRe-encoded "{}"'.format(base))
print("Reduced by {:.2f}%".format(delta))

print(locale.format_string("\nOld Size: %12d KiB", oldsize, grouping=True))
print(locale.format_string("New Size: %12d KiB", newsize, grouping=True))

if oldsize > newsize:
	os.remove(f)
	os.rename(newf, f)
	print("File replaced")
else:
	os.remove(newf)
	print("File not replaced")

end = datetime.now()
end_time = end.strftime("%H:%M:%S")
duration = (end-start)
print("\nFinished at", end_time, "taking", duration, "\n")