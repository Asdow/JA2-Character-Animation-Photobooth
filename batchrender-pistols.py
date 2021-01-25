import bpy

# Animation name in blender & end frame
animationArray = [
	("Standing - Empty Hands - Idle", 8),
	("Standing - Empty Hands - Walk", 12),
	("Standing - Empty Hands - Run", 12),
	("Standing - Pistol - Idle", 8),
	("Standing - Pistol - Walk", 12),
	("Standing - Pistol - Walk Aiming", 12),
	("Standing - Pistol - Aim & Shoot", 21),
	("Standing - Pistol - Shoot low", 8),
	("Standing - Pistol - Sidestep Aim Alternate", 12),
	("Standing - Dual Pistols - Aim & Shoot", 25),
	("Standing To Crouch - Empty hands", 15),
	("Crouch - Empty hands - Walk", 22),
	("Crouch - Pistol - Walk Aiming", 24),
	("Crouch - Pistol - Aim & Shoot", 18),
	("Crouch - Dual Pistol - Walk Aiming", 24),
	("Crouch - Dual Pistol - Aim & Shoot", 25)
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

	# Prop 1, 2, 3, 4, 5  outputs in that order
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.004"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.001"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.002"].base_path = outputfolder
	bpy.data.scenes["camera 1"].node_tree.nodes["File Output.003"].base_path = outputfolder


	# Hide and display objects in renders
	# TODO make these change depending on the animation, if needed
	bpy.data.objects["Weapon - FAL"].hide_render = True
	bpy.data.objects["Weapon - Shotgun"].hide_render = False
	bpy.data.objects["Weapon - AK47"].hide_render = True
	bpy.data.objects["Weapon - Mosin Nagant"].hide_render = False
	bpy.data.objects["Weapon - HK MP5"].hide_render = True
	bpy.data.objects["Weapon - Barrett"].hide_render = False
	bpy.data.objects["Weapon - PKM"].hide_render = False
	bpy.data.objects["Weapon - M14"].hide_render = False
	bpy.data.objects["Weapon - HK MP5K"].hide_render = True
	bpy.data.objects["Weapon - HK MP5K - Left Hand"].hide_render = True
	bpy.data.objects["Weapon - HK USP"].hide_render = True
	bpy.data.objects["Weapon - HK USP - Left Hand"].hide_render = True
	bpy.data.objects["Vest - Flak Jacket"].hide_render = True
	bpy.data.objects["Travel_Backpack"].hide_render = True
	bpy.data.objects["Hat - Beret"].hide_render = True
	bpy.data.objects["Hat - Helmet"].hide_render = True
	bpy.data.objects["Face - Gasmask"].hide_render = True

	# RENDER AWAYYY!
	bpy.ops.render.render(animation=True)