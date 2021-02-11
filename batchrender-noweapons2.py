import bpy

# Animation name in blender & end frame
animationArray = [
#	("Standing - Hop fence",18,"S_HOP"),
#	("Standing - Empty Hands - Climb",44,"S_CLIMB"),
#	("Standing - Empty Hands - Open door",10,"S_OPEN"),
#	("Standing - Empty Hands - Pickup",5,"S_PICKUP"),
#	("Standing - Punch",24,"S_PUNCH"),
#	("Standing - Empty Hands - Hit and die",33,"S_DIE2"),
#	("Standing - Empty Hands - Hit and die 2",35,"S_D_FWD"),
#	("Standing - Empty Hands - Flyback hit",23,"S_DIEBAC"),
	("Standing - Empty Hands - Flyback & die",24,"S_DIEHARD"),
	("Standing - Empty Hands - Flyback & die BLOOD",7,"S_DIEHARDB"),
	("Standing - Empty Hands - Dodge",6,"S_DODGE"),
	("Standing - Empty Hands - Throw",14,"S_LOB"),
	("Standing - Empty Hands - Lob",14,"S_THROW"),
	("Standing - Empty Hands - Kick Door",20,"S_DR_KICK"),
	("Standing - Empty Hands - Squish",20,"S_SQUISH"),
	("Standing - Empty Hands - Pull",13,"S_PULL"),
	("Standing To Cower - Empty hands",12,"S_COWER"),
	("Crouch - Render medical aid",8,"S_MEDIC"),
	("Crouch - Empty Hands - Hit and die",9,"S_C_DIE"),
	("Crouch - Empty Hands - Punch",14,"S_C_PUNCH"),
	("Prone - Empty Hands - Render Aid",7,"S_PRN_MED"),
	("Prone - Empty Hands - Cower",10,"S_PRNCOW"),
	("Prone - Empty Hands - Hit and die",22,"S_P_DIE"),
	("Prone - Empty Hands - Roll",8,"S_ROLL"),
	("Standing - Knife - Stab",14,"S_STAB"),
	("Standing - Knife - Slice",14,"S_SLICE"),
	("Standing - Knife - Throw",14,"S_K_THROW"),
	("Standing - Knife - Breath",12,"S_K_BREATH"),
	("Crouch - Knife - Stab",14,"S_C_STAB"),
	("Crouch To Prone - Sleep",13,"S_SLEEP")
]

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

	# Prop 1, 2, 3, 4, 5  outputs in that order
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.004"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.001"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.002"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.003"].base_path = outputfolder


	# Hide objects in renders
	for object in bpy.data.objects:
		objectName = object.name
		if "Weapon" in objectName or "Vest" in objectName or "Backpack" in objectName or "Hat" in objectName or "Face" in objectName:
			object.hide_render = True
		if "MuzzleFlash" in objectName:
			object.hide_render = True
			object.animation_data.action = bpy.data.actions.get("HideMuzzleFlash")
		if objectName == "Body - RGM" or objectName == "Body - FGM" or objectName == "Body - BGM":
			object.hide_render = True

	# Bodytypes
	bpy.data.objects["Body - RGM"].hide_render = False
	#bpy.data.objects["Body - FGM"].hide_render = False
	#bpy.data.objects["Body - BGM"].hide_render = False

	# Display props in renders depending on the set
	renderSet = 2
	if renderSet == 1:
		bpy.data.objects["Vest - Flak Jacket"].hide_render = False
		bpy.data.objects["Backpack - Backpack"].hide_render = False
		bpy.data.objects["Hat - Beret"].hide_render = False
		bpy.data.objects["Hat - Helmet"].hide_render = False
		bpy.data.objects["Face - Gasmask"].hide_render = False
	elif renderSet == 2:
		if currentAction == "Standing - Knife - Stab" or currentAction == "Standing - Knife - Slice" or currentAction == "Standing - Knife - Breath":
			bpy.data.objects["Weapon - Combat Knife"].hide_render = False
		if currentAction == "Crouch - Knife - Stab":
			bpy.data.objects["Weapon - Combat Knife Alt hold"].hide_render = False		
		if currentAction == "Standing - Knife - Throw":
			bpy.data.objects["Weapon - Combat Knife"].hide_render = False
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get(currentAction)
		bpy.data.objects["Backpack - Backpack"].hide_render = False
		bpy.data.objects["Face - NVG"].hide_render = False

	# RENDER AWAYYY!
	bpy.ops.render.render(animation=True)