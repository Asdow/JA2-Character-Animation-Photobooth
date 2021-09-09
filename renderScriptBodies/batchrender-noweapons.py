for i in range(len(animationArray)):
	# Set up specific animation and its end frame
	currentAction = animationArray[i][0]
	bpy.context.object.animation_data.action = bpy.data.actions.get(currentAction)
	bpy.context.scene.frame_end = animationArray[i][1]

	# Setup output folders according to current animation
	outputfolder = "//output/" + currentAction
	for j in range(1,5):
		bpy.data.node_groups["JA2 Layered Sprite - Body Group"].nodes["File Output.00"+str(j)].base_path = outputfolder
	bpy.data.node_groups["JA2 Layered Sprite - Body Shadow Group"].nodes["File Output"].base_path = outputfolder

	# Prop 1, 2, 3...10 outputs in that order
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.004"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.001"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.002"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.003"].base_path = outputfolder # prop 5
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.005"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.006"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.007"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.008"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.009"].base_path = outputfolder


	# Hide objects in renders
	for object in bpy.data.objects:
		objectName = object.name
		if "Weapon" in objectName or "Vest" in objectName or "Backpack" in objectName or "Hat" in objectName or "Face" in objectName or "Legs" in objectName:
			object.hide_render = True
		if "MuzzleFlash" in objectName:
			object.hide_render = True
			object.animation_data.action = bpy.data.actions.get("HideMuzzleFlash")
		if objectName == "Body - RGM" or objectName == "Body - FGM" or objectName == "Body - BGM":
			object.hide_render = True

	# Bodytypes
	bpy.data.objects["Body - RGM"].hide_render = False
	bpy.data.objects["Body - BGM"].hide_render = True
	bpy.data.objects["Body - FGM"].hide_render = True
	

	if bpy.data.objects["Body - RGM"].hide_render == False:
		helpers.setCameraOrthoScale(6.6)
	if bpy.data.objects["Body - BGM"].hide_render == False:
		helpers.setCameraOrthoScale(6.0)



	# Display props in renders depending on the set
	renderSet = 3
	if renderSet == 1:
		bpy.data.objects["Vest - Flak Jacket"].hide_render = False
		# Change the flak jacket's shrinkwrap target depending on the body to be rendered
		if bpy.data.objects["Body - RGM"].hide_render == False:
			bpy.data.objects["Vest - Flak Jacket"].modifiers["Shrinkwrap"].target = bpy.data.objects["RGM - Vest Target"]
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			bpy.data.objects["Vest - Flak Jacket"].modifiers["Shrinkwrap"].target = bpy.data.objects["BGM - Vest Target"]
		bpy.data.objects["Backpack - Backpack"].hide_render = False
		bpy.data.objects["Hat - Beret"].hide_render = False
		bpy.data.objects["Hat - Helmet"].hide_render = False
		bpy.data.objects["Face - Gasmask"].hide_render = False
		bpy.data.objects["Face - NVG"].hide_render = False
		bpy.data.objects["Hat - Booney"].hide_render = False
		bpy.data.objects["Legs - Kneepad - Left"].hide_render = False
		bpy.data.objects["Legs - Kneepad - Right"].hide_render = False
		bpy.data.objects["Hat - Camo Helmet"].hide_render = False
		# Change the long sleeved mesh depending on body
		if bpy.data.objects["Body - RGM"].hide_render == False:
			bpy.data.objects["Vest - Long Sleeved"].hide_render = False
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			bpy.data.objects["Vest - BGM Long Sleeved"].hide_render = False
		# Switch the background color to gray for the long sleeved composition groups
		bpy.data.node_groups["JA2 Layered Sprite - Prop 10"].nodes["Switch.002"].check = False
	elif renderSet == 2:
		if currentAction == "Standing - Empty Hands - Radio" or currentAction == "Crouch - Empty Hands - Radio" or currentAction == "Standing - Empty Hands - Use Remote":
			bpy.data.objects["Weapon - Radio"].hide_render = False
		helpers.disablePropRenderlayer(1)
		helpers.disablePropRenderlayer(3)
		helpers.disablePropRenderlayer(4)
		helpers.disablePropRenderlayer(5)
		helpers.disablePropRenderlayer(6)
		helpers.disablePropRenderlayer(7)
		helpers.disablePropRenderlayer(8)
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
	if renderSet == 3:
		bpy.data.objects["Hat - Ballcap"].hide_render = False
		if bpy.data.objects["Body - RGM"].hide_render == False:
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
		elif bpy.data.objects["Body - FGM"].hide_render == False:
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
		bpy.data.node_groups["JA2 Layered Sprite - Prop 1"].nodes["Switch.002"].check = False
		helpers.disablePropRenderlayer(2)
		helpers.disablePropRenderlayer(3)
		helpers.disablePropRenderlayer(4)
		helpers.disablePropRenderlayer(5)
		helpers.disablePropRenderlayer(6)
		helpers.disablePropRenderlayer(7)
		helpers.disablePropRenderlayer(8)
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
		
	# RENDER AWAYYY!
	bpy.ops.render.render(animation=True)