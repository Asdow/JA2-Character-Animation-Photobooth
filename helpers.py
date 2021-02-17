import bpy

def disablePropRenderlayer(propNumber):
	if propNumber < 1 or propNumber > 10:
		print("Invalid prop number. Aborting")
		return False
	
	propViewLayer = "Prop " + str(propNumber) + " Viewlayer"
	propGroundShadow = "Prop " + str(propNumber) + " groundShadow"
	propFreestyle = "Freestyle - Prop " + str(propNumber)
	propCryptoMatte = "Prop " + str(propNumber)
	
	for scene in bpy.data.scenes:
		for layer in scene.view_layers:
			layerName = layer.name
			if layerName == propViewLayer or layerName == propGroundShadow or layerName == propFreestyle or layerName == propCryptoMatte:
				layer.use = False
	
	return True
