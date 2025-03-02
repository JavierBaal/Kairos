@echo off
echo ===================================================
echo      Kairos Intelligence System - Instalador LangChain
echo ===================================================
echo.
echo Este script instalara las dependencias de LangChain para Kairos.
echo.
echo Selecciona la version de Python para instalar las dependencias:
echo.
echo 1. Python 3.13.2 (C:\Python313\python.exe)
echo 2. Python 3.12.8 (C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe)
echo 3. Python 3.9.7 (C:\Program Files\Python39\python.exe)
echo.

set /p choice="Ingresa el numero de tu eleccion (1-3): "

if "%choice%"=="1" (
    set PYTHON_PATH=C:\Python313\python.exe
    echo.
    echo Instalando dependencias con Python 3.13...
) else if "%choice%"=="2" (
    set PYTHON_PATH=C:\Users\webma\AppData\Local\Programs\Python\Python312\python.exe
    echo.
    echo Instalando dependencias con Python 3.12...
) else if "%choice%"=="3" (
    set PYTHON_PATH=C:\Program Files\Python39\python.exe
    echo.
    echo Instalando dependencias con Python 3.9...
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
echo Paso 2: Instalando LangChain y sus dependencias...
echo (Este proceso puede tardar varios minutos)
%PYTHON_PATH% -m pip install -r ..\config_files\requirements_langchain.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error al instalar LangChain. Intentando instalar los paquetes individualmente...
    echo.
    %PYTHON_PATH% -m pip install langchain
    %PYTHON_PATH% -m pip install langchain-openai
    %PYTHON_PATH% -m pip install langchain-community
    %PYTHON_PATH% -m pip install langchain-core
    
    if %ERRORLEVEL% NEQ 0 (
        echo Error al instalar LangChain incluso individualmente.
        echo.
        echo Por favor, revisa los mensajes de error e intenta resolver los problemas.
    ) else (
        echo LangChain instalado correctamente.
    )
) else (
    echo LangChain instalado correctamente.
)

echo.
echo Instalacion completada. Puedes ejecutar Kairos con LangChain ahora.
echo.
pause
