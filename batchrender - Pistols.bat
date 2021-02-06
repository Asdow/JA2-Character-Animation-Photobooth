@echo off
setlocal enabledelayedexpansion

rem change these to wherever they are located on your machine
set _BLENDERDIR=J:\Ohjelmat\Blender\Blender 2.90\
set _BLENDFILEDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\JA2 2.9_033.blend
rem set _OUTPUTDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\output\
set _PYTHONFILE=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-pistols.py
set _PYTHONFILE2=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-pistols2.py

echo Rendering pistol animations
echo opening blender and starting animation rendering
cd !_BLENDERDIR!
rem 1> nul ==> suppress text output <- Not using this makes headless rendering considerably slower than just doing CTRL + F12 in blender.
rem 2> nul ==> suppress error output
set /A parallelRender=1

if !parallelRender!==0 (
	blender.exe 1> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!"
) ELSE (
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!"
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE2!"

	:LOOP
	tasklist /FI "IMAGENAME eq blender.exe" 2>NUL | find /I /N "blender.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 11 >nul
		GOTO LOOP
	)
)

echo rendering complete!
pause
