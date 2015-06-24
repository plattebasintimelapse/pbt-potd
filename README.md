# Photo of the Day

A photo of the day site that leverages the daily timelapse imagery of the Platte Basin Timelapse project

### What the Hell Does This Do?

Not much. But you can resize images and then create a timelapse video of those iamges. It makes an MP4, OGG, and WebM, all HTML5 ready videos!

### Getting Started

Before you get started, you need a set of PBT timelapse images in a folder at `images/originals`. You should also create `images/resized` for the resized images that are created.

**Note:** You'll need ffmpeg installed on your machine. I just installed it with Homebrew. Unsure how this gets documented or put into system requirements.

	brew install ffmpeg

If you already have it installed, make sure to include the follow codecs in the build:

	brew reinstall ffmpeg --with-libvpx --with-theora 

I think there is a compilation guide for Raspberry Pi. Found [here](https://trac.ffmpeg.org/wiki/CompilationGuide/RaspberryPi).

Install virutalenv if you don't already have it:

	pip install virtualenv
  
Create a virtual Python environment:

  	virtualenv env
  
To begin using the virtual environment, it needs to be activated:

  	source env/bin/activate
  
Install the project requirements:

  	pip install -r requirements.txt
  
**Make some videos!**

### TODO

- [ ] Automatically pull in images from Dropbox, hourly
- [x] Send resized images to AWS for serveing
- [ ] Cron job to create timelapses nightly
- [ ] Cron job to create weekly timelapses nightly
- [ ] Delete resized images, locally, only after used in weekly timelapse
- [x] Send videos to AWS for serving
- [ ] A bunch of other things, I have no idea what the hell I'm doing
