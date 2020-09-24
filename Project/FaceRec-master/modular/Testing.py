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
from FaceServerSocket import *

def ma(socket):
	while(True):

		rpf=Thread(target=recPiFrame(socket))
		svf=Thread(target=sendVideoFrame(socket))

		rpf.start()
		svf.start()

		rpf.join()
		svf.join()

	
	

if __name__ == '__main__':
	socket=createSocket()
	
	mat=Thread(target=ma(socket))
	mat.start()
	mat.join()

