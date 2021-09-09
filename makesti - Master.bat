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
Rem 128*128 orthoScale 4.5 settings
rem set _OFFSET="(-60,-77)"
rem set "_CROPSETTINGS=121x121+3+4"

Rem 192*192 orthoScale 6.75 settings
set _OFFSET="(-0,-0)"
set "_CROPSETTINGS=192x192+0+0"
set _PIVOT=(95,113)

:AnimDataChoice
echo Choose animation data file
echo [0] rifleAnims.txt
echo [1] pistolAnims.txt
echo [2] noWeaponAnims.txt
echo [3] meleeWeaponAnims.txt
echo [4] HeavyWeaponAnims.txt
echo [5] FemaleAnims.txt
set /p animchoice=Choice: 
if %animchoice%==0 (
	set "animData=batchSriptData\rifleAnims.txt"
) else if %animchoice%==1 (
	set animData=batchSriptData\pistolAnims.txt
) else if %animchoice%==2 (
	set animData=batchSriptData\noWeaponAnims.txt
) else if %animchoice%==3 (
	set animData=batchSriptData\meleeWeaponAnims.txt
) else if %animchoice%==4 (
	set animData=batchSriptData\HeavyWeaponAnims.txt
) else if %animchoice%==5 (
	set animData=batchSriptData\FemaleAnims.txt
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
echo [1] props (Vest, Backpack, beret, Helmet, Gasmask, NVG, booney hat, knee pads, camo helmet, long sleeves)
echo [2] assault rifles (FN FAL, M16, AK47, FAMAS, SCAR-H) and sniper rifles (Barrett, Dragunov, PSG1, TRG42, Patriot)
echo [3] smgs (P90, Thompson, PPSH41, MP5) and shotguns (Mossberg 590, Saiga 12K, SPAS 12)
echo [4] lmgs and rifles (RPK, SAW, PKM, Mosin Nagant, M14, Milkor MKL)
echo [5] pistols (USP, MP5K, Desert eagle, SW500)
echo [6] props (Combat knife, crowbar)
echo [7] Radio
echo [8] LAW
echo [9] Camoshirt and camopants
echo [10] props (ballcap)
echo [99] quit
set /p decision=Choice: 
if %decision%==0 (
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

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	set /a count=1
	set /a div=3
	for /l %%m in (0,1,!animIndex!) do (
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"


		for /l %%n in (0,1,4) do (
			set "_EXTRACTDIR=make_script\extract\!folderName!\!outputPrefix[%%n]!"
			IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"
			rem echo !_EXTRACTDIR!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL "!_EXTRACTDIR!\*.bmp"
			Rem crop and convert rendered images to use correct header type
			start /B make_script\convert.exe "!_INPUTDIR!\!outputPrefix[%%n]!*.png" -crop !_CROPSETTINGS! BMP3:"!_EXTRACTDIR!\0.bmp"
		)
		set /a xx=!count! %% !div!
		if !xx! == 0 (
			call :loop1sync
		)
		set /a count+=1
	)
	call :loop1sync
	
	Rem Turn processed images into sti files in parallel
	set /a count=1
	set /a div=3
	for /l %%m in (0,1,!animIndex!) do (
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!

		for /l %%n in (0,1,4) do (
			set "_EXTRACTDIR=make_script\extract\!folderName!\!outputPrefix[%%n]!"
			IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"
			
			rem create layered .sti files for basebody
			SETLOCAL
			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!suffixList[%%n]!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=!_EXTRACTDIR!\0-%%d.bmp%"
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
			
			start /B make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F -M "TRIM" -P !_PIVOT!
			ENDLOCAL
		)
		set /a xx=!count! %% !div!
		if !xx! == 0 (
			call :loop2sync
		)
		set /a count+=1
	)
	call :loop2sync
	
	GOTO :ContinueSTI
) else if %decision%==1 (
	CALL :CreateBasePropsBPandBeret
) else if %decision%==2 (
	CALL :CreateBasePropsAssaultRifles
) else if %decision%==3 (
	CALL :CreateBasePropsSMGs
) else if %decision%==4 (
	CALL :CreateBasePropsLMGandRifles
) else if %decision%==5 (
	CALL :CreateBasePropsDualPistols
) else if %decision%==6 (
	CALL :CreateBasePropsKnifeAndCrowbar
) else if %decision%==7 (
	CALL :CreateRadioProp
) else if %decision%==8 (
	CALL :CreateLAW
) else if %decision%==9 (
	CALL :CreateCamoprops
) else if %decision%==10 (
	CALL :CreateProps2
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



:loop1sync
	SETLOCAL
	:SYNCLOOP1
	tasklist /FI "IMAGENAME eq convert.exe" 2>NUL | find /I /N "convert.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 3 >nul
		GOTO SYNCLOOP1
	)
	ENDLOCAL
EXIT /B 0

:loop2sync
	SETLOCAL
	:SYNCLOOP2
	tasklist /FI "IMAGENAME eq sticom.exe" 2>NUL | find /I /N "sticom.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 3 >nul
		GOTO SYNCLOOP2
	)
	ENDLOCAL
