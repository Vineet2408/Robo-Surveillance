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

global server_socket
global FrameCounter
global frameList

def findPeople(features_arr, positions, thres = 0.6, percent_thres = 70):
	'''
	:param features_arr: a list of 128d Features of all faces on screen
	:param positions: a list of face position types of all faces on screen
	:param thres: distance threshold
	:return: person name and percentage
	'''
	f = open('./facerec_128D.txt','r')
	data_set = json.loads(f.read());
	returnRes = [];
	for i in range(len(features_arr)):
		features_128D=features_arr[i]
		result = "Unknown";
		smallest = sys.maxsize
		for person in data_set.keys():
			person_data = data_set[person][positions[i]];
			for data in person_data:
				distance = np.sqrt(np.sum(np.square(data-features_128D)))
				if(distance < smallest):
					smallest = distance;
					result = person;
		percentage =  min(100, 100 * thres / smallest)
		if percentage <= percent_thres :
			result = "Unknown"
		if(result == 'Unknown'):
			print()
		else:
			print('Neutralize')
		returnRes.append((result,percentage))
	return returnRes

def camera_recog(frame,frameList,FrameCounter,aligner,extract_feature,face_detect):
	FrameCounter=FrameCounter+1
	detect_time = time.time()

	rects, landmarks = face_detect.detect_face(frame,80);#min face size is set to 80x80
	aligns = []
	positions = []
	try:
		for (i) in range(len(rects)):
			rect= rects[i]
			#print('niche vala')
			aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
			if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
				aligns.append(aligned_face)
				positions.append(face_pos)
			else: 
				print("Align face failed") #log        
		if(len(aligns) > 0):
			features_arr = extract_feature.get_features(aligns)
			recog_data = findPeople(features_arr,positions)
			for (i) in range(len(rects)):
				rect= rects[i]
				cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(255,0,0)) #draw bounding box for the face
				cv2.putText(frame,recog_data[i][0]+" - "+str(recog_data[i][1])+"%",(rect[0],rect[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
		#cv2.imshow("Frame",frame)
		time.sleep(0.01)
		frameList.append(frame)
		return (frameList,FrameCounter,frame)
		
	except Exception as e:
		print(e)
		
def startRec():
	FrameCounter=0
	#parser = argparse.ArgumentParser()
	#parser.add_argument("--mode", type=str, help="Run camera recognition", default="camera")
	#args = parser.parse_args(sys.argv[1:]);
	FRGraph = FaceRecGraph();
	MTCNNGraph = FaceRecGraph();
	aligner = AlignCustom();
	extract_feature = FaceFeature(FRGraph)
	face_detect = MTCNNDetect(MTCNNGraph, scale_factor=1); #scale_factor, rescales image for faster detection		
	#mode = args.mode
	return (FrameCounter,aligner,extract_feature,face_detect)
