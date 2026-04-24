# 🚀 RefuTrack - Instrucciones para Crear Instalador

## 📋 Archivos Necesarios

Esta carpeta contiene todos los archivos esenciales para crear el instalador de RefuTrack:

### Archivos Principales:
- `app.py` - Aplicación Flask principal
- `config.py` - Configuración de la aplicación
- `database.py` - Gestión de base de datos SQLite
- `routes.py` - Rutas y lógica de la aplicación
- `utils.py` - Funciones de utilidad y validación
- `run_gui.py` - Script de inicio con interfaz gráfica
- `requirements.txt` - Dependencias de Python

### Archivos de Compilación:
- `RefuTrack_complete.spec` - Especificación de PyInstaller
- `refu.ico` - Icono de la aplicación
- `version_info.txt` - Información de versión

### Plantillas HTML:
- `templates/` - Carpeta con todas las plantillas HTML
- `templates/base.html` - Plantilla base
- `templates/productos/` - Plantillas para gestión de productos
- `templates/errors/` - Plantillas de páginas de error

### Entorno Virtual:
- `venv/` - Entorno virtual de Python con todas las dependencias

---

## 🛠️ Pasos para Crear el Instalador

### Paso 1: Verificar Entorno Virtual
```bash
# Activar el entorno virtual
venv\Scripts\activate

# Verificar que PyInstaller esté instalado
pip list | findstr pyinstaller
```

### Paso 2: Compilar el Ejecutable
```bash
# Compilar usando la especificación completa
venv\Scripts\pyinstaller.exe RefuTrack_complete.spec --clean --noconfirm
```

### Paso 3: Verificar el Ejecutable
```bash
# El ejecutable se creará en:
dist\RefuTrack.exe

# Probar que funciona
dist\RefuTrack.exe
```

### Paso 4: Crear Instalador MSI (Opcional)
Si tienes Inno Setup instalado, puedes crear un instalador MSI:

```bash
# Crear archivo .iss para Inno Setup
# (Ver sección de Inno Setup más abajo)
```

---

## 📦 Crear Instalador MSI con Inno Setup

### Instalar Inno Setup:
1. Descargar desde: https://jrsoftware.org/isinfo.php
2. Instalar con configuración predeterminada

### Crear Script de Inno Setup:
Crear archivo `RefuTrack.iss`:

```ini
[Setup]
AppName=RefuTrack
AppVersion=1.0
AppPublisher=Tu Empresa
AppPublisherURL=https://tu-sitio.com
AppSupportURL=https://tu-sitio.com/support
AppUpdatesURL=https://tu-sitio.com/updates
DefaultDirName={autopf}\RefuTrack
DefaultGroupName=RefuTrack
AllowNoIcons=yes
LicenseFile=
OutputDir=installer
OutputBaseFilename=RefuTrack-Setup
SetupIconFile=refu.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\RefuTrack.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "refu.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\RefuTrack"; Filename: "{app}\RefuTrack.exe"; IconFilename: "{app}\refu.ico"
Name: "{group}\{cm:UninstallProgram,RefuTrack}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\RefuTrack"; Filename: "{app}\RefuTrack.exe"; IconFilename: "{app}\refu.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\RefuTrack.exe"; Description: "{cm:LaunchProgram,RefuTrack}"; Flags: nowait postinstall skipifsilent
```

### Compilar el Instalador:
1. Abrir Inno Setup Compiler
2. Abrir el archivo `RefuTrack.iss`
3. Hacer clic en "Build" → "Compile"
4. El instalador se creará en la carpeta `installer/`

---

## 🔧 Scripts de Automatización

### Script para Compilar Todo (build.bat):
```batch
@echo off
echo Compilando RefuTrack...

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Limpiar compilaciones anteriores
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Compilar
venv\Scripts\pyinstaller.exe RefuTrack_complete.spec --clean --noconfirm

REM Verificar resultado
if exist dist\RefuTrack.exe (
    echo ¡Compilacion exitosa!
    echo Ejecutable creado en: dist\RefuTrack.exe
) else (
    echo ¡Error en la compilacion!
    pause
    exit /b 1
)

pause
```

### Script para Crear Instalador MSI (build_installer.bat):
```batch
@echo off
echo Creando instalador MSI...

REM Primero compilar el ejecutable
call build.bat

REM Verificar que Inno Setup esté instalado
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo Error: Inno Setup no encontrado
    echo Instala Inno Setup desde: https://jrsoftware.org/isinfo.php
    pause
    exit /b 1
)

REM Compilar instalador
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" RefuTrack.iss

echo ¡Instalador creado exitosamente!
pause
```

---

## 📋 Lista de Verificación

### Antes de Compilar:
- [ ] Entorno virtual activado
- [ ] Todas las dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `RefuTrack_complete.spec` presente
- [ ] Icono `refu.ico` presente
- [ ] Carpeta `templates/` completa

### Después de Compilar:
- [ ] Ejecutable `dist\RefuTrack.exe` creado
- [ ] Aplicación se abre correctamente
- [ ] Formulario de crear producto funciona
- [ ] Base de datos se crea automáticamente
- [ ] Todas las funcionalidades operativas

### Para el Instalador:
- [ ] Inno Setup instalado
- [ ] Script `RefuTrack.iss` creado
- [ ] Instalador MSI generado
- [ ] Instalador se ejecuta en otra PC
- [ ] Aplicación funciona después de instalar

---

## 🚨 Solución de Problemas

### Error: "No module named 'waitress'"
```bash
venv\Scripts\activate
pip install waitress
```

### Error: "No module named 'webview'"
```bash
venv\Scripts\activate
pip install pywebview
```

### Error: PyInstaller no encontrado
```bash
venv\Scripts\activate
pip install pyinstaller
```

### Error: "The view function did not return a valid response"
- Verificar que todas las rutas tengan `return` statements
- Revisar `routes.py` línea por línea

### Error: "Internal Server Error"
- Verificar que la base de datos tenga el esquema correcto
- Revisar `database.py` y `config.py`

### El ejecutable no funciona:
1. Verificar que `RefuTrack_complete.spec` incluya todos los archivos
2. Recompilar con `--clean --noconfirm`
3. Probar el ejecutable en la misma PC

---

## 📁 Estructura Final de Archivos

```
C:\App Py\
├── app.py                    # Aplicación principal
├── config.py                 # Configuración
├── database.py               # Base de datos
├── routes.py                 # Rutas
├── utils.py                  # Utilidades
├── run_gui.py                # Script de inicio
├── requirements.txt          # Dependencias
├── RefuTrack_complete.spec   # Especificación PyInstaller
├── refu.ico                  # Icono
├── version_info.txt          # Información de versión
├── templates/                # Plantillas HTML
│   ├── base.html
│   ├── productos/
│   └── errors/
├── venv/                     # Entorno virtual
├── dist/                     # Ejecutable compilado
│   └── RefuTrack.exe
└── INSTRUCCIONES_INSTALADOR.md  # Este archivo
```

---

## 🎯 Resumen Rápido

**Para compilar rápidamente:**
1. `venv\Scripts\activate`
2. `venv\Scripts\pyinstaller.exe RefuTrack_complete.spec --clean --noconfirm`
3. Probar `dist\RefuTrack.exe`

**Para crear instalador:**
1. Instalar Inno Setup
2. Crear `RefuTrack.iss`
3. Compilar con Inno Setup
4. Distribuir el MSI

¡RefuTrack está listo para distribuir! 🚀
