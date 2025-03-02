@echo off
echo ===================================================
echo      Kairos Intelligence System - Launcher
echo ===================================================
echo.

REM Intentar ejecutar con Python disponible localmente
echo Ejecutando Kairos con Python...
echo.

REM Intentar usar Python del sistema (asumiendo que está en el PATH)
python main.py

REM Si el comando anterior falla, intentar con rutas específicas
if %ERRORLEVEL% NEQ 0 (
    echo Intentando con rutas alternativas...
    
    if exist "C:\Python313\python.exe" (
        echo Ejecutando con Python 3.13...
        "C:\Python313\python.exe" main.py
    ) else if exist "C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe" (
        echo Ejecutando con Python 3.12...
        "C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe" main.py
    ) else if exist "C:\Program Files\Python39\python.exe" (
        echo Ejecutando con Python 3.9...
        "C:\Program Files\Python39\python.exe" main.py
    ) else (
        echo No se pudo encontrar una instalación de Python.
        echo Por favor, asegúrate de que Python esté instalado correctamente.
        pause
        exit /b 1
    )
)

echo.
echo Presiona cualquier tecla para salir...
pause > nul
