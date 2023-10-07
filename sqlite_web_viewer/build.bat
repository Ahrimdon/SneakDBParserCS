@echo off

cd /d %~dp0  :: Change directory to the location of this batch file
call ..\venv\Scripts\activate  :: Activate the virtual environment
pyinstaller --noconfirm --onefile --console --icon "..\assets\build\icon\icon.ico" --add-data "templates;templates" --add-data "static;static" sqlite_web.py --distpath="..\bin" -n "sqlite_web"

rmdir /s /q build
del /q "sqlite_web.spec"

pause