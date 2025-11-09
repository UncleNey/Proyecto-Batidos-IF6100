from db import get_conn, query_scalar, query_all, debug_connection_string
import pyodbc

def main():
    print("Drivers ODBC encontrados:", pyodbc.drivers())
    print("Connection string (sin password):", debug_connection_string())

    try:
        with get_conn() as conn:
            print("✅ Conexión exitosa a SQL Server.")
            cur = conn.cursor()
            cur.execute("SELECT @@VERSION;")
            print("Versión de SQL Server:", cur.fetchone()[0])
    except Exception as e:
        print("❌ Error de conexión:", e)
        return

    try:
        total = query_scalar("SELECT COUNT(*) FROM sys.tables;")
        print("Tablas en la BD actual:", total)

        tablas = query_all("""
            SELECT s.name AS esquema, t.name AS tabla
            FROM sys.tables t
            JOIN sys.schemas s ON s.schema_id = t.schema_id
            ORDER BY s.name, t.name;
        """)
        for t in tablas:
            print(f"- {t['esquema']}.{t['tabla']}")
    except Exception as e:
        print("⚠️ Conectó pero falló al consultar metadatos:", e)

if __name__ == "__main__":
    main()
