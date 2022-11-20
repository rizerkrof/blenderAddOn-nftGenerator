#!/usr/bin/env python3
import bpy
import random
from ..utils.blenderUtils import isAttributeCollection, getAttributeNameFromCollectionName, popup
from ..utils.outputUtils import createDirectory, createJsonFile

class Generate(bpy.types.Operator):
	bl_idname='wm.hide_operator'
	bl_label='Generate'
	originLocation={}
	attributeStorage={}
	generateHistory=[]
	keyframeIndex=1
	isExportGLB=True
	objectsNameAllowedForGeneration=[]
	def execute(self,context):
		print('Generation started...')
		bpy.context.scene.frame_set(0)
		self.nameOfObjects = context.scene.generatorSettings.nameOfObjects
		self.description = context.scene.generatorSettings.description
		self.image = context.scene.generatorSettings.image
		self.imageFormat = context.scene.generatorSettings.imageFormat
		for action in bpy.data.actions:
			bpy.data.actions.remove(action)
		self.filteredAttributes=list(filter(isAttributeCollection, bpy.data.collections.keys()))
		for attribute in self.filteredAttributes:
			self.attributeStorage[attribute]=[]
			for attributeValue in bpy.data.collections[attribute].children.keys():
				attributeValueObjectsNames=[]
				for attributeValueObject in bpy.data.collections[attribute].children[attributeValue].all_objects:
					if attributeValueObject.hide_render==False:
						self.objectsNameAllowedForGeneration.append(attributeValueObject.name)
						attributeValueObject.keyframe_insert(data_path='hide_render', frame=0)
						attributeValueObject.keyframe_insert(data_path='hide_viewport', frame=0)
						attributeValueObjectsNames.append(attributeValueObject.name)
				for attributeValueObjectsName in attributeValueObjectsNames:
					self.hideAllRender(attributeValueObjectsName)
				self.attributeStorage[attribute].append(attributeValue)
		self.randomBrackets=self.createPickRandomBrackets(context.scene.traitSettings)
		self.randomBracketsMax=self.createMaxOfBrackets(self.randomBrackets)
		context.scene.generatorSettings.maxIterations = self.recheckNumberOfIterations()
		nIteration=context.scene.generatorSettings.desiredIterations
		context.scene.frame_end=nIteration
		context.scene.frame_start=1
		iteration=0
		while iteration<nIteration:
			if self.generate():
				iteration+=1
		bpy.context.scene.frame_set(0);
		popup('Generation done!')
		return{'FINISHED'}

	def generate(self):
		bpy.ops.object.select_all(action='DESELECT')
		generatedCombination={}
		generatedCombination['name'] = f'{self.nameOfObjects} {self.keyframeIndex:04}'
		generatedCombination['description'] = self.description
		generatedCombination['image'] = f'{self.image}{self.keyframeIndex}{self.imageFormat}'
		generatedCombination['attributes']=[]
		for attributeIndex, attribute in enumerate(self.filteredAttributes):
			rndRarity=random.randrange(0,self.randomBracketsMax[attributeIndex])
			rndAttributeValue=self.findObjectNameInBrackets(rndRarity,attributeIndex,attribute)
			print('=============================', self.keyframeIndex)
			print(attribute, rndAttributeValue)
			for attributeValue in self.attributeStorage[attribute]:
				if attributeValue==rndAttributeValue:
					attributeValueObjects=bpy.data.collections[attribute].children[attributeValue].all_objects
					self.selectTraitObjectsActive(attributeValueObjects)
					self.makeKeyFrameHideOfList(attributeValueObjects)
					attributeMetadata={
						'trait_type':getAttributeNameFromCollectionName(attribute),
						'value':attributeValue
					}
					generatedCombination['attributes'].append(attributeMetadata)
				else:
					self.makeClearKeyframeHideOfList(bpy.data.collections[attribute].children[attributeValue].all_objects)
		createDirectory('metadata')
		createJsonFile(f'metadata_{self.keyframeIndex:04}', 'metadata/', generatedCombination)
		self.keyframeIndex+=1
		return True

	def makeClearKeyframeHideOfList(self, listOfObjects):
		objectsNameAllowedForGeneration=[]
		for object in listOfObjects:
			if object.name in self.objectsNameAllowedForGeneration:
				objectsNameAllowedForGeneration.append(object.name)
		for objectName in objectsNameAllowedForGeneration:
			self.hideAllRender(objectName)
			bpy.context.scene.objects[objectName].keyframe_insert(data_path='hide_render', frame=self.keyframeIndex)
			bpy.context.scene.objects[objectName].keyframe_insert(data_path='hide_viewport', frame=self.keyframeIndex)
		return

	def makeKeyFrameHideOfList(self, listOfObjects):
		objectsNameAllowedForGeneration=[]
		for object in listOfObjects:
			if object.name in self.objectsNameAllowedForGeneration:
				objectsNameAllowedForGeneration.append(object.name)
		for objectName in objectsNameAllowedForGeneration:
			obj=bpy.context.scene.objects[objectName]
			obj.hide_render=False
			obj.hide_viewport=False
			obj.keyframe_insert(data_path='hide_render', frame=self.keyframeIndex)
			obj.keyframe_insert(data_path='hide_viewport', frame=self.keyframeIndex)
			self.hideAllRender(objectName);
			obj.keyframe_insert(data_path='hide_render', frame=self.keyframeIndex+1)
			obj.keyframe_insert(data_path='hide_viewport', frame=self.keyframeIndex+1)
		return

	def selectTraitObjectsActive(self, listOfObjects):
		for object in listOfObjects:
			bpy.context.view_layer.objects.active=object
			object.select_set(True)
		return

	def hideAllRender(self, objectName):
		bpy.context.scene.objects[objectName].hide_render=True
		bpy.context.scene.objects[objectName].hide_viewport=True

	def createPickRandomBrackets(self, traitSettings):
		attributesCommonness=[];
		for attribute in self.filteredAttributes:
			attributeCommonness=[]
			for attributeValueIndex, attributeValue in enumerate(bpy.data.collections[attribute].children.keys()):
				I=bpy.data.collections[attribute].children[attributeValue].all_objects
				attributeValueRarity=traitSettings[attributeValueIndex].rarity
				attributeCommonness.append(100-attributeValueRarity)
			attributesCommonness.append(attributeCommonness)
		return attributesCommonness

	def createMaxOfBrackets(self, randomBrackets):
		maxBrackets=[]
		for attributeCommonness in randomBrackets:
			sum=0
			for attributeValueCommonness in attributeCommonness:
				sum+=attributeValueCommonness
			maxBrackets.append(sum)
		return maxBrackets

	def findObjectNameInBrackets(self, rndIndex, attributeIndex, attributeName):
		attributeValueGenerated=''
		attributeCommonness=self.randomBrackets[attributeIndex]
		count=0
		for index, attributeValueCommonness in enumerate(attributeCommonness):
			if count<=rndIndex and rndIndex<count+attributeValueCommonness:
				attributeValueGenerated=self.attributeStorage[attributeName][index]
			count+=attributeValueCommonness
		return attributeValueGenerated

	def recheckNumberOfIterations(self):
		nIterations=1
		for attribute in self.filteredAttributes:
			nIterations=nIterations*len(bpy.data.collections[attribute].children.keys())
		return nIterations if nIterations!=1 else 0
