#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from PIL import Image, ImageDraw, ImageChops
import six
import imagehash
import face_recognition
from google_images_download import google_images_download

def getItem(item):
	arguments = {
					"keywords": item,
					"limit": 20,
				}
	response = google_images_download.googleimagesdownload()
	response.download(arguments)

def averageImage(item, hashfunc = imagehash.average_hash):
	import os
	item = str(item)
	userpath = "./downloads/" + item
	def is_image(filename):
		f = filename.lower()
		return f.endswith(".png") or f.endswith(".jpg") or \
			f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif") or '.jpg' in f
	
	image_filenames = []
	image_filenames += [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
	images = {}
	for img in sorted(image_filenames):
		try:
			hash = hashfunc(Image.open(img).convert('RGBA'))
		except Exception as e:
			print('Problem:', e, 'with', img)
		if hash in images:
			print(img, '  already exists as', ' '.join(images[hash]))
			if 'dupPictures' in img:
				print('rm -v', img)
		images[hash] = images.get(hash, []) + [img]
	values = {}
	for k in images.keys():
		values[int(str(k), 16)] = images[k][0]
	average = sum(list(values.keys())) / len(values)
	return values[min(values, key=lambda x:abs(x-average))]

def findFace(image):
	unknown_image = face_recognition.load_image_file(image)
	return face_recognition.face_locations(unknown_image)[0]

def clear(dir):
	import shutil
	shutil.rmtree('./downloads/' + dir, ignore_errors = True)
	

def yourFace(face, location, item):
	face = Image.open(face).convert('RGBA')
	item = Image.open(item).convert('RGBA')
	height = abs(location[0] - location[2])
	width = abs(location[1] - location[3])
	box = (location[3], location[0], location[1], location[2])
	print(height, width, box)

	face.paste(item.resize((width, height)), box)
	face.show()
	return face

def main():
	import sys, os
	face = sys.argv[1] if len(sys.argv) > 1 else quit()
	itemstr = sys.argv[2] if len(sys.argv) > 2 else quit()

	getItem(itemstr)
	item = averageImage(itemstr)
	face_location = findFace(face)
	new_face = yourFace(face, face_location, item)
	clear(itemstr)

if __name__ == "__main__":
	main()
