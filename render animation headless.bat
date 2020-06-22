@echo off
setlocal enabledelayedexpansion

rem change these to wherever they are located on your machine
set _BLENDERDIR=J:\Ohjelmat\Blender\blender-2.90.0-fd8d245e6a80-windows64\
set _BLENDFILEDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\JA2 2.9_033.blend
set _OUTPUTDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\output\

echo deleting .png files from !_OUTPUTDIR!
cd !_OUTPUTDIR!
DEL "!_OUTPUTDIR!*.png"

echo opening blender and starting animation rendering
cd !_BLENDERDIR!
rem 1> nul ==> suppress text output <- Not using this makes headless rendering considerably slower than just doing CTRL + F12 in blender.
rem 2> nul ==> suppress error output
blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -a

echo rendering complete!
pause
