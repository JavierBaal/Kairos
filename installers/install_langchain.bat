@echo off
echo ===================================================
echo      Kairos - Instalacion de dependencias LangChain
echo ===================================================
echo.

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar langchain y dependencias
pip install langchain-community==0.0.16 langchain==0.1.4 openai==1.10.0

echo.
echo Instalacion completada.
echo.
pause
