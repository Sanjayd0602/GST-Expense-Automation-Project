import pytesseract
from PIL import Image
import re
import io
import pypdf

def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Intelligent extraction:
    - If filename ends vertically with .pdf -> Try pypdf (text based).
    - If pypdf gives nothing -> Provide warning (scanned PDF needs poppler).
    - Else -> Input to Tesseract as Image.
    """
    if filename.lower().endswith(".pdf"):
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Error reading PDF {filename}: {e}")
            return ""
            
    # Assume Image
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error reading Image {filename}: {e}")
        return ""

# BACKWARD COMPATIBILITY ALIAS
extract_text_from_image = lambda b: extract_text(b, "unknown.jpg")




def find_gst_rate(text: str, db_conn) -> tuple[float, str]:
    """
    Scans the text for product keywords from the database.
    Returns (GST rate, Keyword) of the first matched keyword.
    Default to (0.0, "Unknown") if no match.
    """
    cursor = db_conn.cursor()
    products = cursor.execute("SELECT keyword, gst_rate FROM product_gst").fetchall()
    
    # Simple case-insensitive search
    text_lower = text.lower()
    for product in products:
        if product['keyword'].lower() in text_lower:
            return (product['gst_rate'], product['keyword'])
            
    return (0.0, "Unknown")

def extract_total_amount(text: str) -> float:
    """
    Attempt to find the Total Amount using Regex.
    Looks for patterns like 'Total: 123.45', 'Amount: 500', etc.
    """
    # Regex for currency/amount patterns
    # Matches: "Total 1,234.56", "Amount: 500.00", etc.
    # We look for the last occurrence as "Total" usually appears at the bottom.
    
    pattern = r"(?:Total|Amount|Grand Total|Net Payable)[\s:]*[\$₹]?\s?([\d,]+\.?\d*)"
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        # Take the last match, remove commas, convert to float
        amount_str = matches[-1].replace(',', '')
        try:
            return float(amount_str)
        except ValueError:
            return 0.0
    return 0.0

def calculate_tax(total_amount: float, gst_rate: float) -> float:
    """
    Tax = Total - (Total / (1 + Rate/100))
    """
    if gst_rate == 0:
        return 0.0
    
    base_amount = total_amount / (1 + (gst_rate / 100))
    tax_amount = total_amount - base_amount
    return round(tax_amount, 2)
