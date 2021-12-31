@echo off
setlocal enabledelayedexpansion

rem change these to wherever they are located on your machine
set _BLENDERDIR=J:\\Ohjelmat\\Blender\\Blender 3.0
set _BLENDFILE=JA2 2.9_033.blend
set _PYTHONFILE=batchrender-Animations - Female - Heavy weapons.py


JA2-BatchRender.exe "%_BLENDERDIR%" "%_BLENDFILE%" "%_PYTHONFILE%"

pause
