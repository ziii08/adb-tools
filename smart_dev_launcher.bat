@echo off
setlocal ENABLEDELAYEDEXPANSION
title 🚀 Smart Dev Launcher v3.5
color 0A

REM ========== CONFIG ==========
set BASE_DIR=\Path
set IP=192.168.0.101
set CACHE_FILE=%BASE_DIR%\.project_cache.txt

REM ========== CEK ARGUMENT ========== 
if "%1"=="--clear-cache" (
    echo 🔄 Menghapus project cache...
    if exist "%CACHE_FILE%" del "%CACHE_FILE%"
    echo ✅ Cache berhasil dihapus.
    echo.
    goto :menu
)

REM ========== TAMPIL MENU RESET ==========
:menu
echo ================================
echo     🚀 Smart Dev Launcher
echo ================================
echo [1] Jalankan Project
echo [2] Reset Project Cache
echo [3] Keluar
echo.

set /p menuChoice=👉 Pilih opsi: 

REM MENANGANI RESET CACHE
if "%menuChoice%"=="2" (
    echo 🔄 Menghapus project cache...
    if exist "%CACHE_FILE%" del "%CACHE_FILE%"
    echo ✅ Cache berhasil dihapus.
    echo.
    REM Setelah reset cache, langsung kembali ke menu
    goto :menu
)

REM KELUAR
if "%menuChoice%"=="3" (
    echo Terima kasih! 👋
    pause
    exit /b
)

REM ========== GUNAKAN CACHE JIKA ADA ==========
if exist "%CACHE_FILE%" (
    echo 💾 Membaca cache project...
    set /a count=0
    for /f "tokens=1,* delims=|" %%A in (%CACHE_FILE%) do (
        set /a count+=1
        set "project!count!=%%B"
        set "type!count!=%%A"
        echo [!count!] %%A: %%~nxB
    )
    goto :chooseProject
)

echo 🔍 Scan project sedang berlangsung...

set /a count=0
set "foundList="

REM ========== SCAN ==========
for /f "delims=" %%D in ('dir "%BASE_DIR%" /ad /b /s') do (
    set "current=%%~fD"

    REM SKIP SUBFOLDER JIKA SUDAH DITEMUKAN
    set "skip=false"
    for %%F in (!foundList!) do (
        echo !current! | find /i "%%~F" >nul
        if !errorlevel! == 0 set "skip=true"
    )
    if "!skip!" == "true" goto :continue

    REM FLUTTER
    if exist "%%D\pubspec.yaml" (
        if exist "%%D\lib\" (
            if exist "%%D\lib\main.dart" (
                set /a count+=1
                echo [!count!] Flutter: %%~fD
                set "project!count!=%%~fD"
                set "type!count!=flutter"
                set "foundList=!foundList! %%~fD"
                echo flutter|%%~fD>> "%CACHE_FILE%"
                goto :continue
            )
        )
    )

    REM REACT NATIVE
    if exist "%%D\package.json" (
        if exist "%%D\App.js" (
            if exist "%%D\android\" (
                if exist "%%D\index.js" (
                    set /a count+=1
                    echo [!count!] React Native: %%~fD
                    set "project!count!=%%~fD"
                    set "type!count!=react"
                    set "foundList=!foundList! %%~fD"
                    echo react|%%~fD>> "%CACHE_FILE%"
                    goto :continue
                )
            )
        )
    )

    :continue
)

if %count%==0 (
    echo ❌ Tidak ada project valid ditemukan.
    pause
    exit /b
)

:chooseProject
echo.
set /p choice=👉 Pilih nomor project: 

set "projectDir=!project%choice%!"
set "projectType=!type%choice%!"

echo.
echo ===============================
echo  🔌 Connecting via ADB Wi-Fi...
echo ===============================
adb connect %IP%
echo.

cd /d "!projectDir!"

if "!projectType!"=="flutter" (
    echo 🚀 Menjalankan Flutter project...
    flutter run
) else (
    echo 🚀 Menjalankan React Native project...
    npx react-native run-android
)

REM Kembali ke menu setelah menjalankan project
goto :menu
