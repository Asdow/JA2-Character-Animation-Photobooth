@echo off
setlocal enabledelayedexpansion

Rem output folder for sti files
rem set _OUTPUTDIR=make_script\sti\
set _OUTPUTDIR=H:\JA2 Dev\Data\Anims\LOBOT\RGM\

rem available palettes. Add palettes into the array here and increment the lastPaletteIndex as well.
set Palettes[0]=JA2_character_model_palette_v3.act
set Palettes[1]=guns_universal.stp
set Palettes[2]=guns_AK.stp
set Palettes[3]=Hats.stp
set lastPaletteIndex=3

Rem offset for the frames. Since this doesn't change often, it's not asked.
set _OFFSET="(-60,-77)"


set /p _FILE_NAME=Give a filename for STI (.sti not required): 
set /p ll=Amount of frames per direction: 
set /A nframes=%ll%
set /A rangeEnd=%nframes% - 2

rem create input for sticom -r parameter
set /A framesXdirections=%nframes%*8-1
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
set /p decision=Choose [0] for making a layered body STI, [1] for prop, [2] props (AR, BP, beret), [3] props (BP, beret), [4] props (BP, beret, pistol): 
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
		Rem make_script\convert.exe "output\!outputPrefix[%%n]!*.bmp" -crop 121x121+190+189 BMP3:make_script\extract\0.bmp
		make_script\convert.exe "output\!outputPrefix[%%n]!*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
		
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
) else if %decision%==3 (
	CALL :CreateBasePropsEmptyHands
) else if %decision%==4 (
	CALL :CreateBasePropsPistol
) ELSE (
	CALL :ChoosePalette chosenPalette
	SETLOCAL
	set /p nProps=Input the number of the prop to turn into sti. 
	set /p _SUFFIX=Give a suffix for the prop filename: 

	rem delete any .bmp files from extract folder before converting output frames into there
	DEL make_script\extract\*.bmp
	Rem crop and convert rendered images to use correct header type
	Rem make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+190+189 BMP3:make_script\extract\0.bmp
	make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
	
	set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
	make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
	ENDLOCAL
)


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
	set propPalettes[0]=!Palettes[0]!
	set propnumbers[0]=1
	set propSuffix[0]=_AR
	Rem Backpack
	set propPalettes[1]=!Palettes[0]!
	set propnumbers[1]=2
	set propSuffix[1]=_BP
	Rem beret
	set propPalettes[2]=!Palettes[3]!
	set propnumbers[2]=3
	set propSuffix[2]=_beret

	for /l %%n in (0,1,2) do (
		set chosenPalette=!propPalettes[%%n]!
		set nProps=!propnumbers[%%n]!
		set _SUFFIX=!propSuffix[%%n]!
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
		
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
	)
	ENDLOCAL
EXIT /B 0

:CreateBasePropsEmptyHands
	SETLOCAL
	Rem Backpack
	set propPalettes[0]=!Palettes[0]!
	set propnumbers[0]=2
	set propSuffix[0]=_BP
	Rem beret
	set propPalettes[1]=!Palettes[3]!
	set propnumbers[1]=3
	set propSuffix[1]=_beret

	for /l %%n in (0,1,1) do (
		set chosenPalette=!propPalettes[%%n]!
		set nProps=!propnumbers[%%n]!
		set _SUFFIX=!propSuffix[%%n]!
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
		
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
	)
	ENDLOCAL
EXIT /B 0

:CreateBasePropsPistol
	SETLOCAL
	Rem Backpack
	set propPalettes[0]=!Palettes[0]!
	set propnumbers[0]=2
	set propSuffix[0]=_BP
	Rem beret
	set propPalettes[1]=!Palettes[3]!
	set propnumbers[1]=3
	set propSuffix[1]=_beret
	Rem pistol
	set propPalettes[2]=!Palettes[1]!
	set propnumbers[2]=4
	set propSuffix[2]=_pistol

	for /l %%n in (0,1,2) do (
		set chosenPalette=!propPalettes[%%n]!
		set nProps=!propnumbers[%%n]!
		set _SUFFIX=!propSuffix[%%n]!
		rem delete any .bmp files from extract folder before converting output frames into there
		DEL make_script\extract\*.bmp
		Rem crop and convert rendered images to use correct header type
		make_script\convert.exe output\Prop!nProps!_C*.png -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
		
		set _FILEPATH=!_OUTPUTDIR!%_FILE_NAME%!_SUFFIX!.sti
		echo !_FILEPATH!
		make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
	)
	ENDLOCAL
EXIT /B 0
