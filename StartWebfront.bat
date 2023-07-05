@echo off
setlocal

set DATABASE="export/surf_db.db"
set HOST=0.0.0.0
set PORT=7890
set ROWS_PER_PAGE=500

echo.
echo ----------------------------------------------
echo        Starting SQL Web Viewer
echo ----------------------------------------------
echo.

:: Check if the database file exists
if not exist %DATABASE% (
    echo The database file %DATABASE% does not exist.
    echo Please make sure you have a valid surf_maps.db database...
    echo.
    pause
    exit /b
)

:: Start the SQLite Web viewer
echo Starting SQLite Web viewer with the following parameters:
echo Host: %HOST%
echo Port: %PORT%
echo Rows per page: %ROWS_PER_PAGE%
echo Database: %DATABASE%
echo.

python "sqlite_web_viewer/sqlite_web.py" --host=%HOST% --port=%PORT% --no-browser --rows-per-page=%ROWS_PER_PAGE% %DATABASE%

:: Check the exit code of the last command
if errorlevel 1 (
    echo.
    echo An error occurred while starting the SQLite Web viewer.
    pause
)

endlocal