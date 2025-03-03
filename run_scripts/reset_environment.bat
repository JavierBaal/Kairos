@echo off
echo ===================================================
echo      Kairos - Limpieza y Reinicio del Entorno
echo ===================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d %SCRIPT_DIR%\..

echo Verificando Python...
python --version 2>NUL
if errorlevel 1 (
    echo Error: Python no está instalado
    pause
    exit /b 1
)

echo.
echo Esta operación realizará las siguientes acciones:
echo  1. Limpiará la caché de pip
echo  2. Desinstalará y reinstalará las dependencias
echo  3. Eliminará archivos temporales y de caché
echo  4. Reinstalará el entorno desde cero
echo.
echo ADVERTENCIA: Esto no eliminará sus archivos de proyecto
echo pero sí reiniciará la configuración del entorno.
echo.

set /p CONFIRM="¿Desea continuar? (S/N): "
if /i "%CONFIRM%" neq "S" (
    echo Operación cancelada.
    pause
    exit /b 0
)

echo.
echo Limpiando caché de pip...
python -m pip cache purge

echo.
echo Desinstalando dependencias...
python -m pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip colour langchain langchain-community openai

echo.
echo Eliminando archivos temporales...
if exist "%TEMP%\kairos_temp" rd /s /q "%TEMP%\kairos_temp"
if exist "__pycache__" rd /s /q "__pycache__"
if exist "ui\__pycache__" rd /s /q "ui\__pycache__"
if exist "ui\components\__pycache__" rd /s /q "ui\components\__pycache__"
if exist "run_scripts\__pycache__" rd /s /q "run_scripts\__pycache__"
if exist "diagnostic_report.json" del /f /q "diagnostic_report.json"

echo.
echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Reinstalando dependencias...
call install.bat

echo.
echo Ejecutando diagnóstico...
cd run_scripts
python diagnostics.py
cd ..

echo.
echo ===================================================
echo Reinicio completado. Por favor, verifique el reporte 
echo de diagnóstico para asegurarse de que todo está
echo correctamente configurado.
echo ===================================================
echo.

pause
