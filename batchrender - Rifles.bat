@echo off
setlocal enabledelayedexpansion

rem change these to wherever they are located on your machine
set _BLENDERDIR=J:\Ohjelmat\Blender\Blender 2.90\
set _BLENDFILEDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\JA2 2.9_033.blend
rem set _OUTPUTDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\output\
set _PYTHONFILE=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-rifles.py
set _PYTHONFILE2=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-rifles2.py
set _PYTHONFILE3=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-rifles3.py

rem echo deleting .png files from !_OUTPUTDIR!
rem cd !_OUTPUTDIR!
rem DEL "!_OUTPUTDIR!*.png"

echo opening blender and starting animation rendering
cd !_BLENDERDIR!
rem 1> nul ==> suppress text output <- Not using this makes headless rendering considerably slower than just doing CTRL + F12 in blender.
rem 2> nul ==> suppress error output
rem blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!"

start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!"
start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE2!"
start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE3!"

echo rendering complete!
pause
