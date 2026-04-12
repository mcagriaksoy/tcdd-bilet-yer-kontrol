@echo off
setlocal EnableExtensions

REM Build Start UI launcher as a standalone EXE with all packages/data.
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

set "ENTRY=%ROOT%\start_ui.py"
set "APP_NAME=start_ui"
set "DIST_DIR=%ROOT%\dist"
set "BUILD_DIR=%ROOT%\build"
set "SPEC_FILE=%ROOT%\%APP_NAME%.spec"
set "VERSION_FILE=%ROOT%\desktop_app\version.txt"

echo [1/4] Proje dizini: %ROOT%

if not exist "%ENTRY%" (
    echo HATA: Giris dosyasi bulunamadi: %ENTRY%
    pause
    exit /b 1
)

where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo HATA: PyInstaller bulunamadi. Once su komutu calistirin:
    echo   python -m pip install pyinstaller
    pause
    exit /b 1
)

echo [2/4] Eski build ciktilari temizleniyor...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%SPEC_FILE%" del /q "%SPEC_FILE%"

if exist "%DIST_DIR%" (
    echo HATA: dist klasoru silinemedi. start_ui.exe calisiyor olabilir.
    echo Lutfen calisan start_ui.exe surecini kapatip tekrar deneyin.
    pause
    exit /b 1
)
if exist "%BUILD_DIR%" (
    echo HATA: build klasoru silinemedi. Dosya kilidi olabilir.
    pause
    exit /b 1
)

echo [3/4] EXE olusturuluyor...
pyinstaller --noconfirm --clean --windowed --onefile ^
    --name "%APP_NAME%" ^
    --icon "%ROOT%\icon.ico" ^
    --version-file "%VERSION_FILE%" ^
    --collect-all webapp ^
    --collect-all desktop_app ^
    --collect-all backend ^
    --collect-submodules selenium ^
    --collect-submodules webdriver_manager ^
    --hidden-import tkinter ^
    --hidden-import tkcalendar ^
    --add-data "%ROOT%\webapp\templates;webapp\templates" ^
    --add-data "%ROOT%\webapp\static;webapp\static" ^
    --add-data "%ROOT%\desktop_app\icon.ico;desktop_app" ^
    --add-data "%ROOT%\desktop_app\default-green.png;desktop_app" ^
    --add-data "%ROOT%\icon.ico;." ^
    "%ENTRY%"

if errorlevel 1 (
    echo HATA: PyInstaller islemi basarisiz oldu.
    pause
    exit /b 1
)

echo [4/4] Runtime dosyalari kopyalaniyor...
if exist "%ROOT%\msedgedriver.exe" (
    copy /Y "%ROOT%\msedgedriver.exe" "%DIST_DIR%\msedgedriver.exe" >nul
)
if exist "%ROOT%\desktop_app\version.txt" (
    copy /Y "%ROOT%\desktop_app\version.txt" "%DIST_DIR%\version.txt" >nul
)

echo.
echo Basarili: %DIST_DIR%\%APP_NAME%.exe
echo Not: msedgedriver.exe dist klasorune kopyalandiysa exe ile ayni klasorde kalmali.
pause
exit /b 0
