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

Rem offset for the frames. Since this doesn't change often, it's not asked.
set _OFFSET="(-60,-77)"


set _FILE_NAME=S_HOP
set ll=18
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
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe "output\Standing - Hop fence\!outputPrefix[%%n]!2*.png" "output\Standing - Hop fence\!outputPrefix[%%n]!4*.png" "output\Standing - Hop fence\!outputPrefix[%%n]!6*.png" "output\Standing - Hop fence\!outputPrefix[%%n]!8*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp

		rem create layered .sti files for basebody
		SETLOCAL
rem		set _FILEPATH=make_script\sti\%_FILE_NAME%!suffixList[%%n]!.sti
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!suffixList[%%n]!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
		ENDLOCAL
	)
) else if %decision%==2 (
 	CALL :CreateBaseProps
) ELSE (
	GOTO :ContinueSTI
)


GOTO :ContinueSTI

:EndScript
EXIT /B %ERRORLEVEL%
pause




:CreateBaseProps
	SETLOCAL
	Rem Vest
	set propPalettes[0]=!Palettes[0]!
	set propnumbers[0]=1
	set propSuffix[0]=_vest
	Rem Backpack
	set propPalettes[1]=!Palettes[0]!
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

	for /l %%n in (0,1,4) do (
		set chosenPalette=!propPalettes[%%n]!
		set nProps=!propnumbers[%%n]!
		set _SUFFIX=!propSuffix[%%n]!
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe "output\Standing - Hop fence\Prop!nProps!_C2*.png" "output\Standing - Hop fence\Prop!nProps!_C4*.png" "output\Standing - Hop fence\Prop!nProps!_C6*.png" "output\Standing - Hop fence\Prop!nProps!_C8*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
		
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
	)
	ENDLOCAL
EXIT /B 0

