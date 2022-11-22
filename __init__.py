#!/usr/bin/env python3
import sys
sys.path.insert(0, sys.path[0]+'/')
import bpy
from bpy.props import PointerProperty, CollectionProperty
from .nftGeneratorAddOn import AddOnPanel, MetadataProperties, AttributesProperties, Analyze, Generate

bl_info = {
    "name": "NFT random generator",
    "description": "Generate assets combinations",
    "author": "Doudou",
    "version": (1, 0, 0),
    "blender": (3, 3, 1),
    "category": "Scene"
}

addOnClasses = AddOnPanel, MetadataProperties, AttributesProperties, Analyze, Generate

def register():
	from bpy.utils import register_class
	for addOnClass in addOnClasses:
		register_class(addOnClass)
	bpy.types.Scene.generatorSettings=PointerProperty(type=MetadataProperties)
	bpy.types.Scene.traitSettings=CollectionProperty(type=AttributesProperties)

def unregister():
	from bpy.utils import unregister_class
	for addOnClass in reversed(addOnClasses):
		unregister_class(addOnClass)
	del bpy.types.Scene.generatorSettings;
	del bpy.types.Scene.traitSettings

if __name__=='__main__':
	register()
