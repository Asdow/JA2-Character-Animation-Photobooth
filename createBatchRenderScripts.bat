@echo off
setlocal enabledelayedexpansion

JA2-BatchRenderCreator.exe "8" "noWeaponAnims.txt" "batchrender-noweapons.py"
JA2-BatchRenderCreator.exe "4" "meleeWeaponAnims.txt" "batchrender-meleeweapons.py"
JA2-BatchRenderCreator.exe "8" "pistolAnims.txt" "batchrender-pistols.py"
JA2-BatchRenderCreator.exe "8" "rifleAnims.txt" "batchrender-rifles.py"
JA2-BatchRenderCreator.exe "2" "HeavyWeaponAnims.txt" "batchrender-heavyweapons.py"
