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


:AnimDataChoice
echo Choose animation data file
echo [0] rifleAnims.txt
echo [1] pistolAnims.txt
echo [2] noWeaponAnims.txt
set /p animchoice=Choice: 
if %animchoice%==0 (
	set "animData=batchSriptData\rifleAnims.txt"
) else if %animchoice%==1 (
	set animData=batchSriptData\pistolAnims.txt
) else if %animchoice%==2 (
	set animData=batchSriptData\noWeaponAnims.txt
) ELSE (
	echo Invalid choice
	GOTO :AnimDataChoice
)


rem Read animation data
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

echo Printing animation data
echo(
for /L %%i in (0,1,%animIndex%) do call echo "%%animFolders[%%i]%%"
echo(
for /L %%i in (0,1,%animIndex%) do call echo "%%animFrames[%%i]%%"
echo(
for /L %%i in (0,1,%animIndex%) do call echo "%%animFileNames[%%i]%%"
echo(
echo(


rem Create necessary inputs for sticom.exe
for /l %%n in (0,1,!animIndex!) do (
	set /A nframes=!animFrames[%%n]!
	set /A rangeEnd=!nframes! - 2
	
rem	echo "nframes=!nframes!"
rem	echo "rangeEnd=!rangeEnd!"
	rem create input for sticom -r parameter
	set /A framesXdirections=!nframes!*8-1
	set _RANGE[%%n]="0-!framesXdirections!"
	
rem	echo "framesXdirections=!framesXdirections!"
rem	echo "_RANGE=!_RANGE[%%n]!"
	rem convert nframes to hexadecimal
	set "hex=0123456789ABCDEF"
	set /a high=!nframes! / 16
	set /a low=!nframes! %% 16
	
rem	echo "high=!high!"
rem	echo "low=!low!"
	rem create input for sticom -k parameter
	for %%b in (!high!) do set "highHex=!hex:~%%b,1!"
	for %%b in (!low!) do set "lowHex=!hex:~%%b,1!"

	set c=0x!highHex!!lowHex!
rem	echo "c=!c!"
	for /l %%m in (0,1,!rangeEnd!) do (
		call set "c=%%c%% 0x00"
	)
	set _KEYFRAME[%%n]=!c!
rem	echo !_KEYFRAME[%%n]!
)



:ContinueSTI
echo Choose
echo [0] for making a layered body STI
echo [1] for props (AR, Shotgun, AK47, Mosin Nagant, MP5)
echo [2] props (Vest, Backpack, beret, Helmet, Gasmask)
echo [3] props (Barrett, PKM, M14)
echo [4] props (HK USP, HK USP Left Hand)
echo [5] props (HK MP5K, HK MP5K Left Hand)
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
	for /l %%m in (0,1,!animIndex!) do (
rem		set folderName=!animFolders[%%m]:"=!
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"

		for /l %%n in (0,1,4) do (
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL make_script\extract\*.bmp
			Rem crop and convert rendered images to use correct header type
			make_script\convert.exe "!_INPUTDIR!\!outputPrefix[%%n]!*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
			
			rem create layered .sti files for basebody
			SETLOCAL
			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!suffixList[%%n]!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=make_script\extract\0-%%d.bmp%"
			set "_palette=make_script\Palettes\!chosenPalette!"
			set "_keyframes=!_KEYFRAME[%%m]!"
			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			Rem echo empty lines
			echo(
			
			make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F
			ENDLOCAL
		)
	)
) else if %decision%==1 (
	CALL :CreateBasePropsRifles
) else if %decision%==2 (
	CALL :CreateBasePropsBPandBeret
) else if %decision%==3 (
	CALL :CreateBasePropsBarrett
) else if %decision%==4 (
	CALL :CreateBasePropsDualPistols
) else if %decision%==5 (
	CALL :CreateBasePropsDualMachinePistols
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


:CreateBasePropsRifles
	SETLOCAL
	Rem Assault Rifle
	set propPalettes[0]=!Palettes[0]!
	set propnumbers[0]=1
	set propSuffix[0]=_AR
	Rem Shotgun
	set propPalettes[1]=!Palettes[2]!
	set propnumbers[1]=2
	set propSuffix[1]=_shotgun
	Rem AK47
	set propPalettes[2]=!Palettes[2]!
	set propnumbers[2]=3
	set propSuffix[2]=_AK47
	Rem Mosin Nagant
	set propPalettes[3]=!Palettes[2]!
	set propnumbers[3]=4
	set propSuffix[3]=_mosin
	Rem MP5
	set propPalettes[4]=!Palettes[1]!
	set propnumbers[4]=5
	set propSuffix[4]=_MP5

	for /l %%m in (0,1,!animIndex!) do (
rem		set folderName=!animFolders[%%m]:"=!
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"
		
		for /l %%n in (0,1,4) do (
			set chosenPalette=!propPalettes[%%n]!
			set nProps=!propnumbers[%%n]!
			set _SUFFIX=!propSuffix[%%n]!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL make_script\extract\*.bmp
			Rem crop and convert rendered images to use correct header type
			make_script\convert.exe "!_INPUTDIR!\Prop!nProps!_C*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
			

			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!_SUFFIX!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=make_script\extract\0-%%d.bmp%"
			set "_palette=make_script\Palettes\!chosenPalette!"
			set "_keyframes=!_KEYFRAME[%%m]!"
			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			echo(
		
			make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F
Rem			make_script\sticom.exe new -o "!_FILEPATH!"  -i "make_script\extract\0-%%d.bmp%" -r !_RANGE! -p "make_script\Palettes\!chosenPalette!" --offset !_OFFSET! -k "!c!" -F
		)
	)
	ENDLOCAL
EXIT /B 0

:CreateBasePropsBPandBeret
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

	for /l %%m in (0,1,!animIndex!) do (
rem		set folderName=!animFolders[%%m]:"=!
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"

		for /l %%n in (0,1,4) do (
			set chosenPalette=!propPalettes[%%n]!
			set nProps=!propnumbers[%%n]!
			set _SUFFIX=!propSuffix[%%n]!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL make_script\extract\*.bmp
			Rem crop and convert rendered images to use correct header type
			make_script\convert.exe "!_INPUTDIR!\Prop!nProps!_C*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
			
			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!_SUFFIX!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=make_script\extract\0-%%d.bmp%"
			set "_palette=make_script\Palettes\!chosenPalette!"
			set "_keyframes=!_KEYFRAME[%%m]!"
			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			echo(
			make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F
		)
	)
	ENDLOCAL
EXIT /B 0

:CreateBasePropsBarrett
	SETLOCAL
	Rem Assault Rifle
	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_M82
	Rem Shotgun
	set propPalettes[1]=!Palettes[4]!
	set propnumbers[1]=2
	set propSuffix[1]=_shotgun
	Rem AK47
	set propPalettes[2]=!Palettes[4]!
	set propnumbers[2]=3
	set propSuffix[2]=_PKM
	Rem Mosin Nagant
	set propPalettes[3]=!Palettes[4]!
	set propnumbers[3]=4
	set propSuffix[3]=_mosin
	Rem MP5
	set propPalettes[4]=!Palettes[4]!
	set propnumbers[4]=5
	set propSuffix[4]=_M14

	for /l %%m in (0,1,!animIndex!) do (
rem		set folderName=!animFolders[%%m]:"=!
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"
		
		for /l %%n in (0,1,4) do (
			set chosenPalette=!propPalettes[%%n]!
			set nProps=!propnumbers[%%n]!
			set _SUFFIX=!propSuffix[%%n]!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL make_script\extract\*.bmp
			Rem crop and convert rendered images to use correct header type
			make_script\convert.exe "!_INPUTDIR!\Prop!nProps!_C*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
			

			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!_SUFFIX!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=make_script\extract\0-%%d.bmp%"
			set "_palette=make_script\Palettes\!chosenPalette!"
			set "_keyframes=!_KEYFRAME[%%m]!"
			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			echo(
		
			make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F
		)
	)
	ENDLOCAL
EXIT /B 0


:CreateBasePropsDualPistols
	SETLOCAL
	Rem right pistol
	set propPalettes[0]=!Palettes[1]!
	set propnumbers[0]=1
	set propSuffix[0]=_pistol
	Rem left pistol
	set propPalettes[1]=!Palettes[1]!
	set propnumbers[1]=4
	set propSuffix[1]=_lpistol

	for /l %%m in (0,1,!animIndex!) do (
rem		set folderName=!animFolders[%%m]:"=!
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"
		
		for /l %%n in (0,1,1) do (
			set chosenPalette=!propPalettes[%%n]!
			set nProps=!propnumbers[%%n]!
			set _SUFFIX=!propSuffix[%%n]!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL make_script\extract\*.bmp
			Rem crop and convert rendered images to use correct header type
			make_script\convert.exe "!_INPUTDIR!\Prop!nProps!_C*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
			

			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!_SUFFIX!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=make_script\extract\0-%%d.bmp%"
			set "_palette=make_script\Palettes\!chosenPalette!"
			set "_keyframes=!_KEYFRAME[%%m]!"
			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			echo(
		
			make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F
		)
	)
	ENDLOCAL
EXIT /B 0

:CreateBasePropsDualMachinePistols
	SETLOCAL
	Rem right pistol
	set propPalettes[0]=!Palettes[1]!
	set propnumbers[0]=1
	set propSuffix[0]=_mpistol
	Rem left pistol
	set propPalettes[1]=!Palettes[1]!
	set propnumbers[1]=4
	set propSuffix[1]=_lmpistol

	for /l %%m in (0,1,!animIndex!) do (
rem		set folderName=!animFolders[%%m]:"=!
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"
		
		for /l %%n in (0,1,1) do (
			set chosenPalette=!propPalettes[%%n]!
			set nProps=!propnumbers[%%n]!
			set _SUFFIX=!propSuffix[%%n]!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL make_script\extract\*.bmp
			Rem crop and convert rendered images to use correct header type
			make_script\convert.exe "!_INPUTDIR!\Prop!nProps!_C*.png" -crop 121x121+3+4 BMP3:make_script\extract\0.bmp
			

			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!_SUFFIX!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=make_script\extract\0-%%d.bmp%"
			set "_palette=make_script\Palettes\!chosenPalette!"
			set "_keyframes=!_KEYFRAME[%%m]!"
			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			echo(
		
			make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F
		)
	)
	ENDLOCAL
EXIT /B 0