EXIT /B 0


REM functions
:CreateBasePropsAssaultRifles
	SETLOCAL

	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_FAL

	set propPalettes[1]=!Palettes[4]!
	set propnumbers[1]=2
	set propSuffix[1]=_AR

	set propPalettes[2]=!Palettes[4]!
	set propnumbers[2]=3
	set propSuffix[2]=_AK47

	set propPalettes[3]=!Palettes[4]!
	set propnumbers[3]=4
	set propSuffix[3]=_famas

	set propPalettes[4]=!Palettes[4]!
	set propnumbers[4]=5
	set propSuffix[4]=_SCARH


	set propPalettes[5]=!Palettes[4]!
	set propnumbers[5]=6
	set propSuffix[5]=_M82

	set propPalettes[6]=!Palettes[4]!
	set propnumbers[6]=7
	set propSuffix[6]=_dragunov

	set propPalettes[7]=!Palettes[4]!
	set propnumbers[7]=8
	set propSuffix[7]=_PSG1

	set propPalettes[8]=!Palettes[4]!
	set propnumbers[8]=9
	set propSuffix[8]=_TRG42

	set propPalettes[9]=!Palettes[4]!
	set propnumbers[9]=10
	set propSuffix[9]=_Patriot
	set /a maxProps=9

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps

	ENDLOCAL
EXIT /B 0


:CreateBasePropsBPandBeret
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


	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps

	ENDLOCAL
EXIT /B 0


:CreateProps2
	SETLOCAL
	set propPalettes[0]=!Palettes[0]!
	set propnumbers[0]=1
	set propSuffix[0]=_bcap

	set /a maxProps=0


	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps

	ENDLOCAL
EXIT /B 0


:CreateCamoprops
	SETLOCAL
	set chosenPalette=!Palettes[5]!
	set outputPrefix[0]=Legs
	set suffixList[0]=_camolegs

	set /a maxProps=0

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	set /a count=1
	set /a div=4
	for /l %%m in (0,1,!animIndex!) do (
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"


		for /l %%n in (0,1,!maxProps!) do (
			set "_EXTRACTDIR=make_script\extract\!folderName!\!outputPrefix[%%n]!"
			IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"
			rem echo !_EXTRACTDIR!
			rem delete any .bmp files from extract folder before converting output frames into there
			DEL "!_EXTRACTDIR!\*.bmp"
			Rem crop and convert rendered images to use correct header type
			start /B make_script\convert.exe "!_INPUTDIR!\!outputPrefix[%%n]!*.png" -crop !_CROPSETTINGS! BMP3:"!_EXTRACTDIR!\0.bmp"
		)
		set /a xx=!count! %% !div!
		if !xx! == 0 (
			call :loop1sync
		)
		set /a count+=1
	)
	call :loop1sync
	
	Rem Turn processed images into sti files in parallel
	set /a count=1
	set /a div=4
	for /l %%m in (0,1,!animIndex!) do (
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!

		for /l %%n in (0,1,!maxProps!) do (
			set "_EXTRACTDIR=make_script\extract\!folderName!\!outputPrefix[%%n]!"
			IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"
			
			rem create layered .sti files for basebody
			SETLOCAL
			set _FILE_NAME=!animFileNames[%%m]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!suffixList[%%n]!.sti
			set _range=!_RANGE[%%m]!
			set "_extract=!_EXTRACTDIR!\0-%%d.bmp%"
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
			
			start /B make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F -M "TRIM" -P !_PIVOT!
			ENDLOCAL
		)
		set /a xx=!count! %% !div!
		if !xx! == 0 (
			call :loop2sync
		)
		set /a count+=1
	)
	call :loop2sync



	
	set propPalettes[0]=!Palettes[5]!
	set propnumbers[0]=10
	set propSuffix[0]=_camolsleeve

	set /a maxProps=0


	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps

	ENDLOCAL
