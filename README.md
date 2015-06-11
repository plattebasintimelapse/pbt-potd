# Photo of the Day

A photo of the day site that leverages the daily timelapse imagery of the Platte Basin Timelapse project

### What the Hell Does This Do?

Not much. But you can resize images and then create a timelapse video of those iamges. It makes an MP4, OGG, and WebM, all HTML5 ready videos!

### Getting Started

Before you get started, you need a set of PBT timelapse images in a folder at `images/originals`. You should also create `images/resized` for the resized images that are created.

### What You'll See

At least at this point...

	Greetings!
	I'll help you make some timelapse videos!
	First, you'll need to resize your images. And then you can use those images to create a video.

	Do you need to resize images? [y/N] 
	y

	What camera do you want to resize images for?
	Enter a directory: 002

	Resizing Images:
	_0021061.JPG -> 002_1061.jpg
	_0021062.JPG -> 002_1062.jpg
	_0021063.JPG -> 002_1063.jpg
	...
	_0021115.JPG -> 002_1115.jpg
	_0021116.JPG -> 002_1116.jpg
	_0021117.JPG -> 002_1117.jpg

	-------------------------------------------------
	57 images were resized successfully into images/resized/002/
	-------------------------------------------------

	Do you need to resize images? [y/N] 
	n
	Do you want to create a timelapse video? [y/N] 
	y

	-------------------------------------------------

	What camera do you want to create a timelapse for?
	Enter a directory: 002
	Output Folder: final

	ffmpeg version 2.6.2 Copyright (c) 2000-2015 the FFmpeg developers
	...
	...
	...

	Complete!
	Your videos are located in video/final


	Do you want to delete the resized images located in images/resized/002/? [y/N] 
	n
	Do you want to create a timelapse video? [y/N] 
	n

	-------------------------------------------------

	END

### Usage

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

* Automatically pull in images from Dropbox, hourly
* Send resized images to AWS for serveing
* Cron job to create timelapses nightly
* Cron job to create weekly timelapses nightly
* Delete resized images, locally, only after used in weekly timelapse
* Send videos to AWS for serving
* A bunch of other things, I have no idea what the hell I'm doing
