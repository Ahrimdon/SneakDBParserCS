@echo off
cd /d %~dp0  :: Change directory to the location of this batch file
call venv\Scripts\activate  :: Activate the virtual environment
pyinstaller --noconfirm --onefile --console --icon "build\assets\icon\icon.ico" --add-data "build\assets\frequencies.json;charset_normalizer/assets/" main.py --distpath="build" -n "SneakDBParser"
pause
