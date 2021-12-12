import bpy

def disablePropRenderlayer(propNumber):
	if propNumber < 1 or propNumber > 25:
		print("Invalid prop number. Aborting")
		return False
	
	propViewLayer = "Prop " + str(propNumber) + " Viewlayer"
	propGroundShadow = "Prop " + str(propNumber) + " groundShadow"
	propFreestyle = "Freestyle - Prop " + str(propNumber)
	propCryptoMatte = "Prop " + str(propNumber)
	
	# Disable file output for node
	if propNumber >= 10:
		fileOutput = "File Output.0" + str(propNumber)
	else:
		fileOutput = "File Output.00" + str(propNumber)
	bpy.data.scenes["camera 1"].node_tree.nodes["fileOutput"].mute_toggle()
	
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