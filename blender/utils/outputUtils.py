#!/usr/bin/env python3
import bpy
import json
import os

def createJsonFile(nameOfFile, path, data):
	with open(bpy.path.abspath('//')+path+nameOfFile+'.json','w') as f:
		json.dump(data, f, indent=4)

def createDirectory(dirName):
	if not os.path.exists(bpy.path.abspath('//')+dirName):
		os.mkdir(bpy.path.abspath('//')+dirName)
