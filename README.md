# README #

Speaker's Corner Project

*** Note: There's going to be a lot of commits. I'm developing this via a very screwy wifi dongle.***


### Important Information ###

* Images are stored in images/
* The program looks for *.jpg
* Instruction text is loaded from images/inst.txt
* Images are resized to fit within the screen.
* NOTE: Will not change aspect ratio! To avoid grey borders, ensure that aspect ratio of image is the same as screen.
* Do not put too many images in place, or they won't center properly.
* Video recordings go in rec/
* Video recordings are given a timestamp in filename


### Setup ###

* Put in ~/speakers-corner
* Copy init.d/speaker_corner to /etc/init.d/

### Dependencies ###

system:
- ffmpeg

python:
- RPIGPIO
- Pillow (modern fill for PIL)
- max7219 (for led matrix)

binaries
- picam

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)


### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions


### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines


### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
