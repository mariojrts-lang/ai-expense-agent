import mysql.connector
import os
from typing import Optional

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "expense_user"),
        password=os.getenv("DB_PASSWORD", "expense_secret_pass"),
        database=os.getenv("DB_NAME", "expenses_db")
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fecha DATE NOT NULL,
        descripcion VARCHAR(255) NOT NULL,
        categoria VARCHAR(100) NOT NULL,
        subcategoria VARCHAR(100) NOT NULL,
        tipo VARCHAR(50) NOT NULL,
        monto DECIMAL(10, 2) NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def registrar_gasto(monto: float, descripcion: str, categoria: str, subcategoria: str, tipo: str, fecha: str):
    """
    Registra un nuevo gasto en la base de datos.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO expenses (fecha, descripcion, categoria, subcategoria, tipo, monto)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (fecha, descripcion, categoria, subcategoria, tipo, monto))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Gasto registrado correctamente: {descripcion} por S/ {monto:.2f} (Fecha: {fecha})"

def consultar_gastos_totales(fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None, categoria: Optional[str] = None):
    """
    Consulta y recupera el listado completo y detallado de cada gasto en la base de datos, 
    incluyendo la fecha exacta (YYYY-MM-DD), descripcion, categoria, subcategoria, tipo y monto.
    Permite filtrar por fecha_inicio, fecha_fin y categoria.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT id, fecha, descripcion, categoria, subcategoria, tipo, monto FROM expenses WHERE 1=1"
    params = []
    
    if fecha_inicio:
        query += " AND fecha >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND fecha <= %s"
        params.append(fecha_fin)
    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)
        
    query += " ORDER BY fecha DESC, id DESC"
    
    cursor.execute(query, params)
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not registros:
        return "No se encontraron gastos registrados para los criterios especificados."
        
    resultado = "LISTA DE GASTOS DETALLADA:\n"
    total = 0.0
    for r in registros:
        fecha_str = str(r['fecha'])
        monto_val = float(r['monto'])
        resultado += f"Fecha: {fecha_str} | ID: {r['id']} | Descripcion: {r['descripcion']} | Categoria: {r['categoria']} | Subcategoria: {r['subcategoria']} | Tipo: {r['tipo']} | Monto: S/ {monto_val:.2f}\n"
        total += monto_val
        
    resultado += f"\nTotal Acumulado: S/ {total:.2f}"
    return resultado
