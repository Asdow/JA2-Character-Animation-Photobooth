@echo off
setlocal enabledelayedexpansion

rem change these to wherever they are located on your machine
set _BLENDERDIR=J:\Ohjelmat\Blender\Blender 2.90\
set _BLENDFILEDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\JA2 2.9_033.blend
rem set _OUTPUTDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\output\
set _PYTHONFILE=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-noweapons.py
set _PYTHONFILE2=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-noweapons2.py
set _PYTHONFILE3=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-noweapons3.py
set _PYTHONFILE4=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-noweapons4.py
set _PYTHONFILE5=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-noweapons5.py

echo Rendering no weapons animations
echo opening blender and starting rendering
cd !_BLENDERDIR!
rem 1> nul ==> suppress text output <- Not using this makes headless rendering considerably slower than just doing CTRL + F12 in blender.
rem 2> nul ==> suppress error output
set /A parallelRender=1

if !parallelRender!==0 (
	blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!"
) ELSE (
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!"
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE2!"
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE3!"
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE4!"
	start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE5!"

	:LOOP
	tasklist /FI "IMAGENAME eq blender.exe" 2>NUL | find /I /N "blender.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 41 >nul
		GOTO LOOP
	)
)

echo rendering complete!
pause
