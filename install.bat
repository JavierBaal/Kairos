@echo off
echo ===================================================
echo      Kairos Intelligence System - Instalador
echo ===================================================
echo.
echo Este script es un acceso directo para instalar las dependencias de Kairos.
echo.
echo Selecciona la versión que deseas instalar:
echo.
echo 1. Kairos con LangChain (recomendado)
echo 2. Kairos con CrewAI (original)
echo.

set /p choice="Ingresa el número de tu elección (1-2): "

if "%choice%"=="1" (
    echo.
    echo Instalando Kairos con LangChain...
    echo.
    cd installers
    call install_langchain.bat
    cd ..
) else if "%choice%"=="2" (
    echo.
    echo Instalando Kairos con CrewAI...
    echo.
    cd installers
    call install_dependencies.bat
    cd ..
) else (
    echo.
    echo Opción inválida. Por favor ejecuta el script nuevamente.
    echo.
    pause
    exit
)
