import bpy

# Animation name in blender & end frame
animationArray = [
	("Standing - Empty Hands - Idle",8,"S_N_STD"),
	("Standing - Empty Hands - Walk",12,"S_N_WALK"),
	("Standing - Empty Hands - Hurt Walk",12,"S_N_WALK_HURT"),
	("Standing - Empty Hands - Run",12,"S_N_RUN"),
	("Standing - Empty Hands - Pain",14,"S_N_PAIN"),
	("Standing - Empty Hands - Drunk",20,"S_N_DRUNK"),
	("Standing - Pistol - Idle",8,"S_P_BRTH"),
	("Standing - Pistol - Walk",12,"S_P_WALK"),
	("Standing - Pistol - Walk Aiming",12,"S_P_RDY_WALK2"),
	("Standing - Pistol - Aim & Shoot",21,"S_N_SHOT"),
	("Standing - Pistol - Shoot low",8,"S_P_LOW"),
	("Standing - Pistol - Sidestep Aim Alternate",12,"S_P_SDSP_AIM"),
#	("Standing - Dual Pistols - Aim & Shoot",25,"S_DBLSHOT"),
#	("Standing To Crouch - Empty hands",15,"S_N_CRCH"),
#	("Crouch - Empty hands - Walk",22,"S_N_SWAT"),
#	("Crouch - Pistol - Walk Aiming",24,"cr_walk_pistol"),
#	("Crouch - Pistol - Aim & Shoot",18,"S_CR_AIM_P"),
#	("Crouch - Dual Pistol - Walk Aiming",24,"cr_walk_dual"),
#	("Crouch - Dual Pistol - Aim & Shoot",25,"S_CR_AIM_D"),
#	("Prone - Pistol - Crawl & Shoot",29,"S_N_PRNE"),
#	("Prone - Dual Pistol - Shoot",12,"S_DB_PRN")
]

for i in range(len(animationArray)):
	# Set up specific animation and its end frame
	bpy.context.object.animation_data.action = bpy.data.actions.get(animationArray[i][0])
	bpy.context.scene.frame_end = animationArray[i][1]


	# Setup output folders according to current animation
	outputfolder = "//output/" + animationArray[i][0]
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
	if renderSet == 1:
		bpy.data.objects["Vest - Flak Jacket"].hide_render = False
		bpy.data.objects["Backpack - Backpack"].hide_render = False
		bpy.data.objects["Hat - Beret"].hide_render = False
		bpy.data.objects["Hat - Helmet"].hide_render = False
		bpy.data.objects["Face - Gasmask"].hide_render = False
		bpy.data.objects["Face - NVG"].hide_render = False
		bpy.data.objects["Hat - Booney"].hide_render = False
	elif renderSet == 2:
		bpy.data.objects["Weapon - HK USP"].hide_render = False
		bpy.data.objects["Weapon - HK USP - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - HK MP5K"].hide_render = False
		bpy.data.objects["Weapon - HK MP5K - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - Desert Eagle"].hide_render = False
		bpy.data.objects["Weapon - Desert Eagle - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - SW500"].hide_render = False
		bpy.data.objects["Weapon - SW500 - Left Hand"].hide_render = False
		# Display muzzleflashes only in relevant animations
		if currentAction == "Standing - Dual Pistols - Aim & Shoot" or currentAction == "Crouch - Dual Pistol - Aim & Shoot" or currentAction == "Prone - Dual Pistol - Shoot":
			leftMuzzleFlashAction = "Dual Pistols - Aim & Shoot - Left Muzzleflash"
			if currentAction == "Prone - Dual Pistol - Shoot":
				leftMuzzleFlashAction = "Prone - Dual Pistol - Shoot - Left Muzzleflash"
			bpy.data.objects["MuzzleFlash - HK USP"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK USP - Left Hand"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK MP5K"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK MP5K - Left Hand"].hide_render = False
			bpy.data.objects["MuzzleFlash - Desert Eagle"].hide_render = False
			bpy.data.objects["MuzzleFlash - Desert Eagle - Left Hand"].hide_render = False
			bpy.data.objects["MuzzleFlash - SW500"].hide_render = False
			bpy.data.objects["MuzzleFlash - SW500 - Left Hand"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK USP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - HK USP - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - HK MP5K"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - HK MP5K - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - Desert Eagle"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Desert Eagle - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - SW500"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SW500 - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)

	# RENDER AWAYYY!
	bpy.ops.render.render(animation=True)