@echo off
echo ===================================================
echo      Kairos Intelligence System - Launcher
echo ===================================================
echo.
echo Tienes varias versiones de Python instaladas.
echo Selecciona la version que deseas utilizar:
echo.
echo 1. Python 3.9.7  (Compatible con LangChain)
echo 2. Python 3.13.2 (Recomendado)
echo 3. Python 3.12.8 (Compatible)
echo.

set /p choice="Ingresa el numero de tu eleccion (1-3): "

if "%choice%"=="1" (
    echo.
    echo Ejecutando con Python 3.9...
    echo.
    "C:\Program Files\Python39\python.exe" run_kairos_langchain.py
) else if "%choice%"=="2" (
    echo.
    echo Ejecutando con Python 3.13...
    echo.
    C:\Python313\python.exe run_kairos_langchain.py
) else if "%choice%"=="3" (
    echo.
    echo Ejecutando con Python 3.12...
    echo.
    C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe run_kairos_langchain.py
) else (
    echo.
    echo Opcion invalida. Por favor ejecuta el script nuevamente.
    echo.
    pause
    exit
)

pause
