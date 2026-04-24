# RefuTrack - Módulo de base de datos
import sqlite3
import logging
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestor de base de datos con manejo de conexiones y transacciones"""
    
    SCHEMA = """PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL DEFAULT '',
        stock INTEGER NOT NULL DEFAULT 0,
        stock_min INTEGER NOT NULL DEFAULT 0,
        creado_en TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        cantidad INTEGER NOT NULL,
        destino TEXT NOT NULL DEFAULT '',
        nota TEXT,
        creado_en TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_mov_prod ON movimientos(product_id);
    CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
    CREATE INDEX IF NOT EXISTS idx_products_stock ON products(stock);
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DB_PATH
        self._ensure_schema()
    
    @contextmanager
    def get_connection(self):
        """Context manager para manejo seguro de conexiones"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Error de base de datos: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_transaction(self):
        """Context manager para transacciones"""
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Error en transacción: {e}")
                raise
    
    def _ensure_schema(self):
        """Crear esquema de base de datos si no existe"""
        try:
            with self.get_connection() as conn:
                conn.executescript(self.SCHEMA)
            logger.info("Esquema de base de datos verificado")
        except sqlite3.Error as e:
            logger.error(f"Error creando esquema: {e}")
            raise
    
    # Métodos para productos
    def create_product(self, sku: str, nombre: str, descripcion: str = "", 
                      stock: int = 0, stock_min: int = 0) -> int:
        """Crear un nuevo producto"""
        from datetime import datetime
        try:
            with self.get_transaction() as conn:
                cursor = conn.execute(
                    """INSERT INTO products(sku, nombre, descripcion, stock, stock_min, creado_en) 
                       VALUES (?,?,?,?,?,?)""",
                    (sku, nombre, descripcion, stock, stock_min, 
                     datetime.utcnow().isoformat())
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("SKU duplicado")
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtener un producto por ID"""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
            return dict(row) if row else None
    
    def get_products(self, search: str = None, limit: int = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtener lista de productos con búsqueda opcional"""
        with self.get_connection() as conn:
            if search:
                query = """SELECT * FROM products 
                          WHERE sku LIKE ? OR nombre LIKE ? OR descripcion LIKE ? 
                          ORDER BY id DESC"""
                params = (f"%{search}%", f"%{search}%", f"%{search}%")
            else:
                query = "SELECT * FROM products ORDER BY id DESC"
                params = ()
            
            if limit:
                query += " LIMIT ? OFFSET ?"
                params = params + (limit, offset)
            
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
    
    def update_product(self, product_id: int, **kwargs) -> bool:
        """Actualizar un producto"""
        # Filtrar campos permitidos
        allowed_fields = {'sku', 'nombre', 'descripcion', 'stock', 'stock_min'}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        set_clause = ", ".join([f"{k}=?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [product_id]
        
        try:
            with self.get_transaction() as conn:
                cursor = conn.execute(
                    f"UPDATE products SET {set_clause} WHERE id=?",
                    values
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            raise ValueError("SKU duplicado")
    
    def delete_product(self, product_id: int) -> bool:
        """Eliminar un producto"""
        with self.get_transaction() as conn:
            cursor = conn.execute("DELETE FROM products WHERE id=?", (product_id,))
            return cursor.rowcount > 0
    
    # Métodos para movimientos
    def create_movement(self, product_id: int, cantidad: int, 
                       destino: str = "", nota: str = "") -> int:
        """Crear un nuevo movimiento de stock"""
        from datetime import datetime
        try:
            with self.get_transaction() as conn:
                # Crear el movimiento
                cursor = conn.execute(
                    """INSERT INTO movimientos(product_id, cantidad, destino, nota, creado_en) 
                       VALUES (?,?,?,?,?)""",
                    (product_id, cantidad, destino, nota, datetime.utcnow().isoformat())
                )
                movement_id = cursor.lastrowid
                
                # Actualizar stock del producto
                conn.execute(
                    "UPDATE products SET stock = stock + ? WHERE id = ?",
                    (cantidad, product_id)
                )
                
                return movement_id
        except sqlite3.Error as e:
            logger.error(f"Error creando movimiento: {e}")
            raise
    
    def get_movements(self, product_id: int) -> List[Dict[str, Any]]:
        """Obtener movimientos de un producto"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM movimientos WHERE product_id=? ORDER BY id DESC",
                (product_id,)
            ).fetchall()
            return [dict(row) for row in rows]
    
    def get_low_stock_products(self) -> List[Dict[str, Any]]:
        """Obtener productos con stock bajo"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM products WHERE stock <= stock_min ORDER BY stock ASC"
            ).fetchall()
            return [dict(row) for row in rows]
    
    def export_products_csv(self) -> str:
        """Exportar productos a formato CSV"""
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        writer.writerow(["id", "sku", "nombre", "descripcion", "stock", "stock_min", "creado_en"])
        
        # Datos
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM products ORDER BY id")
            for row in rows:
                writer.writerow([
                    row["id"], row["sku"], row["nombre"], 
                    row["descripcion"], row["stock"], row["stock_min"], row["creado_en"]
                ])
        
        return output.getvalue()

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()



