# FFMPEG Wrapper

Wrap a simple ffmpeg command to re-encode file to H.X265, and dual channel audio.
Created to improve my experience re-encoding my collection of films.

# Requirements

* Python 3.6+
* ffmpeg 

ffmpeg needs to be installed, and added to the system path so that the script can call it.

## Installation

    $ git clone https://github.com/samtomcom/ffmpeg_wrapper.git
    $ cd ffmpeg_wrapper/
    $ sudo chmod +x ffmpeg_wrapper.py

Then add the script to your path, or set an alias so it can be called from any directory.

# Usage

```
usage: ffmpeg_wrapper.py [-h] [-e EXT] [-i IGN] [-l] [-q] [-t N]
                         input [input ...]

Wrap ffmpeg to encode files so I don't have to type as much.

positional arguments:
  input                 the input(s) given.

optional arguments:
  -h, --help            show this help message and exit
  -e EXT, --extension EXT
                        Optionally change the file type(s).
  -i IGN, --ignore IGN  Ignore the provided file types. Default
                        txt,srt,idx,sub
  -l, --list            Indicate the input is a list of files to process.
  -q, --quiet           Hide the ffmpeg output.
  -t N, --threads N     Number of CPU threads to use. Default is 4.
```

Files can be given by absolute or relative paths.

use `-e EXT` to provide a comma seperated list of acceptable output
file types for the re-encoded videos (default is 'mkv,mp4').
Any file encountered that is not one of the accepted types will be 
converted to the first given type.

`-i IGN` is used similarly, but to ignore any files that have 
one of the given file types (default: txt,srt,idx,sub). For use
with * file inputs where the files aren't explicitly named.

use `-t N`, to denote the number of CPU threads to use.  
(Kind of, ffmpeg will actually convert this to a percentage of CPU usage)  
e.g. N=4 when you have 8 threads will use ALL of your threads at 50% usage.

### Regular input

    ffmpeg_wrapper.py file.mp4
    ffmpeg_wrapper.py file1.mp4 file2.mkv file3.mp4
    ffmpeg_wrapper.py *.mp4
    ffmpeg_wrapper.py * 

The input is a file, or a list of files to be encoded.

### File list input

    ffmpeg_wrapper.py --list files.txt
	  ffmpeg_wrapper.py -l files.txt
	
The `input` parameter should be a file that has a name of a file to
encode on each line, e.g.

    files.txt
	  ---------
	  file1.mp4
	  file2.mp4
	  file3.mp4



