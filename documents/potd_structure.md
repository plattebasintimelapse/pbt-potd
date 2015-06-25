#POTD Structure#

We need to support a camera location, a camera location today, a camera location yesterday, a camera location last week and a camera location deep time view. To accomplish that, we will need a data structure to support it. That data structure could look like this:

###Camera###

* Camera name
* Camera slug (URL friendly version of the name, i.e. rowe-sanctuary)
* Camera location X (latitude)
* Camera location Y (longitude)
* Camera location Description
* Camera location inception date


###Picture###

* Camera (foreign key link to Camera)
* Photo (file link, stored on S3)
* Photo Date/Time

Do we want the EXIF data for the gear heads? Aperture, Shutter Speed etc.

###TimeLapse###

* Camera (foreign key link to Camera)
* File (file link, stored on S3)
* Lapse Date/Time

###DeepTime###

Not certain what we intend to do here. Is this a curated set of images for this camera location? If so, it would look like this:

* Camera (fk to Camera)
* Picture (many to many link to Picture)

That's it. Really. It's pick a camera, pick some pictures. 