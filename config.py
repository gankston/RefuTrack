# RefuTrack - Configuración de la aplicación
import os
from datetime import datetime

class Config:
    """Configuración base de la aplicación"""
    
    # Información de la aplicación
    APP_TITLE = "RefuTrack"
    APP_VERSION = "2.0.0"
    
    # Configuración de base de datos
    APP_DIR = os.path.join(os.getenv("LOCALAPPDATA") or os.path.expanduser("~"), "RefuTrack")
    DB_PATH = os.environ.get("INV_DB", os.path.join(APP_DIR, "inventario.db"))
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", f"refutrack-{datetime.now().strftime('%Y%m%d')}")
    
    # Configuración de servidor
    HOST = "127.0.0.1"
    PORT = 5000
    
    # Configuración de UI
    ITEMS_PER_PAGE = 50
    
    # Configuración de seguridad
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    @staticmethod
    def init_app():
        """Inicializar directorios necesarios"""
        os.makedirs(Config.APP_DIR, exist_ok=True)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}



