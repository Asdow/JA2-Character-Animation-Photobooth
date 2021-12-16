@echo off
setlocal enabledelayedexpansion

DEL "renderGeneratedScripts\*.py"

JA2-BatchRenderCreator.exe "1" "noWeaponAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "meleeWeaponAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "pistolAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "rifleAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "HeavyWeaponAnims.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "1" "FemaleAnims.txt" "batchrender-unified.py"