EXIT /B 0



:CreateBasePropsLMGandRifles
	SETLOCAL

	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_RPK

	set propPalettes[1]=!Palettes[4]!
	set propnumbers[1]=2
	set propSuffix[1]=_SAW

	set propPalettes[2]=!Palettes[4]!
	set propnumbers[2]=3
	set propSuffix[2]=_PKM

	set propPalettes[3]=!Palettes[4]!
	set propnumbers[3]=4
	set propSuffix[3]=_mosin

	set propPalettes[4]=!Palettes[4]!
	set propnumbers[4]=5
	set propSuffix[4]=_M14

	set propPalettes[5]=!Palettes[4]!
	set propnumbers[5]=6
	set propSuffix[5]=_MKL

	set propPalettes[6]=!Palettes[4]!
	set propnumbers[6]=7
	set propSuffix[6]=_RR
	set /a maxProps=6

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps
	ENDLOCAL
EXIT /B 0


:CreateBasePropsSMGs
	SETLOCAL

	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_P90

	set propPalettes[1]=!Palettes[4]!
	set propnumbers[1]=2
	set propSuffix[1]=_M1A1

	set propPalettes[2]=!Palettes[4]!
	set propnumbers[2]=3
	set propSuffix[2]=_PPSH41

	set propPalettes[3]=!Palettes[4]!
	set propnumbers[3]=4
	set propSuffix[3]=_MP5


	set propPalettes[4]=!Palettes[4]!
	set propnumbers[4]=5
	set propSuffix[4]=_shotgun

	set propPalettes[5]=!Palettes[4]!
	set propnumbers[5]=6
	set propSuffix[5]=_Saiga

	set propPalettes[6]=!Palettes[4]!
	set propnumbers[6]=7
	set propSuffix[6]=_spas12

	set propPalettes[7]=!Palettes[4]!
	set propnumbers[7]=8
	set propSuffix[7]=_uzi

	set /a maxProps=7

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps
	ENDLOCAL
EXIT /B 0



:CreateBasePropsDualPistols
	SETLOCAL
	Rem right pistol
	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_pistol
	Rem left pistol
	set propPalettes[1]=!Palettes[4]!
	set propnumbers[1]=2
	set propSuffix[1]=_lpistol

	set propPalettes[2]=!Palettes[4]!
	set propnumbers[2]=3
	set propSuffix[2]=_mpistol

	set propPalettes[3]=!Palettes[4]!
	set propnumbers[3]=4
	set propSuffix[3]=_lmpistol
	
	set propPalettes[4]=!Palettes[4]!
	set propnumbers[4]=5
	set propSuffix[4]=_deagle

	set propPalettes[5]=!Palettes[4]!
	set propnumbers[5]=6
	set propSuffix[5]=_ldeagle
	
	set propPalettes[6]=!Palettes[4]!
	set propnumbers[6]=7
	set propSuffix[6]=_sw500

	set propPalettes[7]=!Palettes[4]!
	set propnumbers[7]=8
	set propSuffix[7]=_lsw500

	set propPalettes[8]=!Palettes[4]!
	set propnumbers[8]=9
	set propSuffix[8]=_uzi_1h

	set propPalettes[9]=!Palettes[4]!
	set propnumbers[9]=10
	set propSuffix[9]=_uzi_1h_l

	set /a maxProps=9

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps
	ENDLOCAL
EXIT /B 0


:CreateBasePropsKnifeAndCrowbar
	SETLOCAL
	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_knife

	set propPalettes[1]=!Palettes[4]!
	set propnumbers[1]=3
	set propSuffix[1]=_crowbar

	set /a maxProps=1

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps
	ENDLOCAL
