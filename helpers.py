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
