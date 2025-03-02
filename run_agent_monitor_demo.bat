@echo off
echo ===================================================
echo      Kairos Intelligence System - Demo de Monitor de Agentes
echo ===================================================
echo.
echo Este script ejecuta una demostración del panel de monitorización de agentes
echo con el nuevo tema mixto y visualización de costos.
echo.
echo Selecciona la versión de Python para ejecutar la demostración:
echo.
echo 1. Python 3.13.2 (C:\Python313\python.exe)
echo 2. Python 3.12.8 (C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe)
echo 3. Python 3.9.7 (C:\Program Files\Python39\python.exe)
echo.

set /p choice="Ingresa el número de tu elección (1-3): "

if "%choice%"=="1" (
    set PYTHON_PATH=C:\Python313\python.exe
    echo.
    echo Ejecutando con Python 3.13...
) else if "%choice%"=="2" (
    set PYTHON_PATH=C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe
    echo.
    echo Ejecutando con Python 3.12...
) else if "%choice%"=="3" (
    set PYTHON_PATH=C:\Program Files\Python39\python.exe
    echo.
    echo Ejecutando con Python 3.9...
) else (
    echo.
    echo Opción inválida. Por favor ejecuta el script nuevamente.
    echo.
    pause
    exit
)

echo.
echo Iniciando demostración del monitor de agentes...
echo.

%PYTHON_PATH% examples/agent_monitor_demo.py

echo.
echo Demostración finalizada.
echo.
pause
