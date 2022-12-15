@echo off
setlocal enabledelayedexpansion

DEL "renderGeneratedScripts\*.py"

JA2-BatchRenderCreator.exe "10" "Animations - Reg male - All.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Reg male - Heavy weapons.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Reg male - Rifle.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Reg male - Pistol.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Reg male - Melee weapons.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Reg male - Empty hands.txt" "batchrender-unified.py"

JA2-BatchRenderCreator.exe "10" "Animations - Big male - All.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Big male - Heavy weapons.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Big male - Rifle.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Big male - Pistol.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Big male - Melee weapons.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Big male - Empty hands.txt" "batchrender-unified.py"

JA2-BatchRenderCreator.exe "10" "Animations - Female - All.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Female - Heavy weapons.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Female - Rifle.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Female - Pistol.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Female - Melee weapons.txt" "batchrender-unified.py"
JA2-BatchRenderCreator.exe "4" "Animations - Female - Empty hands.txt" "batchrender-unified.py"
