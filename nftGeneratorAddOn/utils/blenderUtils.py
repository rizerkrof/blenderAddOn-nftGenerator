#!/usr/bin/env python3
import bpy

def isAttributeCollection(collectionName):
	return True if collectionName.split('_')[0]=='Attribute' else False

def getAttributeNameFromCollectionName(attributeString):
	return attributeString.split('_')[1]

def popup(message='',title='NFT generator', icon='INFO'):
	def execute(self, context):
		self.layout.label(text=message)
	bpy.context.window_manager.popup_menu(execute, title=title, icon=icon)
