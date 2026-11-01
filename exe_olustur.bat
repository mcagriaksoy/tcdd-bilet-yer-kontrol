@echo off
setlocal EnableExtensions

REM Build the single-file web UI executable with all packages and data.
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

set "ENTRY=%ROOT%\start_ui.py"
set "APP_NAME=tcdd-bilet-botu"
set "DIST_DIR=%ROOT%\dist"
set "BUILD_DIR=%ROOT%\build"
set "SPEC_FILE=%ROOT%\%APP_NAME%.spec"
set "VERSION_FILE=%ROOT%\version.txt"

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
    echo HATA: dist klasoru silinemedi. Uygulama calisiyor olabilir.
    echo Lutfen calisan tcdd-bilet-botu.exe surecini kapatip tekrar deneyin.
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
    --collect-all backend ^
    --collect-all webview ^
    --collect-submodules selenium ^
    --collect-submodules webdriver_manager ^
    --hidden-import webview.platforms.edgechromium ^
    --hidden-import webview.platforms.winforms ^
    --hidden-import clr ^
    --add-data "%ROOT%\webapp\templates;webapp\templates" ^
    --add-data "%ROOT%\webapp\static;webapp\static" ^
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
if exist "%ROOT%\version.txt" (
    copy /Y "%ROOT%\version.txt" "%DIST_DIR%\version.txt" >nul
)

echo.
echo Basarili: %DIST_DIR%\%APP_NAME%.exe
echo Not: msedgedriver.exe dist klasorune kopyalandiysa exe ile ayni klasorde kalmali.
pause
exit /b 0
