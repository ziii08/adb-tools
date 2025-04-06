@echo off
echo 🔍 Mengambil IP address dari device melalui ADB...

REM Jalankan perintah adb untuk mengambil IP dari HP
for /f "tokens=1-10 delims= " %%a in ('adb shell ip route') do (
    set IP=%%g
    goto connect
)

:connect
echo 🌐 IP Address ditemukan: %IP%
echo 🔌 Mengaktifkan ADB WiFi (port 5555)...
adb tcpip 5555
timeout /t 2 >nul

echo 🔗 Menghubungkan ke %IP%:5555 ...
adb connect %IP%:5555

pause
