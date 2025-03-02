@echo off
echo ===================================================
echo      Kairos Intelligence System - Empaquetador
echo ===================================================
echo.
echo Este script empaquetara Kairos como un ejecutable independiente.
echo.
echo Selecciona la version de Python para ejecutar el empaquetador:
echo.
echo 1. Python 3.13.2 (C:\Python313\python.exe)
echo 2. Python 3.12.8 (C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe)
echo 3. Python 3.9.7 (C:\Program Files\Python39\python.exe)
echo.

set /p choice="Ingresa el numero de tu eleccion (1-3): "

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
    echo Opcion invalida. Por favor ejecuta el script nuevamente.
    echo.
    pause
    exit
)

echo.
echo Ejecutando empaquetador de Kairos...
echo.

%PYTHON_PATH% package_kairos.py

echo.
echo Proceso completado.
echo.
pause
