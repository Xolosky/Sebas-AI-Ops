@echo off
setlocal
title 🚀 Sebas AI - Git Auto Push

:: Pedir mensaje de commit
set /p COMMIT_MSG=📝 Ingresa mensaje de commit: 

echo 🔄 Añadiendo cambios...
git add .

echo 🧠 Realizando commit...
git commit -m "%COMMIT_MSG%"

echo 🚀 Enviando a GitHub...
git push origin main

echo ✅ Push completado con éxito.
pause
