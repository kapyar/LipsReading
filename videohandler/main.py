from video_module import VideoHandler
import cv2
import Tkinter as tk
from multiprocessing import Process
from utils import *

__version__ = "0.0.1"

'''
This class is responsiable for start the program

'''
class Main:


	def __init__(self):

		self.is_recording = False

	def start(self):
		if self.is_recording:
			is_recording = False
			print ("false")
		else:
			self.is_recording = True
			print ("true")

	def showVideo(self):
		print ("[INFO]: verion: {}".format(__version__))
		video = VideoHandler()

#show video from camera
		while(video.listenClose()):

			frame, lips = video.readMouthFromWeb() or (None, None)
			cv2.imshow("original", frame)

			if lips is not None:
				cv2.imshow("lips", lips)
				video.writeLips("lips", lips)

				# TODO need to find out how to detect if someone is speaking
				# video.showSplitChannels(lips)
				if is_speaking(lips):
					print ("[INFO]: speaking!")

		video.releaseResources()




if __name__ == '__main__':

	starter = Main()
	starter.showVideo()
	# print("frames #: {}".format(get_number_of_frames("../data/lips.avi")))

	path = "../data/lips.avi"
	# print (get_video_data("../data/lips.avi"))
	# cv2.imshow("3 frame",get_image_by_frame(path, 3))
	# video_to_frames(path , "../data/framed")
