#!/usr/bin/env python3
import bpy
from ..utils.blenderUtils import isAttributeCollection

class AddOnPanel(bpy.types.Panel):
	bl_label='NFT Generator'
	bl_idname='SCENE_PT_layout'
	bl_space_type='PROPERTIES'
	bl_region_type='WINDOW'
	bl_context='scene'
	def draw(self, context):
		count=0
		attributes = list(filter(isAttributeCollection, bpy.data.collections.keys()))
		for attribute in attributes:
			self.layout.label(text=attribute)
			for attributeValue in bpy.data.collections[attribute].children.keys():
				if count<len(context.scene.traitSettings):
					attributeRow = self.layout.row()
					attributeRow.label(text='- '+attributeValue)
					attributeRow.prop(context.scene.traitSettings[count],'rarity')
					count+=1
		separatorRow = self.layout.row()
		separatorRow.separator()
		self.layout.prop(context.scene.generatorSettings, 'nameOfObjects')
		self.layout.prop(context.scene.generatorSettings, 'description')
		self.layout.prop(context.scene.generatorSettings, 'image')
		self.layout.prop(context.scene.generatorSettings, 'imageFormat')
		self.layout.prop(context.scene.generatorSettings,'desiredIterations')
		analyzeButtonRow = self.layout.row()
		analyzeButtonRow.scale_y=3.0
		analyzeButtonRow.operator('wm.analyze_operator')
		generateButtonRow = self.layout.row()
		generateButtonRow.scale_y=3.0
		generateButtonRow.operator('wm.hide_operator')
