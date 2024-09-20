@echo off
echo ------------------SISTEMA COOHOBIENESTAR TASAS------------------
echo --------------------------EJECUTANDO----------------------------
echo.
C:
call Users/JUANJO/.envs/env_coohobienestar/Scripts/activate
D:
echo.
echo ---------PARA APAGAR EL SERVICIO APRETE Ctrl + C----------------
echo.
py manage.py runserver 192.168.0.100:8000
pause