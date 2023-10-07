@echo off

cd /d %~dp0  :: Change directory to the location of this batch file
call venv\Scripts\activate  :: Activate the virtual environment
pyinstaller --noconfirm --onefile --console --icon "assets\build\icon\icon.ico" --add-data "assets\build\frequencies.json;charset_normalizer/assets/" main.py --distpath="bin" -n "SneakDBParser"

rmdir /s /q build
del /q "SneakDBParser"

pause
