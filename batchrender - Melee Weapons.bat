@echo off
setlocal enabledelayedexpansion

rem change these to wherever they are located on your machine
set _BLENDERDIR=J:\Ohjelmat\Blender\Blender 2.93\
set _BLENDFILEDIR=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\JA2 2.9_033.blend
set _PYTHONFILE=J:\JA2 1.13 SVN\JA2-Character-Animation-Photobooth\batchrender-meleeweapons


set /A parallelRender=1
if !parallelRender!==1 (
	rem set /p decision=Input amount of blender processes: 
	set /a decision=4
)


echo Rendering melee weapons animations
echo opening blender and starting rendering
cd !_BLENDERDIR!


rem 1> nul ==> suppress text output <- Not using this makes headless rendering considerably slower than just doing CTRL + F12 in blender.
rem 2> nul ==> suppress error output
if !parallelRender!==0 (
	blender.exe 1> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!0.py"
) ELSE (
	set /a x=!decision! - 1
	for /l %%n in (0,1,!x!) do (
		start /B blender.exe 1> nul 2> nul -b "!_BLENDFILEDIR!" -P "!_PYTHONFILE!%%n.py"
	)


	:LOOP
	tasklist /FI "IMAGENAME eq blender.exe" 2>NUL | find /I /N "blender.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 6 >nul
		GOTO LOOP
	)
)

echo rendering complete!
pause
