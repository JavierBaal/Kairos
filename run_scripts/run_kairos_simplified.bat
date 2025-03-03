@echo off
echo ===================================================
echo      Kairos Intelligence System - Version Simple
echo ===================================================
echo.

REM Obtener directorio del script actual y guardarlo
set "SCRIPT_DIR=%~dp0"

REM Cambiar al directorio del script
cd /d "%SCRIPT_DIR%"

REM Ejecutar diagnóstico
echo Ejecutando diagnóstico del sistema...
python diagnostics.py
if errorlevel 1 (
    echo.
    echo Error: El diagnóstico ha detectado problemas
    echo Por favor, revise el reporte generado para más detalles
    pause
    exit /b 1
)

REM Ejecutar verificación del sistema
echo.
echo Verificando componentes del sistema...
python check_system.py
if errorlevel 1 (
    echo.
    echo Error: La verificación del sistema ha fallado
    echo Ejecute install.bat para instalar las dependencias necesarias
    pause
    exit /b 1
)

REM Verificar la fuente Inter (solo informativo)
REG QUERY "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "Inter Regular (TrueType)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] La fuente Inter no está instalada.
    echo Se usará la fuente del sistema como alternativa.
    echo Para una mejor experiencia visual, puede instalar Inter desde:
    echo https://fonts.google.com/specimen/Inter
    echo.
    timeout /t 2 >nul
)

REM Volver al directorio raíz del proyecto
cd ..

REM Ejecutar la aplicación
echo.
echo [%time%] Iniciando Kairos...
python run_scripts/run_kairos_simplified.py
if errorlevel 1 (
    echo.
    echo Error al ejecutar la aplicación
    echo.
    echo Para más detalles, revise:
    echo 1. El reporte de diagnóstico en: run_scripts\diagnostic_report.json
    echo 2. Los mensajes de error anteriores
    echo.
    echo Para solucionar problemas:
    echo 1. Ejecute run_scripts\reset_environment.bat para reiniciar el entorno
    echo 2. Consulte docs\troubleshooting.md para más ayuda
    pause
    exit /b 1
)

REM Mensaje de cierre exitoso
echo.
echo Aplicación cerrada correctamente.
echo Los registros y diagnósticos están disponibles en:
echo %SCRIPT_DIR%diagnostic_report.json
echo.
pause