EXIT /B 0


:CreateRadioProp
	SETLOCAL
	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=2
	set propSuffix[0]=_radio

	set /a maxProps=0
	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps
	ENDLOCAL
EXIT /B 0


:CreateLAW
	SETLOCAL

	set propPalettes[0]=!Palettes[4]!
	set propnumbers[0]=1
	set propSuffix[0]=_LAW

	set /a maxProps=0

	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	CALL :ConvertOutputToExtractForProps
	Rem Turn processed images into sti files in parallel
	CALL :CreateSTIforProps

	ENDLOCAL
EXIT /B 0


:ConvertOutputToExtractForProps
	SETLOCAL
	Rem Convert rendered images into correct bmp and rename them. Everything goes into its own folders underneath makesti/extract to be able to process things in parallel
	set /a count=1
	set /a div=3
	for /l %%m in (0,1,!animIndex!) do (
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		echo(
		echo "---------------"
		echo "!_INPUTDIR!"

		for /l %%n in (0,1,!maxProps!) do (
			set nProps=!propnumbers[%%n]!
			set "_EXTRACTDIR=make_script\extract\!folderName!\Prop!nProps!"
			IF NOT EXIST "!_EXTRACTDIR!" md "!_EXTRACTDIR!"
			DEL "!_EXTRACTDIR!\*.bmp"
			start /B make_script\convert.exe "!_INPUTDIR!\Prop!nProps!_C*.png" -crop !_CROPSETTINGS! BMP3:"!_EXTRACTDIR!\0.bmp"
		)
		set /a xx=!count! %% !div!
		if !xx! == 0 (
			call :loopConvert
		)
		set /a count+=1
	)
	call :loopConvert

	ENDLOCAL
EXIT /B 0

:loopConvert
	SETLOCAL
	:SYNCLOOPoutput
	tasklist /FI "IMAGENAME eq convert.exe" 2>NUL | find /I /N "convert.exe">NUL
	if %ERRORLEVEL%==0 (
		ping localhost -n 4 >nul
		GOTO SYNCLOOPoutput
	)
	ENDLOCAL
EXIT /B 0


:CreateSTIforProps
	SETLOCAL
	Rem Turn processed images into sti files in parallel
	set /a count=1
	set /a div=3
	for /l %%m in (0,1,!animIndex!) do (
		set folderName=!animFolders[%%m]!
		set _INPUTDIR=output\!folderName!
		
		for /l %%n in (0,1,!maxProps!) do (
			set _FILE_NAME=!animFileNames[%%m]!
			set _SUFFIX=!propSuffix[%%n]!
			set _FILEPATH=!_OUTPUTDIR!!_FILE_NAME!!_SUFFIX!.sti
			
			set nProps=!propnumbers[%%n]!
			set "_EXTRACTDIR=make_script\extract\!folderName!\Prop!nProps!"
			set "_extract=!_EXTRACTDIR!\0-%%d.bmp%"
			
			set _range=!_RANGE[%%m]!

			set chosenPalette=!propPalettes[%%n]!
			set "_palette=make_script\Palettes\!chosenPalette!"

			set "_keyframes=!_KEYFRAME[%%m]!"

			echo !_FILEPATH!
rem			echo !_extract!
rem			echo !_range!
			echo !_palette!
rem			echo !_OFFSET!
rem			echo !_keyframes!
			echo(
		
			start /B make_script\sticom.exe new -o "!_FILEPATH!"  -i "!_extract!" -r !_range! -p "!_palette!" --offset !_OFFSET! -k "!_keyframes!" -F -M "TRIM" -P !_PIVOT!
		)
		set /a xx=!count! %% !div!
		if !xx! == 0 (
			call :sticomLoop
		)
		set /a count+=1
	)
	call :sticomLoop

	ENDLOCAL
EXIT /B 0

:sticomLoop
	SETLOCAL
	:SYNCLOOPsti
	tasklist /FI "IMAGENAME eq sticom.exe" 2>NUL | find /I /N "sticom.exe">NUL
	if !ERRORLEVEL!==0 (
		ping localhost -n 4 >nul
		GOTO SYNCLOOPsti
	)
	ENDLOCAL
EXIT /B 0

