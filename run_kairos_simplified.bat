@echo off
echo ===================================================
echo      Kairos Intelligence System - Version Simple
echo ===================================================
echo.

REM Verificar Python
python --version 2>NUL
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor, instale Python 3.8 o superior
    pause
    exit /b 1
)

REM Obtener directorio del script actual
cd /d %~dp0

REM Verificar dependencias
echo Verificando dependencias...
python -c "import PyQt6" 2>NUL
if errorlevel 1 (
    echo Instalando dependencias...
    cd ..
    call install.bat
    cd %~dp0
)

REM Verificar la fuente Inter
REG QUERY "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "Inter Regular (TrueType)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [AVISO] La fuente Inter no está instalada en el sistema.
    echo Para una mejor experiencia visual, instale la fuente desde:
    echo https://fonts.google.com/specimen/Inter
    echo.
    pause
)

REM Ejecutar la aplicación
echo.
echo Iniciando Kairos...
python run_kairos_simplified.py
if errorlevel 1 (
    echo.
    echo Error al ejecutar la aplicación
    pause
)
