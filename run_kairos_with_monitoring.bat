@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo Kairos Intelligence System - Con Monitorización de Agentes
echo ===================================================

echo Este script ejecuta Kairos con la nueva funcionalidad de monitorización
echo de agentes integrada en la interfaz principal.

echo.
echo Selecciona la versión de Python para ejecutar Kairos:
echo 1. Python 3.13.2 (C:\Python313\python.exe)
echo 2. Python 3.12.8 (C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe)
echo 3. Python 3.9.7 (C:\Program Files\Python39\python.exe)

set /p choice=Ingresa el número de tu elección (1-3): 

if "%choice%"=="1" (
    set python_exe=C:\Python313\python.exe
) else if "%choice%"=="2" (
    set python_exe=C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe
) else if "%choice%"=="3" (
    set python_exe=C:\Program Files\Python39\python.exe
) else (
    echo Opción no válida. Usando Python 3.13.2 por defecto.
    set python_exe=C:\Python313\python.exe
)

echo.
echo Ejecutando Kairos con %python_exe%...
echo.

"%python_exe%" main.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error al ejecutar Kairos. Código de error: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Kairos ha finalizado.
pause
