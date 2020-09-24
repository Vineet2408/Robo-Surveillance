import socket
import pickle
import tensorflow as tf
import argparse
import sys
import socket
import os
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import json
import time
from threading import *
import colorsys
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2

import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input

from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import image_preporcess

import multiprocessing
from multiprocessing import Pipe
import mss
import time
from threading import *

global server_socket
global FrameCounter
global frameList


def createSocket():
	global server_socket
	global FrameCounter
	FrameCounter=0
	global frameList
	frameList=[]
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print('Socket created')

	server_socket.bind(('',9000))
	print('Socket bind complete')
	server_socket.listen(10)
	print('Socket now listening')

	

class YOLO(object):
	_defaults = {
		#"model_path": 'logs/ep050-loss21.173-val_loss19.575.h5',
		"model_path": 'logs/trained_weights_final.h5',
		"anchors_path": 'model_data/yolo_anchors.txt',
		"classes_path": '1_CLASS_test_classes.txt',
		"score" : 0.3,
		"iou" : 0.45,
		"model_image_size" : (416, 416),
		"text_size" : 3,
	}

	@classmethod
	def get_defaults(cls, n):
		if n in cls._defaults:
			return cls._defaults[n]
		else:
			return "Unrecognized attribute name '" + n + "'"

	def __init__(self, **kwargs):
		self.__dict__.update(self._defaults) # set up default values
		self.__dict__.update(kwargs) # and update with user overrides
		self.class_names = self._get_class()
		self.anchors = self._get_anchors()
		self.sess = K.get_session()
		self.boxes, self.scores, self.classes = self.generate()

	def _get_class(self):
		classes_path = os.path.expanduser(self.classes_path)
		with open(classes_path) as f:
			class_names = f.readlines()
		class_names = [c.strip() for c in class_names]
		return class_names

	def _get_anchors(self):
		anchors_path = os.path.expanduser(self.anchors_path)
		with open(anchors_path) as f:
			anchors = f.readline()
		anchors = [float(x) for x in anchors.split(',')]
		return np.array(anchors).reshape(-1, 2)

	def generate(self):
		model_path = os.path.expanduser(self.model_path)
		assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

		# Load model, or construct model and load weights.
		num_anchors = len(self.anchors)
		num_classes = len(self.class_names)
		is_tiny_version = num_anchors==6 # default setting
		try:
			self.yolo_model = load_model(model_path, compile=False)
		except:
			self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
				if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
			self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
		else:
			assert self.yolo_model.layers[-1].output_shape[-1] == \
				num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
				'Mismatch between model and given anchor and class sizes'

		print('{} model, anchors, and classes loaded.'.format(model_path))

		# Generate colors for drawing bounding boxes.
		hsv_tuples = [(x / len(self.class_names), 1., 1.)
					  for x in range(len(self.class_names))]
		self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
		self.colors = list(
			map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
				self.colors))

		np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.

		# Generate output tensor targets for filtered bounding boxes.
		self.input_image_shape = K.placeholder(shape=(2, ))
		boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
				len(self.class_names), self.input_image_shape,
				score_threshold=self.score, iou_threshold=self.iou)
		return boxes, scores, classes

	def detect_image(self, image):
		global frameList
		global FrameCounter
		if self.model_image_size != (None, None):
			assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
			assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
			boxed_image = image_preporcess(np.copy(image), tuple(reversed(self.model_image_size)))
			image_data = boxed_image

		out_boxes, out_scores, out_classes = self.sess.run(
			[self.boxes, self.scores, self.classes],
			feed_dict={
				self.yolo_model.input: image_data,
				self.input_image_shape: [image.shape[0], image.shape[1]],#[image.size[1], image.size[0]],
				K.learning_phase(): 0
			})

		#print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

		thickness = (image.shape[0] + image.shape[1]) // 600
		fontScale=1
		ObjectsList = []
		Mylst=[]
		for i in range(0,len(out_classes)):
			Mylst.append((i,out_classes[i]))

		for i, c in reversed(Mylst):
			predicted_class = self.class_names[c]
			box = out_boxes[i]
			score = out_scores[i]

			label = '{} {:.2f}'.format(predicted_class, score)
			#label = '{}'.format(predicted_class)
			scores = '{:.2f}'.format(score)

			top, left, bottom, right = box
			top = max(0, np.floor(top + 0.5).astype('int32'))
			left = max(0, np.floor(left + 0.5).astype('int32'))
			bottom = min(image.shape[0], np.floor(bottom + 0.5).astype('int32'))
			right = min(image.shape[1], np.floor(right + 0.5).astype('int32'))

			mid_h = (bottom-top)/2+top
			mid_v = (right-left)/2+left

			# put object rectangle
			cv2.rectangle(image, (left, top), (right, bottom), self.colors[c], thickness)

			# get text size
			(test_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, thickness/self.text_size, 1)

			# put text rectangle
			cv2.rectangle(image, (left, top), (left + test_width, top - text_height - baseline), self.colors[c], thickness=cv2.FILLED)

			# put text above rectangle
			cv2.putText(image, label, (left, top-2), cv2.FONT_HERSHEY_SIMPLEX, thickness/self.text_size, (0, 0, 0), 1)

			# add everything to list
			ObjectsList.append([top, left, bottom, right, mid_v, mid_h, label, scores])
		cv2.imshow('Frame',image)
		frameList.append(image)
		FrameCounter+=1
		return image, ObjectsList

	def close_session(self):
		self.sess.close()

	def detect_img(self, image):
		image = cv2.imread(image, cv2.IMREAD_COLOR)
		original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		original_image_color = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

		r_image, ObjectsList = self.detect_image(original_image_color)
		return r_image, ObjectsList

