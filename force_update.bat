@echo off
title 🧠 Sebas AI - Forzar subida de carpetas vacías con .gitkeep

setlocal
set "DIR=%cd%"

for %%F in (
    "scripts"
    "src"
    "docs"
    "logs"
    "output"
    "assets"
    "plantillas"
) do (
    if not exist "%DIR%\%%F\.gitkeep" (
        echo.>"%DIR%\%%F\.gitkeep"
        echo ✅ Añadido .gitkeep a %%F
    )
)

pause