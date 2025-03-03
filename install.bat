@echo off
echo ===================================================
echo          Kairos - Instalacion de dependencias
echo ===================================================
echo.

REM Verificar Python
python --version 2>NUL
if errorlevel 1 (
    echo Error: Python no esta instalado o no esta en el PATH
    echo Por favor, instale Python 3.8 o superior
    pause
    exit /b 1
)

echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando/Actualizando dependencias UI...
python -m pip install --upgrade --no-cache-dir PyQt6==6.6.1 colour==0.1.5

echo.
echo Verificando instalacion PyQt6...
python -c "import PyQt6; print(f'PyQt6 version: {PyQt6.__version__}')" 2>NUL
if errorlevel 1 (
    echo Error: No se pudo importar PyQt6
    echo Intentando instalacion alternativa...
    python -m pip install --upgrade --no-cache-dir PyQt6-Qt6==6.6.1 PyQt6-sip==13.6.0
)

echo.
echo Verificando colour...
python -c "import colour; print('Colour: OK')" 2>NUL
if errorlevel 1 (
    echo Error: No se pudo importar colour
    echo Reintentando instalacion...
    python -m pip install --upgrade --no-cache-dir colour
)

echo.
echo Instalando dependencias LangChain...
python -m pip install --upgrade --no-cache-dir ^
    langchain-community==0.0.16 ^
    langchain==0.1.4 ^
    openai==1.10.0

echo.
echo Verificando todas las dependencias...
python -c "import sys; print(f'Python {sys.version}'); import PyQt6; import colour; print('Todas las dependencias instaladas correctamente.')"
if errorlevel 1 (
    echo.
    echo Error: Algunas dependencias no se instalaron correctamente
    echo Por favor, revise los mensajes de error anteriores
    pause
    exit /b 1
)

echo.
echo Instalacion completada exitosamente.
echo.
echo [INFO] Para una mejor experiencia visual, puede instalar la fuente Inter:
echo https://fonts.google.com/specimen/Inter
echo.
pause
