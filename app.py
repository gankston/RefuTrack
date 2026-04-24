# RefuTrack - Aplicación optimizada de gestión de inventario
from flask import Flask, request, redirect, url_for, Response, render_template, flash, abort
from werkzeug.exceptions import BadRequest
import logging
from datetime import datetime

from config import config, Config
from database import db_manager
from utils import (
    validate_sku, validate_product_name, validate_stock_value, 
    sanitize_string, get_current_timestamp, format_datetime_local,
    log_user_action, ValidationError
)

logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configurar logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    
    # Inicializar directorios
    Config.init_app()
    
    # Registrar blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error interno: {error}")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        flash(str(error), 'error')
        return redirect('/productos')
    
    @app.errorhandler(BadRequest)
    def bad_request(error):
        flash('Solicitud inválida', 'error')
        return redirect('/productos')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host=Config.HOST, port=Config.PORT)
