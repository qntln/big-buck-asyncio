# Convert

This is a Python 2.7 script that converts _real_ video files to ASCII-encoded video files.

This uses [img2txt](https://github.com/hit9/img2txt) to convert single video frames to ASCII art.

## Installation

First make sure that you have `avconv` installed. On Ubuntu-like systems you can install with

```
sudo apt-get install libav-tools
```

Then install requirements:

```
pip install -r requirements.txt
```

## Usage

```
./convert.py <input file.avi> <output file.ascii>
```