def recvPiFrame():
		global frameList
		global conn
		global frame

		global server_socket
		conn,add1= server_socket.accept()

		print("conection has been established | ip "+add1[0]+" port "+str(add1[1]))

		print("recieving")
		yolo = YOLO()
		i=0
		data = b""
		payload_size = struct.calcsize(">L")
		print("payload_size: {}".format(payload_size))
		while True:
			time.sleep(0.01)
			while len(data) < payload_size:
				print("Recv: {}".format(len(data)))
				data += conn.recv(4096)

			print("Done Recv: {}".format(len(data)))
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack(">L", packed_msg_size)[0]
			print("msg_size: {}".format(msg_size))
			while len(data) < msg_size:
				data += conn.recv(4096)
			frame_data = data[:msg_size]	
			data = data[msg_size:]

			frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
			#img = p_output.recv()
			img=frame
			#Grab screen image
			#img = np.array(sct.grab(monitor))

			# Put image from pipe
			

			 #cv2.imshow('ffff',frame)
			#frame=cv2.resize(frame,(416,416))
			yolo.detect_image(frame)
			#camera_recog(frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break
		


def sendVideoFrame():
	global server_socket
	global	conn2
	global FrameCounter
	global add2
	conn2,add2= server_socket.accept()
	
	print("conection has been established | ip "+add2[0]+" port "+str(add2[1]))
	
	img_counter = 0
	time.sleep(0.01)
	pr=conn2.recv(1024)
	
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	print('sending')
	
	while True:
		time.sleep(0.02)
		
		if FrameCounter > 5:
			frame =frameList[FrameCounter-2]
			cv2.imshow("Frame",frame)
			#cv2.imshow('fcontroller',frame)
			result, frame = cv2.imencode('.jpg', frame, encode_param)
			#data = zlib.compress(pickle.dumps(frame, 0))
			data = pickle.dumps(frame, 0)
			size = len(data)

			print("frames:","{}: {}".format(img_counter, size))
			#frame=cv2.resize(frame,(680,420))
			conn2.send(frame)
			time.sleep(0.07)
			
			
			img_counter += 1
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			

	cam.release()
	
def RecvCommand():
	
	while True:	
		global conn2
		global add2
		pr=conn2.recv(1024)
		print('recThread')
		print('pr = ',pr)
		time.sleep(0.02)

if __name__ == '__main__':
	
	
	
	createSocket()
	
	RecPiFrameThread=Thread(target=recvPiFrame)			
	RecPiFrameThread.start()
		
	FrameSenderThread=sendVideoFrame()
	cmdRecThread=RecvCommand()

	global FrameCounter
	if FrameCounter >4:
		FrameSenderThread.start()
		cmdRecThread.start()
		
	RecPiFrameThread.join()
	FrameSenderThread.join()
	cmdRecThread.join()
	
