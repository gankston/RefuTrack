# RefuTrack - Rutas de la aplicación
from flask import Blueprint, request, redirect, url_for, render_template, flash, Response, jsonify
import logging
from datetime import datetime

from database import db_manager
from utils import (
    validate_sku, validate_product_name, validate_stock_value,
    sanitize_string, format_datetime_local, log_user_action,
    ValidationError
)

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    """Página principal - redirige a lista de productos"""
    return redirect('/productos')

@main_bp.route("/productos")
def lista_productos():
    """Lista de productos con búsqueda y paginación"""
    try:
        # Parámetros de búsqueda y paginación
        search_query = sanitize_string(request.args.get("q", ""))
        page = max(1, int(request.args.get("page", 1)))
        per_page = 20
        
        # Obtener productos
        offset = (page - 1) * per_page
        productos = db_manager.get_products(search_query, per_page, offset)
        
        # Obtener productos con stock bajo
        low_stock_products = db_manager.get_low_stock_products()
        low_stock_count = len(low_stock_products)
        
        # Log de acción
        log_user_action("lista_productos", f"búsqueda: '{search_query}', página: {page}", request.remote_addr)
        
        return render_template('productos/lista.html',
                             productos=productos,
                             search_query=search_query,
                             low_stock_count=low_stock_count,
                             app_title="RefuTrack",
                             current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)
    
    except Exception as e:
        logger.error(f"Error en lista_productos: {e}")
        flash("Error al cargar la lista de productos", "error")
        return redirect('/')

@main_bp.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    """Crear nuevo producto"""
    if request.method == "POST":
        try:
            # Validar y sanitizar datos
            sku = sanitize_string(request.form.get("sku", ""))
            nombre = sanitize_string(request.form.get("nombre", ""))
            descripcion = sanitize_string(request.form.get("descripcion", ""), 1000)
            
            # Validaciones
            sku_valid, sku_value = validate_sku(sku)
            if not sku_valid:
                raise ValidationError(sku_value)
            
            nombre_valid, nombre_value = validate_product_name(nombre)
            if not nombre_valid:
                raise ValidationError(nombre_value)
            
            stock_valid, stock_value = validate_stock_value(request.form.get("stock", "0"))
            if not stock_valid:
                raise ValidationError(stock_value)
            
            stock_min_valid, stock_min_value = validate_stock_value(request.form.get("stock_min", "0"), "Stock mínimo")
            if not stock_min_valid:
                raise ValidationError(stock_min_value)
            
            # Crear producto
            product_id = db_manager.create_product(
                sku=sku_value,
                nombre=nombre_value,
                descripcion=descripcion,
                stock=stock_value,
                stock_min=stock_min_value
            )
            
            log_user_action("crear_producto", f"SKU: {sku_value}, ID: {product_id}", request.remote_addr)
            flash(f"Producto '{sku_value}' creado exitosamente", "success")
            return redirect('/productos')
            
        except ValidationError as e:
            flash(str(e), "error")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            logger.error(f"Error creando producto: {e}")
            flash("Error interno al crear el producto", "error")
    
    # GET o POST con errores - mostrar formulario
    return render_template('productos/formulario.html',
                         form_title="Nuevo Producto",
                         producto=None,
                         app_title="RefuTrack",
                         current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)

@main_bp.route("/productos/<int:pid>/editar", methods=["GET", "POST"])
def editar_producto(pid):
    """Editar producto existente"""
    try:
        producto = db_manager.get_product(pid)
        if not producto:
            flash("Producto no encontrado", "error")
            return redirect('/productos')
        
        if request.method == "POST":
            # Validar y sanitizar datos
            sku = sanitize_string(request.form.get("sku", ""))
            nombre = sanitize_string(request.form.get("nombre", ""))
            descripcion = sanitize_string(request.form.get("descripcion", ""), 1000)
            
            # Validaciones
            sku_valid, sku_value = validate_sku(sku)
            if not sku_valid:
                raise ValidationError(sku_value)
            
            nombre_valid, nombre_value = validate_product_name(nombre)
            if not nombre_valid:
                raise ValidationError(nombre_value)
            
            stock_valid, stock_value = validate_stock_value(request.form.get("stock", "0"))
            if not stock_valid:
                raise ValidationError(stock_value)
            
            stock_min_valid, stock_min_value = validate_stock_value(request.form.get("stock_min", "0"), "Stock mínimo")
            if not stock_min_valid:
                raise ValidationError(stock_min_value)
            
            # Actualizar producto
            success = db_manager.update_product(
                pid,
                sku=sku_value,
                nombre=nombre_value,
                descripcion=descripcion,
                stock=stock_value,
                stock_min=stock_min_value
            )
            
            if success:
                log_user_action("editar_producto", f"SKU: {sku_value}, ID: {pid}", request.remote_addr)
                flash(f"Producto '{sku_value}' actualizado exitosamente", "success")
                return redirect('/productos')
            else:
                flash("No se pudo actualizar el producto", "error")
        
        return render_template('productos/formulario.html',
                             form_title="Editar Producto",
                             producto=producto,
                             app_title="RefuTrack",
                             current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)
    
    except ValidationError as e:
        flash(str(e), "error")
        return render_template('productos/formulario.html',
                             form_title="Editar Producto",
                             producto=producto,
                             app_title="RefuTrack",
                             current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)
    except Exception as e:
        logger.error(f"Error editando producto {pid}: {e}")
        flash("Error interno al editar el producto", "error")
        return redirect('/productos')

