@echo off
echo [*] Instalando dependencias (customtkinter, pyinstaller, etc)...
pip install -r requirements.txt

echo.
echo [*] Compilando ejecutable con PyInstaller (Icono y Metadata de Version)...
pyinstaller --clean --noconsole --onefile --icon=icon.ico --version-file=version_info.txt --name ChronoLock app.py

echo.
echo ========================================================
echo [+] COMPILACION FINALIZADA.
echo [+] El ejecutable ChronoLock.exe esta en la carpeta 'dist'
echo ========================================================
pause
