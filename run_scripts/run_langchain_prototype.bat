@echo off
echo ===================================================
echo      Kairos Intelligence System - Prototipo LangChain
echo ===================================================
echo.
echo Este script ejecutara el prototipo de Kairos con LangChain.
echo.
echo Selecciona la version de Python para ejecutar el prototipo:
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
echo Antes de ejecutar el prototipo, necesitas configurar tu API key de OpenAI.
echo.
set /p api_key="Ingresa tu API key de OpenAI (o presiona Enter para omitir): "

if not "%api_key%"=="" (
    echo.
    echo Configurando API key...
    set OPENAI_API_KEY=%api_key%
)

echo.
echo Ejecutando prototipo de LangChain...
echo.

%PYTHON_PATH% langchain_prototype/agent_example.py

echo.
echo Ejecucion completada.
echo.
pause
