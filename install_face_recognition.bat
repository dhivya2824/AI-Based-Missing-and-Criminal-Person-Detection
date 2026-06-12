@echo off
echo Checking CMake installation...
cmake --version
if %errorlevel% neq 0 (
    echo ERROR: CMake not found! Please install CMake first.
    pause
    exit /b 1
)

echo.
echo CMake found! Installing face-recognition...
pip install --default-timeout=100 face-recognition

echo.
echo Installation complete!
pause
