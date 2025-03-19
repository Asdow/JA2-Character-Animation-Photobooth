import bpy

def disablePropRenderlayer(propNumber):
	if propNumber < 1 or propNumber > 25:
		print("Invalid prop number. Aborting")
		return False

	if propNumber >= 10:
		number = "0" + str(propNumber)
	else:
		number = "00" + str(propNumber)

	
	propViewLayer = "Prop Viewlayer_" + number
	propGroundShadow = "Prop groundShadow_" + number
	propFreestyle = "Freestyle - Prop_" + number
	propCryptoMatte = "Prop " + str(propNumber)
	
	# Disable file output for node
	if propNumber >= 10:
		fileOutput = "File Output.0" + str(propNumber)
	else:
		fileOutput = "File Output.00" + str(propNumber)
	bpy.data.scenes["camera 1"].node_tree.nodes[fileOutput].mute = True
	
	for scene in bpy.data.scenes:
		for layer in scene.view_layers:
			layerName = layer.name
			if layerName == propViewLayer or layerName == propGroundShadow or layerName == propFreestyle or layerName == propCryptoMatte:
				layer.use = False
	
	return True

def enablePropRenderlayer(propNumber):
	if propNumber < 1 or propNumber > 25:
		print("Invalid prop number. Aborting")
		return False

	if propNumber >= 10:
		number = "0" + str(propNumber)
	else:
		number = "00" + str(propNumber)

	
	propViewLayer = "Prop Viewlayer_" + number
	propGroundShadow = "Prop groundShadow_" + number
	propFreestyle = "Freestyle - Prop_" + number
	propCryptoMatte = "Prop " + str(propNumber)
	
	# Enable file output for node
	if propNumber >= 10:
		fileOutput = "File Output.0" + str(propNumber)
	else:
		fileOutput = "File Output.00" + str(propNumber)
	bpy.data.scenes["camera 1"].node_tree.nodes[fileOutput].mute = False
	
	for scene in bpy.data.scenes:
		for layer in scene.view_layers:
			layerName = layer.name
			if layerName == propViewLayer or layerName == propGroundShadow or layerName == propFreestyle or layerName == propCryptoMatte:
				layer.use = True
	
	return True


def setCameraOrthoScale(scale):
	for scene in bpy.data.scenes:
		for object in bpy.data.objects:
			if "camera 1" in object.name:
				#print(object)
				#object.data.ortho_scale=6.7 # For backup, used for RGM
				object.data.ortho_scale=scale


def disablePropGroundshadows(propNumber):
	if propNumber < 1 or propNumber > 25:
		print("Invalid prop number. Aborting")
		return False
	
	if propNumber >= 10:
		number = "0" + str(propNumber)
	else:
		number = "00" + str(propNumber)

	propGroundShadow = "Prop groundShadow_" + number
	
	for scene in bpy.data.scenes:
		for layer in scene.view_layers:
			layerName = layer.name
			if layerName == propGroundShadow:
				layer.use = False
	
	return True


def enablePropGroundshadows(propNumber):
	if propNumber < 1 or propNumber > 25:
		print("Invalid prop number. Aborting")
		return False
	
	if propNumber >= 10:
		number = "0" + str(propNumber)
	else:
		number = "00" + str(propNumber)

	propGroundShadow = "Prop groundShadow_" + number
	
	for scene in bpy.data.scenes:
		for layer in scene.view_layers:
			layerName = layer.name
			if layerName == propGroundShadow:
				layer.use = True
	
	return True


def disableFullbodyOutput():
	bpy.data.node_groups["JA2 - Full Body Group"].nodes["File Output.026"].mute = True
	#bpy.data.nodes["Group.045"].mute = True

def disableLayeredbodyShadowOutput():
	bpy.data.node_groups["JA2 Layered Sprite - Body Shadow Group"].nodes["File Output"].mute = True
	#bpy.data.nodes["Group.009"].mute = True

def disableLayeredbodyOutput():
	disableLayeredbodyShadowOutput()
	#bpy.data.nodes["Group.010"].mute = True
	for j in range(1,5):
		bpy.data.node_groups["JA2 Layered Sprite - Body Group"].nodes["File Output.00"+str(j)].mute = True


def enableFullbodyOutput():
	bpy.data.node_groups["JA2 - Full Body Group"].nodes["File Output.026"].mute = False
	#bpy.data.nodes["Group.045"].mute = False

def enableLayeredbodyShadowOutput():
	bpy.data.node_groups["JA2 Layered Sprite - Body Shadow Group"].nodes["File Output"].mute = False
	#bpy.data.nodes["Group.009"].mute = False

def enableLayeredbodyOutput():
	enableLayeredbodyShadowOutput()
	#bpy.data.nodes["Group.010"].mute = False
	for j in range(1,5):
		bpy.data.node_groups["JA2 Layered Sprite - Body Group"].nodes["File Output.00"+str(j)].mute = False

def updateWaterVisibility(toggle):
	sceneList = [
		"camera 1", "camera 2", "camera 3", "camera 4", 
		"camera 5", "camera 6", "camera 7", "camera 8"
	]
	sceneList2 = [
		"camera 1 cryptomatte", "camera 2 cryptomatte", "camera 3 cryptomatte", "camera 4 cryptomatte",
		"camera 5 cryptomatte", "camera 6 cryptomatte", "camera 7 cryptomatte", "camera 8 cryptomatte"
	]
	layerList = [
		"Prop View Layer", "Prop Viewlayer", 
		"Prop groundShadow", "Freestyle - Prop"
	]
	bodyLayerlist = [
		"View Layer", "groundShadow", "Freestyle"
	]
	propLayers = [
		"Layer_002", "layer_002", # backpack
		"Layer_018", "layer_018", # EOD Vest
		"Layer_019", "layer_019", # EOD Pants
		"Layer_020", "layer_020", # Ghillie Vest
		"Layer_021", "layer_021"  # Ghillie Pants
	]
	
	if toggle == True:
		for scene in bpy.data.scenes:
			if scene.name in sceneList:
				for layer in scene.view_layers:
					layerName = layer.name
					if layerName in bodyLayerlist:
						for collection in layer.layer_collection.children:
							cName = collection.name
							if "Collection - Water" in cName:
								collection.exclude = False
					elif any(substring in layerName for substring in layerList):
						for collection in layer.layer_collection.children:
							cName = collection.name
							if "Collection - Water" in cName:
								collection.exclude = False
								for childColl in collection.children:
									if "brush" in childColl.name:
										childColl.exclude = True
									# Show water effect with backpack, EOD vest & pants, ghillie suit
									if "Water Volume" in childColl.name and any(substring in layerName for substring in propLayers):
										childColl.exclude = False
									else:
										childColl.exclude = True
			elif scene.name in sceneList2:
				for layer in scene.view_layers:
					layerName = layer.name
					if "Prop" in layerName:
						for collection in layer.layer_collection.children:
							cName = collection.name
							if layerName == "View Layer" and "Collection - Water" in cName:
								collection.exclude = False
							elif "Collection - Water" in cName:
								collection.exclude = True
	else:
		for scene in bpy.data.scenes:
			if scene.name in sceneList:
				for layer in scene.view_layers:
					layerName = layer.name
					for collection in layer.layer_collection.children:
						cName = collection.name
						if "Collection - Water" in cName:
							collection.exclude = True
