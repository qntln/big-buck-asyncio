# Convert

This it python 2.7 script used for converting video files to ascii encoded video files.

This script is using [img2txt](https://github.com/hit9/img2txt) for converting frames
of video to ascii art.

## Installation

First prepare make sure you have `avconv` installed. On ubuntu like systems you can install it using

```
sudo apt-get install libav-tools
```

Then install requirements:

```
pip install -r requirements.txt
```

## Usage

To convert video files use it using this command:

```
./convert.py <input file.avi> <output file.ascii>
```
