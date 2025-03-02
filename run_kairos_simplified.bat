@echo off
echo Ejecutando Kairos con interfaz simplificada...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no se encuentra en el PATH.
    echo Por favor, instala Python 3.9 o superior.
    pause
    exit /b 1
)

REM Ejecutar Kairos con interfaz simplificada
python run_scripts/run_kairos_simplified.py

REM Si hay un error, mostrar mensaje
if %errorlevel% neq 0 (
    echo.
    echo Error al ejecutar Kairos. Código de error: %errorlevel%
    pause
)
