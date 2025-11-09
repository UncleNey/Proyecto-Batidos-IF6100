import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

SERVER   = os.getenv("SQLSERVER_HOST", "localhost").strip()
DATABASE = os.getenv("SQLSERVER_DB", "batidos").strip()
AUTH     = os.getenv("SQLSERVER_AUTH", "windows").strip().lower()  # windows | sql

ENV_DRIVER = os.getenv("SQLSERVER_DRIVER", "").strip()
ENCRYPT  = os.getenv("SQLSERVER_ENCRYPT", "yes").strip()
TRUST    = os.getenv("SQLSERVER_TRUST_SERVER_CERT", "yes").strip()

USERNAME = os.getenv("SQLSERVER_USER", "").strip()
PASSWORD = os.getenv("SQLSERVER_PASSWORD", "").strip()

def _pick_driver() -> str:
    if ENV_DRIVER:
        return ENV_DRIVER
    installed = set(pyodbc.drivers())
    for cand in ("ODBC Driver 18 for SQL Server",
                 "ODBC Driver 17 for SQL Server",
                 "ODBC Driver 13 for SQL Server"):
        if cand in installed:
            return cand
    for d in installed:
        if "ODBC Driver" in d and "SQL Server" in d:
            return d
    raise RuntimeError("No se encontró un driver ODBC de SQL Server instalado.")

def _build_conn_str() -> str:
    driver = _pick_driver()
    parts = [
        "DRIVER={" + driver + "}",
        "SERVER=" + SERVER,
        "DATABASE=" + DATABASE,
        "Encrypt=" + ENCRYPT,
        "TrustServerCertificate=" + TRUST,
    ]
    if AUTH == "windows":
        parts.append("Trusted_Connection=yes")
    else:
        parts.append("UID=" + USERNAME)
        parts.append("PWD=" + PASSWORD)
    return ";".join(parts)

def get_conn():
    return pyodbc.connect(_build_conn_str(), timeout=5)

def query_scalar(sql: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row[0] if row else None

def execute(sql: str, params=None, commit=True):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or [])
        if commit:
            conn.commit()

def query_all(sql: str, params=None):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or [])
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

def debug_connection_string(mask_password: bool = True) -> str:
    driver = _pick_driver()
    parts = [
        "DRIVER={" + driver + "}",
        "SERVER=" + SERVER,
        "DATABASE=" + DATABASE,
        "Encrypt=" + ENCRYPT,
        "TrustServerCertificate=" + TRUST,
        "Trusted_Connection=yes" if AUTH == "windows" else "UID=" + USERNAME,
    ]
    if AUTH != "windows":
        parts.append("PWD=" + ("***" if mask_password else PASSWORD))
    return ";".join(parts)
