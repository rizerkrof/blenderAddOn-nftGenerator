#!/usr/bin/env python3
from bpy.props import IntProperty, StringProperty
from bpy.types import PropertyGroup

class MetadataProperties(PropertyGroup):
	desiredIterations:IntProperty(name='Number of combinations',description='Desired number of combinations you want to generate',default=0,min=0)
	nameOfObjects:StringProperty(name='Name of NFTs')
	description:StringProperty(name='Description')
	image:StringProperty(name='Image URI base link')
	imageFormat:StringProperty(name='Image format')
	randomSeed:IntProperty(name='Random seed', description='The seed used to the random generation. Usefull to regenerate metadata', default=0, min=0 )
