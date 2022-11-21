#!/usr/bin/env python3
from bpy.props import IntProperty
from bpy.types import PropertyGroup

class AttributesProperties(PropertyGroup):
	rarity:IntProperty(name='Rarity', description='The higher the number the more rare it is', default=0, min=0, max=99)
