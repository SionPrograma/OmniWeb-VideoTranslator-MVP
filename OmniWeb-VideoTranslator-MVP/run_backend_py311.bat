@echo off
echo ==================================================
echo   OmniWeb VideoTranslator - Starting Backend (3.11)
echo ==================================================
echo.

:: Check if the environment exists
if not exist .venv\Scripts\activate (
    echo [ERROR] El entorno virtual no existe. Por favor, ejecuta primero setup_env_py311.bat
    pause
    exit /b 1
)

echo [1/3] Activando entorno virtual (.venv)...
call .venv\Scripts\activate

echo [2/3] Cambiando al directorio del backend...
cd backend

echo [3/3] Ejecutando el servidor FastAPI con Python 3.11...
python -m app.main

echo.
pause
