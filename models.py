import sqlite3
from typing import List, Optional
from pydantic import BaseModel
import os

os.makedirs("data", exist_ok=True)
DB_PATH = "data/gst_invoice.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Invoice Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        extracted_text TEXT,
        total_amount REAL,
        tax_amount REAL,
        status TEXT,
        gst_rate REAL,
        category TEXT
    )
    ''') # Status: Processed, Error, Verified

    # Migration for existing table
    try:
        cursor.execute("ALTER TABLE invoices ADD COLUMN gst_rate REAL")
        cursor.execute("ALTER TABLE invoices ADD COLUMN category TEXT")
    except sqlite3.OperationalError:
        pass # Columns likely exist


    # Product GST Mapping Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_gst (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT UNIQUE NOT NULL,
        gst_rate REAL NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic Models for API response
class InvoiceModel(BaseModel):
    id: int
    filename: str
    upload_date: str
    total_amount: Optional[float]
    tax_amount: Optional[float]
    status: str

class ProductGSTModel(BaseModel):
    keyword: str
    gst_rate: float

