# Sanity checks before rendering
bpy.data.objects["rig"].data.pose_position = 'POSE'



objectList = [
	"Weapon", "Vest", "Backpack", "Hat",
	"Face", "Legs", "Body"
]

rifleActions = [
	"Standing - Rifle - Aim", "Crouch - Rifle - Aim & Shoot", "Prone - Rifle - Crawl & Shoot",
	"Standing - Rifle - Shoot low", "Standing - Rifle - Hip Aim", "Standing - Rifle - Hip Shoot low",
	"Standing - Rifle - Aim Badass", "Crouch - Rifle - Aim & Shoot Badass", "Prone - Rifle - Crawl & Shoot Badass",
	"Standing - Rifle - Aim & Shoot - Female", "Crouch - Rifle - Aim & Shoot - Female", "Prone - Rifle - Crawl & Shoot - Female",
	"Standing - Rifle - Shoot low - Female", "Standing - Rifle - Hip Aim - Female", "Standing - Rifle - Hip Shoot low - Female"
]

pistolActions = [
	"Standing - Pistol - Aim & Shoot", "Crouch - Pistol - Aim & Shoot", "Standing - Pistol - Shoot low",
	"Standing - Pistol - Aim & Shoot - One Handed", "Standing - Pistol - Aim Badass", 
	"Standing - Pistol - Aim & Shoot - Female", "Crouch - Pistol - Aim & Shoot - Female",
	"Standing - Pistol - Shoot low - Female", "Standing - Pistol - Aim & Shoot - One Handed - Female",
	"Prone - Pistol - Crawl & Shoot"
]

dualPistolActions = [
	"Standing - Dual Pistols - Aim & Shoot", "Crouch - Dual Pistol - Aim & Shoot", 
	"Standing - Dual Pistols - Aim & Shoot - Female", "Crouch - Dual Pistol - Aim & Shoot - Female",
	"Prone - Dual Pistol - Shoot"
]

radioActions = [
	"Standing - Empty Hands - Radio", "Crouch - Empty Hands - Radio", "Standing - Empty Hands - Use Remote",
	"Standing - Empty Hands - Radio - Female", "Crouch - Empty Hands - Radio - Female", "Standing - Empty Hands - Use Remote - Female"
]

