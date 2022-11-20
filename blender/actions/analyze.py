#!/usr/bin/env python3
import bpy
from ..utils.blenderUtils import isAttributeCollection

class Analyze(bpy.types.Operator):
	bl_idname='wm.analyze_operator'
	bl_label='Analyze scene'
	hardTree='exportOption'
	def execute(self, context):
		print('Started analazing...')
		context.scene.traitSettings.clear()
		self.filteredAttributes = list(filter(isAttributeCollection, bpy.data.collections.keys()))
		maxIterations=1
		for attribute in self.filteredAttributes:
			maxIterations=maxIterations*len(bpy.data.collections[attribute].children.keys())
			for attributeValue in bpy.data.collections[attribute].children.keys():
				context.scene.traitSettings.add().name=attributeValue
				context.scene.traitSettings.add().rarity=50

		context.scene.generatorSettings.maxIterations=maxIterations if maxIterations!=1 else 0
		context.scene.generatorSettings.desiredIterations=maxIterations if maxIterations!=1 else 0
		print('Analazing done!')
		return{'FINISHED'}
