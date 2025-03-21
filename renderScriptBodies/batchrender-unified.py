from enum import Enum
class BodyType(Enum):
	RegMale = 1
	BigMale = 2
	RegFemale = 3
	SpaceMarine = 4
	EliteOperator = 5
	
# Sanity checks before rendering
bpy.data.objects["rig"].data.pose_position = 'POSE'
bpy.data.objects["Armature - Helirope"].data.pose_position = 'POSE'
bpy.data.objects["Armature - Rock"].data.pose_position = 'POSE'
bpy.context.scene.frame_start = 1
for j in range(1,26):
	helpers.enablePropRenderlayer(j)



objectList = [
	"Weapon", "Vest", "Backpack", "Hat",
	"Face", "Legs", "Body", "Item", "Helmet", "Ghillie"
]

rifleActions = [
	"Standing - Rifle - Aim", "Crouch - Rifle - Aim & Shoot", "Prone - Rifle - Crawl & Shoot",
	"Standing - Rifle - Shoot low", "Standing - Rifle - Hip Aim", "Standing - Rifle - Hip Shoot low",
	"Standing - Rifle - Aim Badass", "Crouch - Rifle - Aim & Shoot Badass", "Prone - Rifle - Crawl & Shoot Badass",	"Standing - Rifle - Hip Aim Badass",
	"Standing - Rifle - Aim & Shoot - Female", "Crouch - Rifle - Aim & Shoot - Female", "Prone - Rifle - Crawl & Shoot - Female",
	"Standing - Rifle - Shoot low - Female", "Standing - Rifle - Hip Aim - Female", "Standing - Rifle - Hip Shoot low - Female",
	"Standing - Rifle - Hip Aim Water", "Standing - Rifle - Aim Water", "Standing - Rifle - Aim & Shoot - Female Water",
	"Standing - Rifle - Hip Aim - Female Water"
]

pistolActions = [
	"Standing - Pistol - Aim & Shoot", "Crouch - Pistol - Aim & Shoot", "Standing - Pistol - Shoot low",
	"Standing - Pistol - Aim & Shoot - One Handed", "Standing - Pistol - Aim Badass", 
	"Standing - Pistol - Aim & Shoot - Female", "Crouch - Pistol - Aim & Shoot - Female",
	"Standing - Pistol - Shoot low - Female", "Standing - Pistol - Aim & Shoot - One Handed - Female",
	"Prone - Pistol - Crawl & Shoot", "Standing - Pistol - Aim & Shoot Water", "Standing - Pistol - Aim Badass Water",
	"Standing - Pistol - Aim & Shoot - Female Water"
]

dualPistolActions = [
	"Standing - Dual Pistols - Aim & Shoot", "Crouch - Dual Pistol - Aim & Shoot", 
	"Standing - Dual Pistols - Aim & Shoot - Female", "Crouch - Dual Pistol - Aim & Shoot - Female",
	"Prone - Dual Pistol - Shoot", "Standing - Dual Pistols - Aim & Shoot Water", "Standing - Dual Pistols - Aim & Shoot - Female Water"
]

radioActions = [
	"Standing - Empty Hands - Radio", "Crouch - Empty Hands - Radio", "Standing - Empty Hands - Use Remote",
	"Standing - Empty Hands - Radio - Female", "Crouch - Empty Hands - Radio - Female", "Standing - Empty Hands - Use Remote - Female"
]

knifeActions = [
	"Standing - Knife - Stab", "Standing - Knife - Slice", "Standing - Knife - Breath",
	"Standing - Knife - Stab - Female", "Standing - Knife - Slice - Female", "Standing - Knife - Breath - Female"
 ]

deathActions = [
	"Standing - Empty Hands - Hit and die", "Standing - Empty Hands - Hit and die 2", "Prone - Empty Hands - Hit and die",
	"Standing - Empty Hands - Flyback hit"
]


# Select which bodytype to render
bodytype = BodyType.RegMale

propsOnly = True
layeredBody = True
renderSet = 1


