# RefuTrack 🔧

[Español](#español) | [English](#english)

---

## Español

Sistema ligero de gestión de inventario y stock diseñado para funcionar como una aplicación de escritorio moderna utilizando tecnologías web.

### 🚀 Características
- **Control de Stock**: Gestión de productos mediante SKU, nombre y descripción.
- **Alertas de Stock Bajo**: Indicadores visuales automáticos cuando un producto cae por debajo del mínimo.
- **Registro de Movimientos**: Historial detallado de ingresos y salidas con destino y notas.
- **Interfaz de Escritorio**: Ejecutable nativo con ventana dedicada (sin necesidad de navegador externo).
- **Exportación**: Generación de reportes en formato CSV.
- **Base de Datos Portable**: SQLite configurado en la carpeta del usuario para evitar problemas de permisos.

### 🛠️ Stack Tecnológico
- **Backend**: Python + Flask
- **Frontend**: Bootstrap 5 + Inter Font
- **Desktop Wrapper**: PyWebView + Waitress
- **Base de Datos**: SQLite

### 📂 Estructura del Proyecto
- `app.py`: Lógica central del servidor Flask.
- `run_gui.py`: Script de inicio de la interfaz gráfica.
- `database.py`: Gestión del esquema y conexión a la BD.
- `templates/`: Plantillas HTML dinámicas.

---

## English

A lightweight inventory and stock management system designed to run as a modern desktop application using web technologies.

### 🚀 Key Features
- **Stock Control**: Product management via SKU, name, and description.
- **Low Stock Alerts**: Automatic visual indicators when a product drops below its minimum level.
- **Movement Logs**: Detailed history of ins and outs with destination and notes.
- **Desktop Interface**: Native executable with a dedicated window (no external browser required).
- **Exporting**: CSV report generation.
- **Portable Database**: SQLite configured in the user's local folder to avoid permission issues.

### 🛠️ Tech Stack
- **Backend**: Python + Flask
- **Frontend**: Bootstrap 5 + Inter Font
- **Desktop Wrapper**: PyWebView + Waitress
- **Database**: SQLite

### 📂 Project Structure
- `app.py`: Core Flask server logic.
- `run_gui.py`: Graphical interface startup script.
- `database.py`: Database schema and connection management.
- `templates/`: Dynamic HTML templates.

---
Developed with ❤️ by gankston
