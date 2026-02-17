from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pytesseract
import shutil
import os
import io
from .models import init_db, get_db_connection

# --- CONFIGURATION ---
# Tesseract Path
# 1. Try Environment Variable (Best for Docker/Cloud)
tesseract_cmd = os.getenv("TESSERACT_CMD")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
# 2. Try Common Windows Path (Fallback for Local)
elif os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 3. Default (Relies on PATH)
else:
    # If tesseract is in PATH (like in Docker/Linux), this just works.
    pass

app = FastAPI(title="GST Invoice Processor")

# Mount Static & Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize DB
init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    conn = get_db_connection()
    invoices = conn.execute("SELECT * FROM invoices ORDER BY upload_date DESC").fetchall()
    keywords = conn.execute("SELECT * FROM product_gst").fetchall() # For display
    conn.close()
    
    # Calculate Summary Stats
    total_invoices = len(invoices)
    total_amount = sum(inv['total_amount'] if inv['total_amount'] else 0 for inv in invoices)
    total_tax = sum(inv['tax_amount'] if inv['tax_amount'] else 0 for inv in invoices)
    
    # Calculate Distribution
    gst_distribution = {
        "5%": 0,
        "12%": 0,
        "18%": 0,
        "28%": 0,
        "Other": 0
    }
    
    for inv in invoices:
        rate = inv['gst_rate']
        if rate == 5.0:
            gst_distribution["5%"] += 1
        elif rate == 12.0:
            gst_distribution["12%"] += 1
        elif rate == 18.0:
            gst_distribution["18%"] += 1
        elif rate == 28.0:
            gst_distribution["28%"] += 1
        else:
            gst_distribution["Other"] += 1
            
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "invoices": invoices,
        "keywords": keywords,
        "summary": {
            "total_invoices": total_invoices,
            "total_amount": round(total_amount, 2),
            "total_tax": round(total_tax, 2),
            "gst_distribution": gst_distribution
        }
    })

# --- UPLOAD HANDLERS ---
from .extractor import extract_text, find_gst_rate, extract_total_amount, calculate_tax
import pandas as pd

@app.post("/upload_invoice")
async def upload_invoice(file: UploadFile = File(...)):
    import traceback
    try:
        contents = await file.read()
        
        # 1. Extraction (PDF or Image)
        text = extract_text(contents, file.filename)
        
        # DEBUG: Write text to file
        with open("debug_last_invoice.txt", "w", encoding="utf-8") as f:
            f.write(text)
            
        # 2. Logic
        conn = get_db_connection()
        gst_rate, category = find_gst_rate(text, conn)
        
        total_amount = extract_total_amount(text)
        
        # Fallback: if total is 0, try finding the largest number in the text
        if total_amount == 0.0:
            import re
            # Extract all potential decimal numbers
            candidates = re.findall(r"[\d,]+\.\d{2}", text)
            if candidates:
                # Clean and convert
                values = []
                for c in candidates:
                    try:
                        v = float(c.replace(',', ''))
                        values.append(v)
                    except: pass
                if values:
                    total_amount = max(values) # Assumption: Total is usually the largest amount
        
        tax_amount = calculate_tax(total_amount, gst_rate)
        
        # 3. Save
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invoices (filename, extracted_text, total_amount, tax_amount, status, gst_rate, category) VALUES (?,?,?,?,?,?,?)",
            (file.filename, text, total_amount, tax_amount, "Processed", gst_rate, category)
        )
        conn.commit()
        conn.close()
        
        return RedirectResponse(url="/dashboard", status_code=303)
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print("ERROR IN UPLOAD:", error_msg)
        with open("error_log.txt", "w") as f:
            f.write(error_msg)
        return HTMLResponse(content=f"<h1>Internal Server Error</h1><pre>{error_msg}</pre>", status_code=500)

@app.post("/upload_dataset")
async def upload_dataset(file: UploadFile = File(...)):
    # Expect CSV: keyword, gst_rate
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Upsert logic (replace if exists)
    for index, row in df.iterrows():
        try:
            keyword = row['keyword']
            rate = float(row['gst_rate'])
            cursor.execute("INSERT OR REPLACE INTO product_gst (keyword, gst_rate) VALUES (?, ?)", (keyword, rate))
        except Exception as e:
            print(f"Skipping row {index}: {e}")
            
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/dashboard", status_code=303)

