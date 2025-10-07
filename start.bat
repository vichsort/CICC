@echo off

cd backend

call .\.venv\Scripts\activate.bat

start cmd /k "flask run"

cd ..\frontend

start cmd /k "npm run dev"

exit