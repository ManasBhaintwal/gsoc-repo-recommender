# backend/database/connection.py
import os
from dotenv import load_dotenv
import psycopg
from psycopg_pool import ConnectionPool

load_dotenv()

# Create a connection pool for better performance
_pool = None

def get_pool():
    """Get or create the connection pool."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=f"host={os.getenv('DB_HOST', 'localhost')} "
                     f"port={os.getenv('DB_PORT', '5432')} "
                     f"dbname={os.getenv('DB_NAME', 'gsoc')} "
                     f"user={os.getenv('DB_USER', 'postgres')} "
                     f"password={os.getenv('DB_PASS', '')}",
            min_size=2,
            max_size=10,
            timeout=30,
            open=False  # Don't open pool immediately
        )
        _pool.open()  # Open when first requested
    return _pool

def get_conn():
    """
    Returns a connection from the pool.
    For backward compatibility, returns a regular connection.
    Consider using get_pool().connection() for better performance.
    """
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "gsoc"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", ""),
        autocommit=False
    )

def close_pool():
    """Close the connection pool. Call this on application shutdown."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None
