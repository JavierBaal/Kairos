@echo off
echo ===================================================
echo      Kairos Intelligence System - Instalador
echo ===================================================
echo.
echo Este script instalara las dependencias necesarias para Kairos.
echo.
echo Selecciona la version de Python para instalar las dependencias:
echo.
echo 1. Python 3.13.2 (C:\Python313\python.exe)
echo 2. Python 3.12.8 (C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe)
echo.

set /p choice="Ingresa el numero de tu eleccion (1-2): "

if "%choice%"=="1" (
    set PYTHON_PATH=C:\Python313\python.exe
    echo.
    echo Instalando dependencias con Python 3.13...
) else if "%choice%"=="2" (
    set PYTHON_PATH=C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe
    echo.
    echo Instalando dependencias con Python 3.12...
) else (
    echo.
    echo Opcion invalida. Por favor ejecuta el script nuevamente.
    echo.
    pause
    exit
)

echo.
echo Paso 1: Instalando PyQt6 y PyYAML...
%PYTHON_PATH% -m pip install PyQt6 pyyaml
if %ERRORLEVEL% NEQ 0 (
    echo Error al instalar PyQt6 y PyYAML.
    pause
    exit
)

echo.
echo Paso 2: Verificando si Rust esta instalado...
where rustc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Rust no esta instalado. Se recomienda instalar Rust para compilar dependencias de CrewAI.
    echo Puedes instalar Rust desde: https://rustup.rs/
    echo.
    echo Presiona cualquier tecla para intentar instalar CrewAI sin Rust...
    pause >nul
) else (
    echo Rust esta instalado. Continuando con la instalacion...
)

echo.
echo Paso 3: Instalando CrewAI...
echo (Este proceso puede tardar varios minutos)
%PYTHON_PATH% -m pip install crewai
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error al instalar CrewAI. Intentando instalar sin algunas dependencias...
    echo.
    %PYTHON_PATH% -m pip install crewai --no-deps
    if %ERRORLEVEL% NEQ 0 (
        echo Error al instalar CrewAI incluso sin dependencias.
        echo.
        echo Puedes intentar ejecutar Kairos en modo basico, que no requiere CrewAI.
    ) else (
        echo CrewAI instalado parcialmente (sin todas las dependencias).
        echo Algunas funcionalidades pueden no estar disponibles.
    )
) else (
    echo CrewAI instalado correctamente.
)

echo.
echo Instalacion completada. Puedes ejecutar Kairos ahora.
echo.
pause
