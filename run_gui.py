#!/usr/bin/env python3
# RefuTrack - Script de inicio optimizado
import threading
import time
import logging
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
import webview
from app import create_app
from config import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_server():
    """Iniciar servidor Flask con Waitress"""
    try:
        app = create_app()
        logger.info(f"Iniciando servidor en http://{Config.HOST}:{Config.PORT}")
        serve(app, host=Config.HOST, port=Config.PORT, threads=4)
    except Exception as e:
        logger.error(f"Error iniciando servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    try:
        # Inicializar directorios
        Config.init_app()
        
        # Iniciar servidor en hilo separado
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Esperar a que el servidor esté listo
        time.sleep(2)
        
        # Crear ventana de aplicación
        window_url = f"http://{Config.HOST}:{Config.PORT}"
        logger.info(f"Abriendo aplicación en: {window_url}")
        
        webview.create_window(
            title="RefuTrack - Gestión de Inventario",
            url=window_url,
            width=1200,
            height=800,
            resizable=True,
            fullscreen=False
        )
        
        # Iniciar la interfaz
        webview.start(debug=False)
        
    except KeyboardInterrupt:
        logger.info("Aplicación cerrada por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