knifeActions = [
	"Standing - Knife - Stab", "Standing - Knife - Slice", "Standing - Knife - Breath",
	"Standing - Knife - Stab - Female", "Standing - Knife - Slice - Female", "Standing - Knife - Breath - Female"
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
		if any(substring in objectName for substring in objectList):
			object.hide_render = True
		if "MuzzleFlash" in objectName:
			object.hide_render = True
			object.animation_data.action = bpy.data.actions.get("HideMuzzleFlash")


	# Bodytypes
	bpy.data.objects["Body - RGM"].hide_render = True
	bpy.data.objects["Body - BGM"].hide_render = True
	bpy.data.objects["Body - FGM"].hide_render = False
	

	if bpy.data.objects["Body - RGM"].hide_render == False:
		helpers.setCameraOrthoScale(6.6)
	if bpy.data.objects["Body - BGM"].hide_render == False:
		helpers.setCameraOrthoScale(6.0)
	if bpy.data.objects["Body - FGM"].hide_render == False:
		helpers.setCameraOrthoScale(6.6)
		


	# Display props in renders depending on the set
	renderSet = 9
	if renderSet == 1:
		bpy.data.objects["Weapon - FN FAL"].hide_render = False
		bpy.data.objects["Weapon - M16"].hide_render = False
		bpy.data.objects["Weapon - AK47"].hide_render = False
		bpy.data.objects["Weapon - FAMAS"].hide_render = False
		bpy.data.objects["Weapon - SCAR-H"].hide_render = False
		bpy.data.objects["Weapon - Barrett"].hide_render = False
		bpy.data.objects["Weapon - Dragunov"].hide_render = False
		bpy.data.objects["Weapon - PSG1"].hide_render = False
		bpy.data.objects["Weapon - TRG42"].hide_render = False
		bpy.data.objects["Weapon - Mossberg Patriot"].hide_render = False
		# Display muzzleflashes only in relevant animations
		if currentAction in rifleActions:
			bpy.data.objects["MuzzleFlash - FN FAL"].hide_render = False
			bpy.data.objects["MuzzleFlash - M16"].hide_render = False
			bpy.data.objects["MuzzleFlash - AK47"].hide_render = False
			bpy.data.objects["MuzzleFlash - FAMAS"].hide_render = False
			bpy.data.objects["MuzzleFlash - SCAR-H"].hide_render = False
			bpy.data.objects["MuzzleFlash - FN FAL"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - M16"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - AK47"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - FAMAS"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SCAR-H"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Barrett"].hide_render = False
			bpy.data.objects["MuzzleFlash - Dragunov"].hide_render = False
			bpy.data.objects["MuzzleFlash - PSG1"].hide_render = False
			bpy.data.objects["MuzzleFlash - TRG42"].hide_render = False
			bpy.data.objects["MuzzleFlash - Mossberg Patriot"].hide_render = False
			bpy.data.objects["MuzzleFlash - Barrett"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Dragunov"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - PSG1"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - TRG42"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Mossberg Patriot"].animation_data.action = bpy.data.actions.get(currentAction)
	elif renderSet == 2:
		bpy.data.objects["Weapon - P90"].hide_render = False
		bpy.data.objects["Weapon - Thompson M1A1"].hide_render = False
		bpy.data.objects["Weapon - PPSH41"].hide_render = False
		bpy.data.objects["Weapon - HK MP5"].hide_render = False
		bpy.data.objects["Weapon - Shotgun"].hide_render = False
		bpy.data.objects["Weapon - Saiga 12K"].hide_render = False
		bpy.data.objects["Weapon - SPAS12"].hide_render = False
		bpy.data.objects["Weapon - UZI SMG"].hide_render = False
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
		# Display muzzleflashes only in relevant animations
		if currentAction in rifleActions:
			bpy.data.objects["MuzzleFlash - P90"].hide_render = False
			bpy.data.objects["MuzzleFlash - Thompson M1A1"].hide_render = False
			bpy.data.objects["MuzzleFlash - PPSH41"].hide_render = False
			bpy.data.objects["MuzzleFlash - MP5"].hide_render = False
			bpy.data.objects["MuzzleFlash - P90"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Thompson M1A1"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - PPSH41"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - MP5"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Shotgun"].hide_render = False
			bpy.data.objects["MuzzleFlash - Saiga 12K"].hide_render = False
			bpy.data.objects["MuzzleFlash - SPAS12"].hide_render = False
			bpy.data.objects["MuzzleFlash - Shotgun"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Saiga 12K"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SPAS12"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - UZI SMG"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI SMG"].animation_data.action = bpy.data.actions.get(currentAction)
	elif renderSet == 3:
		bpy.data.objects["Weapon - RPK"].hide_render = False
		bpy.data.objects["Weapon - SAW"].hide_render = False
		bpy.data.objects["Weapon - PKM"].hide_render = False
		bpy.data.objects["Weapon - Mosin Nagant"].hide_render = False
		bpy.data.objects["Weapon - M14"].hide_render = False
		bpy.data.objects["Weapon - Milkor"].hide_render = False
		bpy.data.objects["Weapon - Rocket Rifle"].hide_render = False
		helpers.disablePropRenderlayer(8)
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
		# Display muzzleflashes only in relevant animations
		if currentAction in rifleActions:
			bpy.data.objects["MuzzleFlash - RPK"].hide_render = False
			bpy.data.objects["MuzzleFlash - SAW"].hide_render = False
			bpy.data.objects["MuzzleFlash - PKM"].hide_render = False
			bpy.data.objects["MuzzleFlash - Mosin Nagant"].hide_render = False
			bpy.data.objects["MuzzleFlash - M14"].hide_render = False
			bpy.data.objects["MuzzleFlash - RPK"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SAW"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - PKM"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Mosin Nagant"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - M14"].animation_data.action = bpy.data.actions.get(currentAction)
	elif renderSet == 4:
		bpy.data.objects["Vest - Flak Jacket - Female"].hide_render = False
		bpy.data.objects["Backpack - Backpack"].hide_render = False
		bpy.data.objects["Hat - Beret - Female"].hide_render = False
		bpy.data.objects["Hat - Helmet - Female"].hide_render = False
		bpy.data.objects["Face - Gasmask"].hide_render = False
		bpy.data.objects["Face - NVG"].hide_render = False
		bpy.data.objects["Hat - Booney - Female"].hide_render = False
		bpy.data.objects["Legs - Kneepad - Left"].hide_render = False
		bpy.data.objects["Legs - Kneepad - Right"].hide_render = False
		bpy.data.objects["Hat - Camo Helmet"].hide_render = False
		
		# Change the flak jacket's shrinkwrap target depending on the body to be rendered
		if bpy.data.objects["Body - RGM"].hide_render == False:
			bpy.data.objects["Vest - Flak Jacket"].modifiers["Shrinkwrap"].target = bpy.data.objects["RGM - Vest Target"]
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			bpy.data.objects["Vest - Flak Jacket"].modifiers["Shrinkwrap"].target = bpy.data.objects["BGM - Vest Target"]
		elif bpy.data.objects["Body - FGM"].hide_render == False:
			bpy.data.objects["Vest - Flak Jacket - Female"].modifiers["Shrinkwrap"].target = bpy.data.objects["FGM - Vest Target"]
		
		# Change the long sleeved mesh depending on body
		if bpy.data.objects["Body - RGM"].hide_render == False:
			bpy.data.objects["Vest - Long Sleeved"].hide_render = False
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			bpy.data.objects["Vest - BGM Long Sleeved"].hide_render = False
		elif bpy.data.objects["Body - FGM"].hide_render == False:
			bpy.data.objects["Vest - FGM Long Sleeved"].hide_render = False
		# Switch the background color to gray for the long sleeved composition groups
		bpy.data.node_groups["JA2 Layered Sprite - Prop 10"].nodes["Switch.002"].check = False
	elif renderSet == 5:
		bpy.data.objects["Weapon - HK USP"].hide_render = False
		bpy.data.objects["Weapon - HK USP - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - HK MP5K"].hide_render = False
		bpy.data.objects["Weapon - HK MP5K - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - Desert Eagle"].hide_render = False
		bpy.data.objects["Weapon - Desert Eagle - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - SW500"].hide_render = False
		bpy.data.objects["Weapon - SW500 - Left Hand"].hide_render = False
		bpy.data.objects["Weapon - UZI MP"].hide_render = False
		bpy.data.objects["Weapon - UZI MP Left"].hide_render = False
		# Display muzzleflashes only in relevant animations
		if currentAction in dualPistolActions:
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
			bpy.data.objects["MuzzleFlash - UZI MP"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI MP Left"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI MP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - UZI MP Left"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
		if currentAction in pistolActions:
			bpy.data.objects["MuzzleFlash - HK USP"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK MP5K"].hide_render = False
			bpy.data.objects["MuzzleFlash - Desert Eagle"].hide_render = False
			bpy.data.objects["MuzzleFlash - SW500"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI MP"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK USP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - HK MP5K"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Desert Eagle"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SW500"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - UZI MP"].animation_data.action = bpy.data.actions.get(currentAction)
	elif renderSet == 6:
		if currentAction in radioActions:
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
	elif renderSet == 7:
		bpy.data.objects["Weapon - Combat Knife"].hide_render = False
		bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get("DisplayProp")
		bpy.data.objects["Weapon - Crowbar"].hide_render = False
		if currentAction in knifeActions:
			bpy.data.objects["Weapon - Combat Knife"].hide_render = False
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get(currentAction)
		if currentAction == "Crouch - Knife - Stab - Female":
			bpy.data.objects["Weapon - Combat Knife"].hide_render = True
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get("HideMuzzleFlash")
			bpy.data.objects["Weapon - Combat Knife Alt hold"].hide_render = False
		if currentAction == "Standing - Knife - Throw - Female":
			bpy.data.objects["Weapon - Combat Knife"].hide_render = False
			bpy.data.objects["Weapon - Combat Knife Alt hold"].hide_render = True
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get(currentAction)
		if currentAction == "Standing - Crowbar - Hit - Female":
			bpy.data.objects["Weapon - Crowbar"].hide_render = False
		helpers.disablePropRenderlayer(2)
		helpers.disablePropRenderlayer(4)
		helpers.disablePropRenderlayer(5)
		helpers.disablePropRenderlayer(6)
		helpers.disablePropRenderlayer(7)
		helpers.disablePropRenderlayer(8)
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
	if renderSet == 8:
		bpy.data.objects["Weapon - LAW"].hide_render = False
		helpers.disablePropRenderlayer(2)
		helpers.disablePropRenderlayer(3)
		helpers.disablePropRenderlayer(4)
		helpers.disablePropRenderlayer(5)
		helpers.disablePropRenderlayer(6)
		helpers.disablePropRenderlayer(7)
		helpers.disablePropRenderlayer(8)
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
	if renderSet == 9:
		bpy.data.objects["Hat - Ballcap"].hide_render = False
		helpers.disablePropRenderlayer(2)
		helpers.disablePropRenderlayer(3)
		helpers.disablePropRenderlayer(4)
		helpers.disablePropRenderlayer(5)
		helpers.disablePropRenderlayer(6)
		helpers.disablePropRenderlayer(7)
		helpers.disablePropRenderlayer(8)
		helpers.disablePropRenderlayer(9)
		helpers.disablePropRenderlayer(10)
		# Change the ballcap's shrinkwrap target depending on the body to be rendered
		if bpy.data.objects["Body - RGM"].hide_render == False:
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
		elif bpy.data.objects["Body - FGM"].hide_render == False:
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
		# Switch the background color to gray
		bpy.data.node_groups["JA2 Layered Sprite - Prop 1"].nodes["Switch.002"].check = False


	# RENDER AWAYYY!
	bpy.ops.render.render(animation=True)