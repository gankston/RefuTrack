# RefuTrack - Utilidades y helpers
import logging
from datetime import datetime, timezone
from typing import Optional
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('refutrack.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def format_datetime_local(iso_string: str) -> str:
    """Convertir datetime ISO a formato local legible"""
    try:
        dt = datetime.fromisoformat(iso_string)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        dt_local = dt.astimezone()
        return dt_local.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return iso_string[:16].replace("T", " ") if iso_string else ""

def validate_sku(sku: str) -> tuple[bool, str]:
    """Validar formato de SKU"""
    if not sku or not sku.strip():
        return False, "SKU no puede estar vacío"
    
    sku = sku.strip().upper()
    
    # Permitir letras, números, guiones y guiones bajos
    if not re.match(r'^[A-Z0-9_-]+$', sku):
        return False, "SKU solo puede contener letras, números, guiones y guiones bajos"
    
    if len(sku) < 2:
        return False, "SKU debe tener al menos 2 caracteres"
    
    if len(sku) > 50:
        return False, "SKU no puede tener más de 50 caracteres"
    
    return True, sku

def validate_product_name(name: str) -> tuple[bool, str]:
    """Validar nombre de producto"""
    if not name or not name.strip():
        return False, "Nombre no puede estar vacío"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Nombre debe tener al menos 2 caracteres"
    
    if len(name) > 200:
        return False, "Nombre no puede tener más de 200 caracteres"
    
    return True, name

def validate_stock_value(value: str, field_name: str = "Stock") -> tuple[bool, int]:
    """Validar valor de stock"""
    try:
        stock = int(value) if value else 0
        if stock < 0:
            return False, f"{field_name} no puede ser negativo"
        if stock > 999999:
            return False, f"{field_name} no puede ser mayor a 999,999"
        return True, stock
    except ValueError:
        return False, f"{field_name} debe ser un número válido"

def sanitize_string(value: str, max_length: int = 500) -> str:
    """Sanitizar string de entrada"""
    if not value:
        return ""
    
    # Limpiar y truncar
    cleaned = value.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned

def get_current_timestamp() -> str:
    """Obtener timestamp actual en formato ISO"""
    return datetime.utcnow().isoformat()

def calculate_pagination(page: int, per_page: int, total: int) -> dict:
    """Calcular información de paginación"""
    total_pages = (total + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    prev_page = page - 1 if has_prev else None
    next_page = page + 1 if has_next else None
    
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_page': prev_page,
        'next_page': next_page
    }

class ValidationError(Exception):
    """Excepción para errores de validación"""
    pass

def log_user_action(action: str, details: str = "", user_ip: str = ""):
    """Registrar acción del usuario"""
    logger.info(f"Acción: {action} | Detalles: {details} | IP: {user_ip}")



