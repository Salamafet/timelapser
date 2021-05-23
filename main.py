import cv2
import numpy as np
import glob
import os
from os import path
import time
import sys


def main():

	print(""" 
 _______           __                     
/_  __(_)_ _  ___ / /__ ____  ___ ___ ____
 / / / /  ' \/ -_) / _ `/ _ \(_-</ -_) __/
/_/ /_/_/_/_/\__/_/\_,_/ .__/___/\__/_/   
Alpha V0.5            /_/                 
""")

	try:
		sys.argv[1]
	except IndexError:
		print("You need to give a path for the JPG file.")
		print("Example: python main.py /Users/John/Photos")
		exit()

	liste_fichier = glob.glob('{}/*.JPG'.format(sys.argv[1]))
	liste_fichier = sorted(liste_fichier)

	if(len(liste_fichier) == 0):
		print("No JPG file found")
		if(input("Do you want include subfolder ? Y/N > ").lower() != "y"):
			exit()
		else:
			liste_fichier = glob.glob('{}/**/*.JPG'.format(sys.argv[1]), recursive=True)
			liste_fichier = sorted(liste_fichier)

	# Create the out folder if doesn't exist
	if(not path.exists("out")):
		os.mkdir("out")
	
	# Check if the timelapse file exist and generate new name
	if(path.exists('out/timelapse.mp4')):
		status = 1
		while True:
			if(not path.exists('out/timelapse{}.mp4'.format(status))):
				fichier_sortie = "out/timelapse{}.mp4".format(status)
				break
			else:
				status += 1
	else:
		fichier_sortie = "out/timelapse.mp4"

	# Get resolution of first image for the custom resolution
	for image in liste_fichier:
		img = cv2.imread(image)
		height, width, layers = img.shape
		size = (width, height)
		break

	print("Choose number of FPS: ")
	print("- 30 FPS ({})".format(time.strftime('%M:%S', time.gmtime(len(liste_fichier) / 30))))
	print("- 45 FPS ({})".format(time.strftime('%M:%S', time.gmtime(len(liste_fichier) / 45))))
	print("- 60 FPS ({})".format(time.strftime('%M:%S', time.gmtime(len(liste_fichier) / 60))))
	print("You can choose a custom frame rate")
	while True:
		fps = input("FPS > ")
		try:
			fps = int(fps)
		except ValueError:
			continue
		else:
			break

	resolution = None
	print("Choose video quality:")
	print("[1] - 480p DVD (720x480)")
	print("[2] - 720p HD Ready (1280x720)")
	print("[3] - 1080p Full HD (1920x1080)")
	print("[4] - 2160p UHDTV1 (3840x2160)")
	print("[5] - 4320p UHDTV2 (7680x4320)")
	print("[6] - [First photo resolution] ({}x{})".format(size[0], size[1]))
	while True:
		resolution = input("Number > ")
		try:
			resolution = int(resolution)
		except ValueError:
			continue
		else:
			if(resolution < 1 or resolution > 6):
				continue
			else:
				break

	if resolution == 1:
		print("480p DVD (720x480)")
		size = (720, 480)
	elif resolution == 2:
		print("720p HD Ready (1280x720)")
		size = (1280, 720)
	elif resolution == 3:
		print("1080p Full HD (1920x1080)")
		size = (1920, 1080)
	elif resolution == 4:
		print("2160p UHDTV1 (3840x2160)")
		size = (3840, 2160)
	elif resolution == 5:
		print("4320p UHDTV2 (7680x4320)")
		size = (7680, 4320)
	elif resolution == 6:
		print("[First photo resolution] ({}x{})".format(size[0], size[1]))

	out = cv2.VideoWriter(fichier_sortie, cv2.VideoWriter_fourcc(*'mp4v'), int(fps), size)

	status = 0
	for image in liste_fichier:
		status += 1
		pourcentage = "{:.2f}".format(status * 100 / len(liste_fichier))
		print("# [{}%] ({}/{} - {})".format(pourcentage, status, len(liste_fichier), image), end='\r')
		img = cv2.imread(image)
		frame = cv2.resize(img, size)
		out.write(frame)

	out.release()
	print("")
	print("Final file size: {:.2f} MB".format(os.stat(fichier_sortie).st_size / (1024 * 1024)))

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("")
		print('Aborted !')
		sys.exit(0)