@main_bp.route("/productos/<int:pid>/borrar")
def borrar_producto(pid):
    """Eliminar producto"""
    try:
        producto = db_manager.get_product(pid)
        if not producto:
            flash("Producto no encontrado", "error")
            return redirect('/productos')
        
        success = db_manager.delete_product(pid)
        if success:
            log_user_action("eliminar_producto", f"SKU: {producto['sku']}, ID: {pid}", request.remote_addr)
            flash(f"Producto '{producto['sku']}' eliminado exitosamente", "success")
        else:
            flash("No se pudo eliminar el producto", "error")
    
    except Exception as e:
        logger.error(f"Error eliminando producto {pid}: {e}")
        flash("Error interno al eliminar el producto", "error")
    
    return redirect('/productos')

@main_bp.route("/productos/<int:pid>/movimientos")
def movimientos_producto(pid):
    """Mostrar movimientos de un producto"""
    try:
        producto = db_manager.get_product(pid)
        if not producto:
            flash("Producto no encontrado", "error")
            return redirect('/productos')
        
        movimientos = db_manager.get_movements(pid)
        
        # Formatear fechas
        for movimiento in movimientos:
            movimiento['creado_local'] = format_datetime_local(movimiento['creado_en'])
        
        log_user_action("ver_movimientos", f"SKU: {producto['sku']}, ID: {pid}", request.remote_addr)
        
        return render_template('productos/movimientos.html',
                             producto=producto,
                             movimientos=movimientos,
                             app_title="RefuTrack",
                             current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)
    
    except Exception as e:
        logger.error(f"Error obteniendo movimientos del producto {pid}: {e}")
        flash("Error al cargar los movimientos", "error")
        return redirect('/productos')

@main_bp.route("/productos/<int:pid>/ajustar", methods=["GET", "POST"])
def ajustar_stock(pid):
    """Ajustar stock de un producto"""
    try:
        producto = db_manager.get_product(pid)
        if not producto:
            flash("Producto no encontrado", "error")
            return redirect('/productos')
        
        if request.method == "POST":
            try:
                cantidad = int(request.form.get("cantidad", 0))
            except ValueError:
                raise ValidationError("Cantidad debe ser un número válido")
            
            destino = sanitize_string(request.form.get("destino", ""))
            nota = sanitize_string(request.form.get("nota", ""), 500)
            
            # Validar que para salidas se especifique destino
            if cantidad < 0 and not destino:
                raise ValidationError("Para una SALIDA, debe indicar el destino (topadora, retro, camioneta, etc.)")
            
            # Crear movimiento
            movement_id = db_manager.create_movement(
                product_id=pid,
                cantidad=cantidad,
                destino=destino if cantidad < 0 else "",
                nota=nota
            )
            
            log_user_action("ajustar_stock", 
                          f"SKU: {producto['sku']}, Cantidad: {cantidad}, ID: {movement_id}", 
                          request.remote_addr)
            
            flash(f"Movimiento aplicado exitosamente", "success")
            return redirect('/productos')
        
        return render_template('productos/ajustar_stock.html',
                             producto=producto,
                             app_title="RefuTrack",
                             current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)
    
    except ValidationError as e:
        flash(str(e), "error")
        return render_template('productos/ajustar_stock.html',
                             producto=producto,
                             app_title="RefuTrack",
                             current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
)
    except Exception as e:
        logger.error(f"Error ajustando stock del producto {pid}: {e}")
        flash("Error interno al ajustar el stock", "error")
        return redirect('/productos')

@main_bp.route("/exportar.csv")
def exportar_csv():
    """Exportar productos a CSV"""
    try:
        csv_data = db_manager.export_products_csv()
        
        log_user_action("exportar_csv", "", request.remote_addr)
        
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=productos.csv"}
        )
    
    except Exception as e:
        logger.error(f"Error exportando CSV: {e}")
        flash("Error al exportar los datos", "error")
        return redirect('/productos')

@main_bp.route("/reiniciar", methods=["POST"])
def reiniciar():
    """Crear nueva base de datos"""
    try:
        from config import Config
        import os
        from database import DatabaseManager
        
        # Crear nueva base con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_db_path = os.path.join(Config.APP_DIR, f"inventario_{timestamp}.db")
        
        # Crear nuevo gestor de BD
        new_db = DatabaseManager(new_db_path)
        
        # Actualizar la instancia global (esto requeriría modificar el módulo)
        # Por ahora, solo creamos la nueva base
        log_user_action("reiniciar_db", f"nueva BD: {os.path.basename(new_db_path)}", request.remote_addr)
        
        flash(f"Nueva base de datos creada: {os.path.basename(new_db_path)}", "success")
        
    except Exception as e:
        logger.error(f"Error reiniciando base de datos: {e}")
        flash("Error al crear nueva base de datos", "error")
    
    return redirect('/productos')

