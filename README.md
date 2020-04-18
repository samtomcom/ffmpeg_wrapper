# FFMPEG Wrapper

Wrap a simple ffmpeg command to re-encode file to H.X265, and dual channel audio.
Created to improve my experience re-encoding my collection of films.

# Requirements

* Python 3.3+
* ffmpeg 

ffmpeg needs to be installed, and added to the system path so that the script can call it.

# Usage

```
usage: code.py [-h] [-t {in,multi,file}] [-p 0-100] [-q] input [input ...]

Wrap ffmpeg to encode files so I don't have to type as much

positional arguments:
  input                 the input(s) given.

optional arguments:
  -h, --help            show this help message and exit
  -t {in,multi,file}, --type {in,multi,file}
                        The type of input, file is a single file, multi is a
                        list of files (using *), list is a file containing a
                        list of files to process
  -p 0-100, --percentage 0-100
                        (Sort of) the percentage of the cpu to use. Gets
                        rounded to number of cores
  -q, --quiet           Hide the ffmpeg output
```

I would reccomend adding the script to the path / an alias so that it can be called from anyway easily.
Here, `ffmpeg_wrap` is the alias I have to `python /path/to/the/script/code.py`

Files can be given by absolute or relative paths.

## All types

    ffmpeg_wrap INPUT [-t type] [-q] [-p 0-100]
	
use `-q` to hide the ffmpeg output

use `-p 0-100`, to denote the percentage of CPU to use, roughly

## Regular input

    ffmpeg_wrap file.mp4
	ffmpeg_wrap -t in file.mp4

The `input` paramter should be a single file to be processed.

## Multiple inputs

    ffmpeg_wrap -t multi file1.mp4 file2.mp4 file3.mp4 
    ffmpeg_wrap -t multi *.mp4

With `-t multi`, the `input` parameter should be a list of files.

You can the * operator, or list each file.

## File input

    ffmpeg_wrap -t file files.txt
	
The `input` parameter should be a file that has a name of a file to
encode on each line, e.g.

    files.txt
	---------
	file1.mp4
	file2.mp4
	file3.mp4



