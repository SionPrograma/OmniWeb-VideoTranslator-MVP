@echo off
setlocal
echo ==================================================
echo   OmniWeb VideoTranslator - Setup Python 3.11
echo ==================================================
echo.

:: Check for Python 3.11 using the Python Launcher
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.11 no esta instalado o no se encuentra en el PATH.
    echo Por favor, instala Python 3.11 desde python.org y asegúrate de marcar 'Add to PATH'.
    pause
    exit /b 1
)

echo [1/4] Creando entorno virtual .venv con Python 3.11...
py -3.11 -m venv .venv

echo [2/4] Activando entorno virtual...
call .venv\Scripts\activate

echo [3/4] Actualizando herramientas de instalacion (pip, setuptools, wheel)...
python -m pip install --upgrade pip setuptools wheel

echo [4/4] Instalando dependencias de requirements.txt...
echo Esto puede tardar varios minutos devido al peso de los modelos (PyTorch, Whisper, TTS)...
pip install -r requirements.txt

echo.
echo ==================================================
echo   INSTALACION COMPLETADA CON EXITO
echo ==================================================
echo Para iniciar el proyecto usa: run_backend_py311.bat
echo.
pause
