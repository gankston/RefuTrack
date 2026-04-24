@echo off
echo ========================================
echo    COMPILANDO REFUTRACK
echo ========================================
echo.

REM Activar entorno virtual
echo [1/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    echo Asegurate de que existe la carpeta venv\
    pause
    exit /b 1
)

REM Limpiar compilaciones anteriores
echo [2/4] Limpiando compilaciones anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Verificar archivos necesarios
echo [3/4] Verificando archivos necesarios...
if not exist RefuTrack_complete.spec (
    echo ERROR: No se encontro RefuTrack_complete.spec
    pause
    exit /b 1
)
if not exist refu.ico (
    echo ERROR: No se encontro refu.ico
    pause
    exit /b 1
)

REM Compilar
echo [4/4] Compilando ejecutable...
venv\Scripts\pyinstaller.exe RefuTrack_complete.spec --clean --noconfirm

REM Verificar resultado
echo.
if exist "dist\RefuTrack.exe" (
    echo ========================================
    echo    COMPILACION EXITOSA
    echo ========================================
    echo.
    echo Ejecutable creado en: dist\RefuTrack.exe
    echo Tamaño: 
    dir "dist\RefuTrack.exe"
    echo.
    echo ¿Quieres probar el ejecutable ahora? (S/N)
    set /p test=
    if /i "%test%"=="S" (
        echo Abriendo RefuTrack...
        start "" "dist\RefuTrack.exe"
    )
) else (
    echo ========================================
    echo    ERROR EN LA COMPILACION
    echo ========================================
    echo.
    echo No se pudo crear el ejecutable
    echo Revisa los mensajes de error anteriores
    pause
    exit /b 1
)

echo.
echo Presiona cualquier tecla para continuar...
pause >nul
