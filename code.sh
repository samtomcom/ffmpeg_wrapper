
# Shell script to bulk process files within a directory
# ./code.sh 'path/to/directory'/*.ext
# where ext is the extensions of the files to process

for f in "$@"; do
	echo $f
	python /d/code/ffmpeg/code.py 4 "$f" q
done