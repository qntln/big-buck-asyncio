# ASCII video player

This application is created for workshop on LinuxDays CZ 2016 about asyncio.

In this repository is converted [Big Buck Bunny](https://peach.blender.org/about/) video
to ASCII art frames. You can read more about this movie on their web site: https://peach.blender.org/about/

Also to create ASCII art video files the [img2txt](https://github.com/hit9/img2txt) was used for separated
frames. You can find more information in `./convert/README.md`.

This is implementation of simple player server implemented using asyncio. It can replay ASCII art video files
created using `./convert/` application.

It will start TCP server which can then be accessed using for example telnet.


You can find presentation to this workshop [here](https://qntln.github.io/big-buck-asyncio/#/)

## Prerequisites

This project require **python 3.5** installed. If you don't have python 3.5 but you have docker installed
then you can use `./bin/container.sh` wrapper which will run our application in python 3.5 image in docker.

There are no other special prerequisites.
 
## Install
 
To install all required packages use:

```
pip install -r requirements.txt
```

## Usage

To run server use this simple command:

```
./bin/main.py <video file>
```

Example:

```
./bin/main.py bigBuckBunny.ascii.bz2
```

Or if you don't have python 3.5 installed you can run our server in docker using this wrapper:

```
./bin/container.sh
```

It has no arguments and use file from above example to be replayed by default.

## Accessing server

To access server simple use telnet:

```
telnet localhost 8000
```