for i in range(len(animationArray)):
	# Set up specific animation and its end frame
	currentAction = animationArray[i][0]
	bpy.data.objects["rig"].animation_data.action = bpy.data.actions.get(currentAction)
	bpy.context.scene.frame_end = animationArray[i][1]


	# Setup output folders according to current animation
	outputfolder = "//output/" + currentAction
	for j in range(1,5):
		bpy.data.node_groups["JA2 Layered Sprite - Body Group"].nodes["File Output.00"+str(j)].base_path = outputfolder
	bpy.data.node_groups["JA2 Layered Sprite - Body Shadow Group"].nodes["File Output"].base_path = outputfolder
	bpy.data.node_groups["JA2 - Full Body Group"].nodes["File Output.026"].base_path = outputfolder
	
	# Prop 1, 2, 3...10 outputs
	for j in range(1,26):
		if j < 10:
			number = "00" + str(j)
		else:
			number = "0" + str(j)
		bpy.data.scenes["camera 1"].node_tree.nodes["File Output." + number].base_path = outputfolder	
	

	# Hide objects in renders
	for object in bpy.data.objects:
		objectName = object.name
		if any(substring in objectName for substring in objectList):
			object.hide_render = True
		if "MuzzleFlash" in objectName:
			object.hide_render = True
			object.animation_data.action = bpy.data.actions.get("HideMuzzleFlash")
		if "BloodPool" in objectName:
			object.hide_render = True
			object.animation_data.action = bpy.data.actions.get("HideMuzzleFlash")			

	# Bodytypes
	bpy.data.objects["Body - FGM - Head"].hide_render = True # For EOD suit
	bpy.data.objects["Body - RGM - Head"].hide_render = True # For EOD suit
	bpy.data.objects["Body - RGM - Legs"].hide_render = True # For EOD vest, when prone


	# Camera scale and bodytype specific setup
	if bodytype is BodyType.RegMale:
		bpy.data.objects["Body - RGM"].hide_render = False
		helpers.setCameraOrthoScale(6.6)
	if bodytype is BodyType.BigMale:
		bpy.data.objects["Body - BGM"].hide_render = False
		helpers.setCameraOrthoScale(6.0)
	if bodytype is BodyType.RegFemale:
		bpy.data.objects["Body - FGM"].hide_render = False
		helpers.setCameraOrthoScale(6.6)
	if bodytype is BodyType.EliteOperator:
		bpy.data.objects["Body - Elite Camo"].hide_render = False
		bpy.data.node_groups["Background Group"].nodes["Switch"].check = True
	if bodytype is BodyType.SpaceMarine:
		helpers.setCameraOrthoScale(6.0)
		bpy.data.objects["SpaceMarine__mesh"].hide_render = False
		bpy.data.objects["SM_arm_left"].hide_render = False
		bpy.data.objects["SM_arm_right"].hide_render = False
		bpy.data.objects["sm_chest"].hide_render = False
		bpy.data.objects["sm_helmet"].hide_render = False
		bpy.data.objects["sm_jetpack"].hide_render = False
		bpy.data.objects["sm_leg_left"].hide_render = False
		bpy.data.objects["sm_leg_right"].hide_render = False
		bpy.data.objects["sm_pelvis"].hide_render = False
		bpy.data.objects["sm_shoulder_left"].hide_render = False
		bpy.data.objects["sm_shoulder_right"].hide_render = False
		bpy.data.node_groups["Background Group"].nodes["Switch"].check = True
	else:
		bpy.data.objects["SM_arm_left"].hide_render = True
		bpy.data.objects["SM_arm_right"].hide_render = True
		bpy.data.objects["sm_chest"].hide_render = True
		bpy.data.objects["sm_helmet"].hide_render = True
		bpy.data.objects["sm_jetpack"].hide_render = True
		bpy.data.objects["sm_leg_left"].hide_render = True
		bpy.data.objects["sm_leg_right"].hide_render = True
		bpy.data.objects["sm_pelvis"].hide_render = True
		bpy.data.objects["sm_shoulder_left"].hide_render = True
		bpy.data.objects["sm_shoulder_right"].hide_render = True

	
	# Set up water animations
	if "Water" in currentAction:
		helpers.updateWaterVisibility(True)
		for j in range(1,26):
			helpers.disablePropGroundshadows(j)
	else:
		helpers.updateWaterVisibility(False)
		for j in range(1,26):
			helpers.enablePropGroundshadows(j)


	# Set body file outputs
	if propsOnly:
		helpers.disableLayeredbodyOutput()
		helpers.disableFullbodyOutput()
	elif layeredBody:
		helpers.disableFullbodyOutput()
		helpers.enableLayeredbodyOutput()
	else:
		helpers.enableFullbodyOutput()
		helpers.disableLayeredbodyOutput()


	# Display props in renders depending on the set
	if renderSet == 0:
		# Do not render props
		for j in range(1,26):
			helpers.disablePropRenderlayer(j)
		
		if currentAction in deathActions and layeredBody == False:
			#bpy.data.objects["BloodPool"].hide_render = False
			#bpy.data.objects["BloodPool"].animation_data.action = bpy.data.actions.get("Standing - Empty Hands - Hit and die - Blood Pool")
			#bpy.data.objects["BloodPool.Prone"].hide_render = False
			#bpy.data.objects["BloodPool.Prone"].animation_data.action = bpy.data.actions.get("Prone - Get Hit And Die - Blood")
			bpy.data.objects["BloodPool.FlyBack"].hide_render = False
			bpy.data.objects["BloodPool.FlyBack"].animation_data.action = bpy.data.actions.get("Standing - Empty Hands - Flyback hit - Blood")
		
	elif renderSet == 1:
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
		bpy.data.objects["Weapon - P90"].hide_render = False
		bpy.data.objects["Weapon - Thompson M1A1"].hide_render = False
		bpy.data.objects["Weapon - PPSH41"].hide_render = False
		bpy.data.objects["Weapon - HK MP5"].hide_render = False
		bpy.data.objects["Weapon - Shotgun"].hide_render = False
		bpy.data.objects["Weapon - Saiga 12K"].hide_render = False
		bpy.data.objects["Weapon - SPAS12"].hide_render = False
		bpy.data.objects["Weapon - UZI SMG"].hide_render = False
		bpy.data.objects["Weapon - RPK"].hide_render = False
		bpy.data.objects["Weapon - SAW"].hide_render = False
		bpy.data.objects["Weapon - PKM"].hide_render = False
		bpy.data.objects["Weapon - Mosin Nagant"].hide_render = False
		bpy.data.objects["Weapon - M14"].hide_render = False
		bpy.data.objects["Weapon - Milkor"].hide_render = False
		bpy.data.objects["Weapon - Rocket Rifle"].hide_render = False
		# Display muzzleflashes only in relevant animations
		if currentAction in rifleActions:
			bpy.data.objects["MuzzleFlash - FN FAL"].hide_render = False
			bpy.data.objects["MuzzleFlash - M16"].hide_render = False
			bpy.data.objects["MuzzleFlash - AK47"].hide_render = False
			bpy.data.objects["MuzzleFlash - FAMAS"].hide_render = False
			bpy.data.objects["MuzzleFlash - SCAR-H"].hide_render = False
			bpy.data.objects["MuzzleFlash - Barrett"].hide_render = False
			bpy.data.objects["MuzzleFlash - Dragunov"].hide_render = False
			bpy.data.objects["MuzzleFlash - PSG1"].hide_render = False
			bpy.data.objects["MuzzleFlash - TRG42"].hide_render = False
			bpy.data.objects["MuzzleFlash - Mossberg Patriot"].hide_render = False
			bpy.data.objects["MuzzleFlash - P90"].hide_render = False
			bpy.data.objects["MuzzleFlash - Thompson M1A1"].hide_render = False
			bpy.data.objects["MuzzleFlash - PPSH41"].hide_render = False
			bpy.data.objects["MuzzleFlash - MP5"].hide_render = False
			bpy.data.objects["MuzzleFlash - Shotgun"].hide_render = False
			bpy.data.objects["MuzzleFlash - Saiga 12K"].hide_render = False
			bpy.data.objects["MuzzleFlash - SPAS12"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI SMG"].hide_render = False
			bpy.data.objects["MuzzleFlash - RPK"].hide_render = False
			bpy.data.objects["MuzzleFlash - SAW"].hide_render = False
			bpy.data.objects["MuzzleFlash - PKM"].hide_render = False
			bpy.data.objects["MuzzleFlash - Mosin Nagant"].hide_render = False
			bpy.data.objects["MuzzleFlash - M14"].hide_render = False
			bpy.data.objects["MuzzleFlash - FN FAL"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - M16"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - AK47"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - FAMAS"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SCAR-H"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Barrett"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Dragunov"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - PSG1"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - TRG42"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Mossberg Patriot"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - P90"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Thompson M1A1"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - PPSH41"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - MP5"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Shotgun"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Saiga 12K"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SPAS12"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - UZI SMG"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - RPK"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SAW"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - PKM"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Mosin Nagant"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - M14"].animation_data.action = bpy.data.actions.get(currentAction)
			
	elif renderSet == 2:
		# Default case is regular male
		bpy.data.objects["Vest - Flak Jacket"].hide_render = False
		bpy.data.objects["Backpack - Backpack"].hide_render = False
		bpy.data.objects["Hat - Beret"].hide_render = False
		bpy.data.objects["Hat - Helmet"].hide_render = False
		bpy.data.objects["Face - Gasmask"].hide_render = False
		bpy.data.objects["Face - NVG"].hide_render = False
		bpy.data.objects["Hat - Booney"].hide_render = False
		bpy.data.objects["Legs - Kneepad - Left"].hide_render = False
		bpy.data.objects["Legs - Kneepad - Right"].hide_render = False
		bpy.data.objects["Hat - Camo Helmet"].hide_render = False
		bpy.data.objects["Vest - Long Sleeved"].hide_render = False
		bpy.data.objects["Hat - Ballcap"].hide_render = False
		bpy.data.objects["Vest - Kevlar"].hide_render = False
		bpy.data.objects["Hat - Balaclava"].hide_render = False
		bpy.data.objects["Vest - Spectra"].hide_render = False
		bpy.data.objects["Legs - Holster - Right"].hide_render = False
		bpy.data.objects["Legs - Holster - Left"].hide_render = False
		# EOD suit requires a lot of special handling so the EOD vest is hidden by default
		bpy.data.objects["Helmet - EOD"].hide_render = False
		bpy.data.objects["Vest - EOD"].hide_render = True
		bpy.data.objects["Vest - EOD - BGM"].hide_render = True
		bpy.data.objects["Legs - EOD"].hide_render = False
		#Ghillie Suit
		bpy.data.objects["Ghillie - Arms"].hide_render = False
		bpy.data.objects["Ghillie - Torso"].hide_render = False
		bpy.data.objects["Ghillie - Boots"].hide_render = False
		bpy.data.objects["Ghillie - Pants"].hide_render = False
		bpy.data.objects["Ghillie - Hood"].hide_render = False
		
		# Modifiers
		bpy.data.objects["Vest - Flak Jacket"].modifiers["Shrinkwrap"].target = bpy.data.objects["RGM - Vest Target"]
		bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Vest - Kevlar"].modifiers["Shrinkwrap"].target = bpy.data.objects["RGM - Vest Target"]
		bpy.data.objects["Ghillie - Arms"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Ghillie - Torso"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Ghillie - Pants"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Ghillie - Hood"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		
		# Switch the background color to gray for props that use the default bodytype palette
		bpy.data.node_groups["JA2 Layered Sprite - Prop 10"].nodes["Switch.002"].check = False # long sleeves
		bpy.data.node_groups["JA2 Layered Sprite - Prop 11"].nodes["Switch.002"].check = False # ballcap
		bpy.data.node_groups["JA2 Layered Sprite - Prop 13"].nodes["Switch.002"].check = False # balaclava
		
		
		# Change objects depending on the body
		if bpy.data.objects["Body - FGM"].hide_render == False or bpy.data.objects["Body - FGM - Head"].hide_render == False:
			# Hide RGM objects
			bpy.data.objects["Vest - Flak Jacket"].hide_render = True
			bpy.data.objects["Hat - Beret"].hide_render = True
			bpy.data.objects["Hat - Helmet"].hide_render = True
			bpy.data.objects["Hat - Booney"].hide_render = True
			bpy.data.objects["Vest - Long Sleeved"].hide_render = True
			bpy.data.objects["Vest - Kevlar"].hide_render = True
			bpy.data.objects["Hat - Balaclava"].hide_render = True
			bpy.data.objects["Vest - Spectra"].hide_render = True
			bpy.data.objects["Helmet - EOD"].hide_render = True
			# Show RGF specific ones
			bpy.data.objects["Vest - Flak Jacket - Female"].hide_render = False
			bpy.data.objects["Hat - Beret - Female"].hide_render = False
			bpy.data.objects["Hat - Helmet - Female"].hide_render = False
			bpy.data.objects["Hat - Booney - Female"].hide_render = False
			bpy.data.objects["Vest - FGM Long Sleeved"].hide_render = False
			bpy.data.objects["Vest - Kevlar - Female"].hide_render = False
			bpy.data.objects["Hat - Balaclava - RGF"].hide_render = False
			bpy.data.objects["Vest - Spectra - RGF"].hide_render = False
			bpy.data.objects["Helmet - EOD - Female"].hide_render = False

			bpy.data.objects["Vest - Flak Jacket - Female"].modifiers["Shrinkwrap"].target = bpy.data.objects["FGM - Vest Target"]
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
			bpy.data.objects["Vest - Kevlar - Female"].modifiers["Shrinkwrap"].target = bpy.data.objects["FGM - Vest Target"]
			
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			# Hide RGM objects
			bpy.data.objects["Vest - Long Sleeved"].hide_render = True
			bpy.data.objects["Hat - Balaclava"].hide_render = True
			bpy.data.objects["Vest - Spectra"].hide_render = True
			# Show BGM specific ones
			bpy.data.objects["Vest - BGM Long Sleeved"].hide_render = False
			bpy.data.objects["Hat - Balaclava - BGM"].hide_render = False
			bpy.data.objects["Vest - Spectra - BGM"].hide_render = False

			bpy.data.objects["Vest - Flak Jacket"].modifiers["Shrinkwrap"].target = bpy.data.objects["BGM - Vest Target"]
			bpy.data.objects["Hat - Ballcap"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
			bpy.data.objects["Vest - Kevlar"].modifiers["Shrinkwrap"].target = bpy.data.objects["BGM - Vest Target"]
		
		
		# Disable unused renderlayers			
		for j in range(1,7):
			helpers.disablePropRenderlayer(j)
		for j in range(10,18):
			helpers.disablePropRenderlayer(j)
		helpers.disablePropRenderlayer(18) #EOD Vest
		helpers.disablePropRenderlayer(19) #EOD Pants
		#helpers.disablePropRenderlayer(20) #Ghillie Vest
		#helpers.disablePropRenderlayer(21) #Ghillie Pants
		#helpers.disablePropRenderlayer(22) #Ghillie Hood
		helpers.disablePropRenderlayer(23)
		helpers.disablePropRenderlayer(24)
		helpers.disablePropRenderlayer(25)
		
	elif renderSet == 3:
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
		bpy.data.objects["Weapon - SawnOff"].hide_render = False
		bpy.data.objects["Weapon - SawnOff - Left Hand"].hide_render = False
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
			bpy.data.objects["MuzzleFlash - UZI MP"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI MP Left"].hide_render = False
			bpy.data.objects["MuzzleFlash - SawnOff"].hide_render = False
			bpy.data.objects["MuzzleFlash - SawnOff - Left Hand"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK USP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - HK USP - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - HK MP5K"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - HK MP5K - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - Desert Eagle"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Desert Eagle - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - SW500"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SW500 - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - UZI MP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - UZI MP Left"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
			bpy.data.objects["MuzzleFlash - SawnOff"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SawnOff - Left Hand"].animation_data.action = bpy.data.actions.get(leftMuzzleFlashAction)
		if currentAction in pistolActions:
			bpy.data.objects["MuzzleFlash - HK USP"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK MP5K"].hide_render = False
			bpy.data.objects["MuzzleFlash - Desert Eagle"].hide_render = False
			bpy.data.objects["MuzzleFlash - SW500"].hide_render = False
			bpy.data.objects["MuzzleFlash - UZI MP"].hide_render = False
			bpy.data.objects["MuzzleFlash - SawnOff"].hide_render = False
			bpy.data.objects["MuzzleFlash - HK USP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - HK MP5K"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - Desert Eagle"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SW500"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - UZI MP"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.objects["MuzzleFlash - SawnOff"].animation_data.action = bpy.data.actions.get(currentAction)
	
		for j in range(1,11):
			helpers.disablePropRenderlayer(j)
		helpers.disablePropRenderlayer(13)
		helpers.disablePropRenderlayer(14)
		helpers.disablePropRenderlayer(15)
		helpers.disablePropRenderlayer(16)
		helpers.disablePropRenderlayer(17)
		helpers.disablePropRenderlayer(18)
		helpers.disablePropRenderlayer(19)
		helpers.disablePropRenderlayer(20)
		helpers.disablePropRenderlayer(21)
		helpers.disablePropRenderlayer(22)
		helpers.disablePropRenderlayer(23)
		helpers.disablePropRenderlayer(24)
		helpers.disablePropRenderlayer(25)
		
	elif renderSet == 4:
		if currentAction in radioActions:
			bpy.data.objects["Weapon - Radio"].hide_render = False
		if currentAction == "Standing - Empty Hands - Flip Rock":
			bpy.data.objects["Item - Rock"].hide_render = False
			bpy.data.objects["Armature - Rock"].animation_data.action = bpy.data.actions.get(currentAction)
			bpy.data.node_groups["JA2 Layered Sprite - Prop 24"].nodes["Switch.002"].check = False
		# Show rope only in helidrop animation
		if currentAction == "Helidrop":
			bpy.data.objects["Item - Helirope"].hide_render = False
			bpy.data.objects["Armature - Helirope"].animation_data.action = bpy.data.actions.get("Helirope - ArmatureAction")
		
		
		helpers.disablePropRenderlayer(1)
		for j in range(3,24):
			helpers.disablePropRenderlayer(j)
		
	elif renderSet == 5:
		bpy.data.objects["Weapon - Combat Knife"].hide_render = False
		bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get("DisplayProp")
		bpy.data.objects["Weapon - Crowbar"].hide_render = False
		if currentAction in knifeActions:
			bpy.data.objects["Weapon - Combat Knife"].hide_render = False
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get(currentAction)
		if currentAction == "Crouch - Knife - Stab - Female" or currentAction == "Crouch - Knife - Stab":
			bpy.data.objects["Weapon - Combat Knife"].hide_render = True
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get("HideMuzzleFlash")
			bpy.data.objects["Weapon - Combat Knife Alt hold"].hide_render = False
		if currentAction == "Standing - Knife - Throw - Female" or currentAction == "Standing - Knife - Throw":
			bpy.data.objects["Weapon - Combat Knife"].hide_render = False
			bpy.data.objects["Weapon - Combat Knife Alt hold"].hide_render = True
			bpy.data.objects["Weapon - Combat Knife"].animation_data.action = bpy.data.actions.get(currentAction)
		if currentAction == "Standing - Crowbar - Hit - Female" or currentAction == "Standing - Crowbar - Hit":
			bpy.data.objects["Weapon - Crowbar"].hide_render = False
		
		helpers.disablePropRenderlayer(2)
		for j in range(4,26):
			helpers.disablePropRenderlayer(j)
		
	elif renderSet == 6:
		bpy.data.objects["Weapon - LAW"].hide_render = False
		if currentAction == "Crouch - Mortar - Fire":
			bpy.data.objects["Weapon - Mortar Tube"].hide_render = False
			bpy.data.objects["Weapon - Mortar Legs"].hide_render = False
			bpy.data.objects["Armature - Mortar"].animation_data.action = bpy.data.actions.get(currentAction)
		
		for j in range(3,26):
			helpers.disablePropRenderlayer(j)
			
	elif renderSet == 7:
		bpy.data.objects["Weapon - G11"].hide_render = False
		if currentAction in rifleActions:
			bpy.data.objects["MuzzleFlash - G11"].hide_render = False
			bpy.data.objects["MuzzleFlash - G11"].animation_data.action = bpy.data.actions.get(currentAction)
		for j in range(2,26):
			helpers.disablePropRenderlayer(j)
		
	elif renderSet == 8:
		#bpy.data.objects["Weapon - Bolter"].hide_render = False
		bpy.data.objects["Body - RGM - CamoShirt"].hide_render = False
		bpy.data.objects["Body - RGM - CamoLegs"].hide_render = False
		bpy.data.objects["Hat - Booney"].hide_render = False
		bpy.data.objects["Hat - Camo Helmet"].hide_render = False
		#Ghillie Suit
		bpy.data.objects["Ghillie - Arms"].hide_render = False
		bpy.data.objects["Ghillie - Torso"].hide_render = False
		bpy.data.objects["Ghillie - Boots"].hide_render = False
		bpy.data.objects["Ghillie - Pants"].hide_render = False
		bpy.data.objects["Ghillie - Hood"].hide_render = False
		bpy.data.objects["Ghillie - Arms"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Ghillie - Torso"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Ghillie - Pants"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]
		bpy.data.objects["Ghillie - Hood"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - RGM"]

		# Change objects depending on the body
		if bpy.data.objects["Body - FGM"].hide_render == False or bpy.data.objects["Body - FGM - Head"].hide_render == False:
			# Hide RGM objects
			bpy.data.objects["Hat - Booney"].hide_render = True
			bpy.data.objects["Body - RGM - CamoShirt"].hide_render = True
			bpy.data.objects["Body - RGM - CamoLegs"].hide_render = True
			# Show RGF specific ones
			bpy.data.objects["Hat - Booney - Female"].hide_render = False
			bpy.data.objects["Body - FGM - CamoShirt"].hide_render = False
			bpy.data.objects["Body - FGM - CamoLegs"].hide_render = False
			# Modifiers
			bpy.data.objects["Ghillie - Arms"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
			bpy.data.objects["Ghillie - Torso"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
			bpy.data.objects["Ghillie - Pants"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
			bpy.data.objects["Ghillie - Hood"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - FGM"]
			
		elif bpy.data.objects["Body - BGM"].hide_render == False:
			# Hide RGM objects
			bpy.data.objects["Body - RGM - CamoShirt"].hide_render = True
			bpy.data.objects["Body - RGM - CamoLegs"].hide_render = True
			# Show BGM specific ones
			bpy.data.objects["Body - BGM - CamoShirt"].hide_render = False
			bpy.data.objects["Body - BGM - CamoLegs"].hide_render = False
			
			# Modifiers
			bpy.data.objects["Ghillie - Arms"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
			bpy.data.objects["Ghillie - Torso"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
			bpy.data.objects["Ghillie - Pants"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
			bpy.data.objects["Ghillie - Hood"].modifiers["Shrinkwrap"].target = bpy.data.objects["Body - BGM"]
			
		for j in range(3,7):
			helpers.disablePropRenderlayer(j)
		helpers.disablePropRenderlayer(8)
		for j in range(10,20):
			helpers.disablePropRenderlayer(j)
		helpers.disablePropRenderlayer(23)
		helpers.disablePropRenderlayer(24)
		helpers.disablePropRenderlayer(25)


	# RENDER AWAYYY!
	bpy.ops.render.render(animation=True)