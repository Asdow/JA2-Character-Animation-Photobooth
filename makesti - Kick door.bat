@echo off
setlocal enabledelayedexpansion

Rem output folder for sti files
set _OUTPUTDIR=make_script\sti\
rem set _OUTPUTDIR=H:\JA2 Dev\Data\Anims\LOBOT\RGM\

rem Read available palettes from text file.
set /a lastPaletteIndex=0
FOR /F "tokens=* delims=" %%x in (batchSriptData\palettes.txt) DO (
	set Palettes[!lastPaletteIndex!]=%%~x
	set /a lastPaletteIndex+=1
)
set /a lastPaletteIndex-=1

Rem 192*192 orthoScale 6.75 settings
set _OFFSET="(-0,-0)"
set "_CROPSETTINGS=192x192+0+0"
set _PIVOT=(95,113)

set "_animFolder=Standing - Empty Hands - Kick Door"
set "_output=output\!_animFolder!"
set _FILE_NAME=S_DR_KICK
set ll=20
set /A nframes=%ll%
set /A rangeEnd=%nframes% - 2

rem create input for sticom -r parameter
set /A framesXdirections=%nframes%*4-1
set _RANGE="0-%framesXdirections%"

rem convert nframes to hexadecimal
set "hex=0123456789ABCDEF"
set /a high=%nframes% / 16
set /a low=%nframes% %% 16

rem create input for sticom -k parameter
set c=0x!hex:~%high%,1!!hex:~%low%,1!
for /l %%n in (0,1,%rangeEnd%) do (
	call set "c=%%c%% 0x00"
)



:ContinueSTI
echo Choose
echo [0] for making a layered body STI
echo [1] props (Vest, Backpack, beret, Helmet, Gasmask)
echo [99] quit
set /p decision=Choice: 
if %decision%==0 (
	rem CALL :ChoosePalette chosenPalette
	set chosenPalette=!Palettes[0]!
	set outputPrefix[0]=Shadow
	set outputPrefix[1]=Head
	set outputPrefix[2]=Hands
	set outputPrefix[3]=Torso
	set outputPrefix[4]=Legs

	set suffixList[0]=_shadow
	set suffixList[1]=_head
	set suffixList[2]=_hands
	set suffixList[3]=_torso
	set suffixList[4]=_legs
	for /l %%n in (0,1,4) do (
		set "_EXTRACTDIR=make_script\extract\Standing - Empty Hands - Climb\!outputPrefix[%%n]!"
		IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL "!_EXTRACTDIR!\*.bmp"
		Rem crop and convert rendered images to use correct header type
		start /B make_script\convert.exe "!_output!\!outputPrefix[%%n]!_C2*.png" "!_output!\!outputPrefix[%%n]!_C4*.png" "!_output!\!outputPrefix[%%n]!_C6*.png" "!_output!\!outputPrefix[%%n]!_C8*.png" -crop !_CROPSETTINGS! BMP3:"!_EXTRACTDIR!\0.bmp"
	)
	:SYNCLOOP1
	tasklist /FI "IMAGENAME eq convert.exe" 2>NUL | find /I /N "convert.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 3 >nul
		GOTO SYNCLOOP1
	)

	for /l %%n in (0,1,4) do (
		set "_EXTRACTDIR=make_script\extract\Standing - Empty Hands - Climb\!outputPrefix[%%n]!"
		rem create layered .sti files for basebody
		SETLOCAL
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!suffixList[%%n]!.sti
		echo !_FILEPATH!
		set "_extract=!_EXTRACTDIR!\0-%%d.bmp%"

		start /B make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F -M "TRIM" -P !_PIVOT!
		ENDLOCAL
	)
	:SYNCLOOP2
	tasklist /FI "IMAGENAME eq sticom.exe" 2>NUL | find /I /N "sticom.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 3 >nul
		GOTO SYNCLOOP2
	)
	GOTO :ContinueSTI
) else if %decision%==1 (
 	CALL :CreateBaseProps
) else if %decision%==99 (
	echo Quitting makesti script
	GOTO :EndScript
) ELSE (
	echo Invalid selection
	GOTO :ContinueSTI
)


GOTO :ContinueSTI

:EndScript
EXIT /B %ERRORLEVEL%
pause




:CreateBaseProps
	SETLOCAL
	Rem Vest
	set propPalettes[0]=!Palettes[3]!
	set propnumbers[0]=1
	set propSuffix[0]=_vest
	Rem Backpack
	set propPalettes[1]=!Palettes[3]!
	set propnumbers[1]=2
	set propSuffix[1]=_BP
	Rem beret
	set propPalettes[2]=!Palettes[3]!
	set propnumbers[2]=3
	set propSuffix[2]=_beret
	Rem Helmet
	set propPalettes[3]=!Palettes[3]!
	set propnumbers[3]=4
	set propSuffix[3]=_helmet
	Rem Gasmask
	set propPalettes[4]=!Palettes[3]!
	set propnumbers[4]=5
	set propSuffix[4]=_gasmask
	Rem NVG
	set propPalettes[5]=!Palettes[3]!
	set propnumbers[5]=6
	set propSuffix[5]=_NVG

	set propPalettes[6]=!Palettes[3]!
	set propnumbers[6]=7
	set propSuffix[6]=_Booney

	set propPalettes[7]=!Palettes[3]!
	set propnumbers[7]=8
	set propSuffix[7]=_Pads

	set propPalettes[8]=!Palettes[3]!
	set propnumbers[8]=9
	set propSuffix[8]=_camohelmet

	set propPalettes[9]=!Palettes[0]!
	set propnumbers[9]=10
	set propSuffix[9]=_lsleeve

	set /a maxProps=9

	for /l %%n in (0,1,!maxProps!) do (
		set nProps=!propnumbers[%%n]!

		set "_EXTRACTDIR=make_script\extract\!_animFolder!\Prop!nProps!"
		IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"

		rem delete any .bmp files from extract folder before converting output frames into there
		DEL "!_EXTRACTDIR!\*.bmp"
		Rem crop and convert rendered images to use correct header type
		start /B make_script\convert.exe "!_output!\Prop!nProps!_C2*.png" "!_output!\Prop!nProps!_C4*.png" "!_output!\Prop!nProps!_C6*.png" "!_output!\Prop!nProps!_C8*.png" -crop !_CROPSETTINGS! BMP3:"!_EXTRACTDIR!\0.bmp"
	)
	:SYNCLOOP3
	tasklist /FI "IMAGENAME eq convert.exe" 2>NUL | find /I /N "convert.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 3 >nul
		GOTO SYNCLOOP3
	)


	for /l %%n in (0,1,!maxProps!) do (
		set chosenPalette=!propPalettes[%%n]!
		set nProps=!propnumbers[%%n]!
		set _SUFFIX=!propSuffix[%%n]!
		set "_EXTRACTDIR=make_script\extract\!_animFolder!\Prop!nProps!"
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
		set "_extract=!_EXTRACTDIR!\0-%%d.bmp%"
		set "_palette=make_script\Palettes\!chosenPalette!"
		echo !_FILEPATH!
		start /B make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_RANGE! -p "!_palette!" --offset !_OFFSET! -k "!c!" -F -M "TRIM" -P !_PIVOT!
	)
	:SYNCLOOP4
	tasklist /FI "IMAGENAME eq sticom.exe" 2>NUL | find /I /N "sticom.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 3 >nul
		GOTO SYNCLOOP4
	)
	ENDLOCAL
EXIT /B 0

