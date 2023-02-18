Developed in PopOS, requires syft to be installedd
Usage: python diff.py --first-image image1 --second-image image2
image1 and image2 are docker images already installed/pulled locally.
The script will find common packages, packages with different versions, as well as packages unique to each image. The common packages will not be printed, every other package will be.
