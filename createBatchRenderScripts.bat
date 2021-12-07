@echo off
setlocal enabledelayedexpansion

JA2-BatchRenderCreator.exe "1" "noWeaponAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "meleeWeaponAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "8" "pistolAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "rifleAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "2" "HeavyWeaponAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "FemaleAnims.txt" "batchrender-unified.py"
