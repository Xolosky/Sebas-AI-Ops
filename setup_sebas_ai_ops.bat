@echo off
setlocal
title 🧠 Sebas AI Ops - Setup Inicial

set "ROOT=%cd%"

:: Crear carpetas principales
mkdir "%ROOT%\src"
mkdir "%ROOT%\scripts"
mkdir "%ROOT%\plantillas"
mkdir "%ROOT%\docs"
mkdir "%ROOT%\logs"
mkdir "%ROOT%\assets"
mkdir "%ROOT%\output"

:: Crear archivos base
echo # Sebas-AI-Ops > "%ROOT%\README.md"
echo requests > "%ROOT%\requirements.txt"
echo """Archivo de configuración para constantes globales.""" > "%ROOT%\src\sebas_ai_config.py"
echo """Log del sistema Sebas AI Ops.""" > "%ROOT%\logs\log.txt"
echo """Notas y documentación del proyecto.""" > "%ROOT%\docs\notas.txt"

:: Gitignore extendido
(
echo __pycache__/
echo *.pyc
echo *.log
echo /output
echo .env
echo .vscode/
) > "%ROOT%\.gitignore"

echo.
echo ✅ Estructura creada en %ROOT%
echo 🔁 Abre todo en VS Code y comienza a trabajar en modo IA.
pause
