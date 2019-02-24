@ECHO OFF
echo Compiling resources.qrc
pyrcc5 resources.qrc -o ..\resources.py
echo Complete
pause