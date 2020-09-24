import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import tensorflow as tf
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
import argparse
import sys
import json
import time
from threading import *
from FaceRecog import *
global server_socket
global FrameCounter
global frameList
global t
global noc


def add(a,b):
	c=a+b
	print(c)
	return c

def createSocket():
	global server_socket
	global FrameCounter
	global aligner
	global extract_feature
	global face_detect
	FrameCounter,aligner,extract_feature,face_detect=startRec()
	global noc
	FrameCounter=0
	noc=10
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print('Socket created')

	server_socket.bind(('',9000))
	print('Socket bind complete')
	server_socket.listen(noc)
	print('Socket now listening')
	return server_socket

def recPiFrame(server_socket):
	global frameList
	global aligner
	global extract_feature
	global face_detect
	global FrameCounter
	frameList=[]	
	print("waitng for pi")
	conn1,add1= server_socket.accept()
	print("conection has been established with pi| ip "+add1[0]+" port "+str(add1[1]))

	data = b""
	payload_size = struct.calcsize(">L")
	time.sleep(1)
	print("payload_size: {}".format(payload_size))
	while True:
		time.sleep(0.01)
		while len(data) < payload_size:
			data += conn1.recv(4096)
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack(">L", packed_msg_size)[0]
		while len(data) < msg_size:
			data += conn1.recv(4096)
		frame_data = data[:msg_size]
		data = data[msg_size:]
		frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
		frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
		frameList,FrameCounter,frame=camera_recog(frame,frameList,FrameCounter,aligner,extract_feature,face_detect)
		time.sleep(0.01)
		
		cv2.waitKey(1)


def sendVideoFrame(server_socket):
	global conn2
	global FrameCounter
	global frameList
	
	print("waiting for Android to connect")
	conn2,add2= server_socket.accept()
	
	print("conection has been established with android | ip "+add2[0]+" port "+str(add2[1]))
	time.sleep(0.020)
	time.sleep(1)
	img_counter = 0
	pr=conn2.recv(9)
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	print('sending')
	cmdRecThread=Thread(target=RecCommand)
	cmdRecThread.start()

	while True:
		
		if FrameCounter > 3:
			frame =frameList[FrameCounter-2]
			cv2.imshow('fcontroller'+str(len(frame)),frame)
			result, frame = cv2.imencode('.jpg', frame, encode_param)
			#data = zlib.compress(pickle.dumps(frame, 0))
			data = pickle.dumps(frame, 0)
			size = len(data)

			#print("frames:","{}: {}".format(img_counter, size))
			conn2.send(frame)
			time.sleep(0.06)
			
			img_counter += 1
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break				
	
def RecCommand():
	time.sleep(1)
	while True:	
		global conn2
		global add2
		pr=conn2.recv(10)
		time.sleep(0.050)
		print(pr)