@echo off
set /p IP=Masukkan IP Address HP kamu: 
set PORT=5555

echo 🔌 Menghubungkan ke %IP%:%PORT% ...
adb connect %IP%:%PORT%
pause
