@echo off
setlocal enabledelayedexpansion

Rem output folder for sti files
set _OUTPUTDIR=make_script\sti\
rem set _OUTPUTDIR=H:\JA2 Dev\Data\Anims\LOBOT\RGM\

rem available palettes. Add palettes into the array here and increment the lastPaletteIndex as well.
set Palettes[0]=JA2_character_model_palette_v3.act
set Palettes[1]=guns_universal.stp
set Palettes[2]=guns_AK.stp
set Palettes[3]=Hats.stp
set lastPaletteIndex=3

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
set /p decision=Choose [0] for making a layered body STI or [1] for prop STI or [2] for basic props: 
if %decision%==0 (
	rem CALL :ChoosePalette chosenPalette
	set chosenPalette=!Palettes[0]!
	set outputPrefix[0]=Shadow_C
	set outputPrefix[1]=Head_C
	set outputPrefix[2]=Hands_C
	set outputPrefix[3]=Torso_C
	set outputPrefix[4]=Legs_C

	set suffixList[0]=_shadow
	set suffixList[1]=_head
	set suffixList[2]=_hands
	set suffixList[3]=_torso
	set suffixList[4]=_legs
	for /l %%n in (0,1,4) do (
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe "output\!outputPrefix[%%n]!2*.png" "output\!outputPrefix[%%n]!4*.png" "output\!outputPrefix[%%n]!6*.png" "output\!outputPrefix[%%n]!8*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp

		rem create layered .sti files for basebody
		SETLOCAL
rem		set _FILEPATH=make_script\sti\%_FILE_NAME%!suffixList[%%n]!.sti
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!suffixList[%%n]!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
		ENDLOCAL
	)
) else %decision%==2 (
 	CALL :CreateBaseProps
) 
rem ELSE (
rem 	CALL :ChoosePalette chosenPalette
rem 	SETLOCAL
rem 	set /p nProps=Input the number of the prop to turn into sti. 
rem 	set /p _SUFFIX=Give a suffix for the prop filename: 

	rem delete any .bmp files from extract folder before converting output frames into there
rem 	DEL make_script\extract\*.bmp
	Rem crop and convert rendered images to use correct header type
	Rem make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+190+189 BMP3:make_script\extract\0.bmp
rem 	make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
	
rem 	set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
rem 	make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
rem 	ENDLOCAL
rem )


set /p continueChoice=Choose [0] to quit, otherwise jump back to STI choice for next sti: 
if %continueChoice%==0 (
echo Quitting makesti script
GOTO :EndScript
) else (
GOTO :ContinueSTI
)

:EndScript
EXIT /B %ERRORLEVEL%
pause



REM functions
:ChoosePalette
	:PaletteDialog
	for /l %%n in (0,1,%lastPaletteIndex%) do (
		echo %%n !Palettes[%%n]!
	)
	set /p paletteChoice=Select a palette by its index: 
	if %paletteChoice% LSS 0 (
		echo Invalid palette selection!
		GOTO :PaletteDialog
	) else if %paletteChoice% GTR %lastPaletteIndex% (
		echo Invalid palette selection!
		GOTO :PaletteDialog
	) else (
		set chosenPalette=!Palettes[%paletteChoice%]!
	)
EXIT /B 0


:CreateBaseProps
	SETLOCAL
	Rem Assault Rifle
	rem set propPalettes[0]=!Palettes[0]!
	rem set propnumbers[0]=1
	rem set propSuffix[0]=_AR
	Rem Backpack
	rem set propPalettes[1]=!Palettes[0]!
	rem set propnumbers[1]=2
	rem set propSuffix[1]=_BP
	Rem beret
	set propPalettes[0]=!Palettes[3]!
	set propnumbers[0]=3
	set propSuffix[0]=_beret

	for /l %%n in (0,1,0) do (
		set chosenPalette=!propPalettes[%%n]!
		set nProps=!propnumbers[%%n]!
		set _SUFFIX=!propSuffix[%%n]!
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe "output\Prop!nProps!_C2*.png" "output\Prop!nProps!_C4*.png" "output\Prop!nProps!_C6*.png" "output\Prop!nProps!_C8*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
		
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
	)
	ENDLOCAL
EXIT /B 0

