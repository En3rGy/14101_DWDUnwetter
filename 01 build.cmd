@echo off
set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib

echo ^<head^> > .\release\log14101.html
echo ^<link rel="stylesheet" href="style.css"^> >> .\release\log14101.html
echo ^<title^>Logik - DWD Unwetter (14101)^</title^> >> .\release\log14101.html
echo ^<style^> >> .\release\log14101.html
echo body { background: none; } >> .\release\log14101.html
echo ^</style^> >> .\release\log14101.html
echo ^<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"^> >> .\release\log14101.html
echo ^</head^> >> .\release\log14101.html

@echo on

type .\README.md | C:\Python27\python -m markdown -x tables >> .\release\log14100.html

cd ..\..
C:\Python27\python generator.pyc "14101_DWDUnwetter" UTF-8

xcopy .\projects\14101_DWDUnwetter\src .\projects\14101_DWDUnwetter\release  /exclude:.\projects\14101_DWDUnwetter\src\exclude.txt

@echo Fertig.

@pause