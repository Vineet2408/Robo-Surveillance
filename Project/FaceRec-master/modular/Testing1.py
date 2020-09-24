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
from FaceServerSocketV2 import *

def ma(socket):

	cdt=start(socket)
	
	

if __name__ == '__main__':
	socket=createSocket()
	
	mat=Thread(target=ma(socket))
	mat.start()
	mat.join()

