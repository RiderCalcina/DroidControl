@echo off
title DroidControl - Launcher
echo Iniciando aplicacion...
python DroidControl.py
if %errorlevel% neq 0 (
    echo.
    echo Error al iniciar. Asegurese de tener Python instalado y las dependencias.
    echo Ejecute: pip install -r requirements.txt
    pause
)
