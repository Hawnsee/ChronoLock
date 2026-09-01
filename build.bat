@echo off
echo [*] Instalando dependencias (customtkinter, pyinstaller, etc)...
pip install -r requirements.txt

echo.
echo [*] Compilando ejecutable con PyInstaller...
pyinstaller --noconsole --onefile --name ChronoLock app.py

echo.
echo ========================================================
echo [+] COMPILACION FINALIZADA.
echo [+] El ejecutable ChronoLock.exe esta en la carpeta 'dist'
echo ========================================================
pause
