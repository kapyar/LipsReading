import cv2
import os
import numpy as np

def is_speaking(frame):

	height, width, channels = frame.shape
	sum = 0

	for i in range(0,height):
		gray = 0
		for j in range(0, width):
			gray += frame[i, j]
		sum += gray/3


	# print(sum)
	if (sum.any()) > 200:
		return True
	else:
		return False



def get_video_data(path):

	frames_count = -1
	fps = -1
	width = -1
	height = -1

	cap = cv2.VideoCapture(path)

	if cap:
		frames_count = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
		width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
		height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
		fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

	return width, height, frames_count, fps


def get_image_by_frame(path, index=None):
	cap = cv2.VideoCapture(path)
	cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, index)

	if cap:
		success,frame = cap.read()
		if(not success):
			print("[INFO] no frame #: {}".format(index))
		return frame
	else:
		print("[INFO] no frame #: {}".format(index))


def video_to_frames(video, path_output_dir):

	width,height,frames,fps = get_video_data(video)

	vidcap = cv2.VideoCapture(video)
	count = 0

	# create np array to glue frames
	vis = None
	count = int()
	while vidcap.isOpened():
		success, image = vidcap.read()

		if success:
			if vis is None:
				vis = image
			else:
				vis = np.concatenate((vis, image), axis=1)
				count = count + 1
				print("[INFO] : concantenate {} ".format(count))
				assert (count<=frames)
		else:
			break

	cv2.imwrite('out.png', vis)
	cv2.destroyAllWindows()
	vidcap.release()