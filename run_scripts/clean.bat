@echo off
echo ===================================================
echo      Kairos - Limpieza de Archivos Temporales
echo ===================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%\.."

echo Verificando archivos temporales...
echo.

REM Lista de directorios a limpiar
set "CLEAN_DIRS=__pycache__ build dist temp .temp .pytest_cache .coverage"

REM Lista de extensiones a limpiar
set "CLEAN_EXT=*.pyc *.pyo *.pyd *.spec *.log *.tmp *.qmlc *.jsc ~* *.bak *.swp"

REM Limpiar directorios
for %%d in (%CLEAN_DIRS%) do (
    if exist "%%d" (
        echo Eliminando directorio: %%d
        rd /s /q "%%d" 2>nul
    )
)

REM Limpiar archivos por extensión
for %%e in (%CLEAN_EXT%) do (
    echo Buscando: %%e
    del /s /q "%%e" 2>nul
)

REM Limpiar __pycache__ en subdirectorios
for /d /r %%d in (*) do (
    if "%%~nxd"=="__pycache__" (
        echo Eliminando: %%d
        rd /s /q "%%d"
    )
)

REM Eliminar archivos de diagnóstico antiguos
if exist "run_scripts\diagnostic_report.json" (
    echo Eliminando reporte de diagnóstico antiguo...
    del /f /q "run_scripts\diagnostic_report.json"
)

REM Verificar y limpiar directorios específicos
for %%d in (ui models run_scripts) do (
    if exist "%%d\__pycache__" (
        echo Limpiando caché en: %%d
        rd /s /q "%%d\__pycache__"
    )
)

REM Limpiar caché de PyQt si existe
if exist ".qt" rd /s /q ".qt"
if exist ".qmake.stash" del /f /q ".qmake.stash"

echo.
echo Limpieza completada.
echo Se han eliminado archivos temporales y cachés.
echo.

REM Mostrar espacio recuperado (si es posible)
if exist "C:\Windows\System32\wbem\wmic.exe" (
    echo Espacio en disco actual:
    wmic logicaldisk where "DeviceID='%~d0'" get size,freespace /format:value
)

echo.
echo Para una limpieza completa del entorno, ejecute:
echo run_scripts\reset_environment.bat
echo.
pause
