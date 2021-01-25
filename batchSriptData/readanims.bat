@echo off
setlocal enabledelayedexpansion

rem Read rifle anim data
set animData=noWeaponAnims.txt
set /a animIndex=0
FOR /F "tokens=1 delims=()," %%x in (!animData!) DO (
	set animFolders[!animIndex!]=%%~x
	set /a animIndex+=1
)
set /a animIndex-=1

set /a animIndex=0
FOR /F "tokens=2 delims=()," %%x in (!animData!) DO (
	set animFrames[!animIndex!]=%%~x
	set /a animIndex+=1
)
set /a animIndex-=1

set /a animIndex=0
FOR /F "tokens=3 delims=()," %%x in (!animData!) DO (
	set animFileNames[!animIndex!]=%%~x
	set /a animIndex+=1
)
set /a animIndex-=1


for /L %%i in (0,1,%animIndex%) do call echo "%%animFolders[%%i]%%"
for /L %%i in (0,1,%animIndex%) do call echo "%%animFrames[%%i]%%"
for /L %%i in (0,1,%animIndex%) do call echo "%%animFileNames[%%i]%%"


pause