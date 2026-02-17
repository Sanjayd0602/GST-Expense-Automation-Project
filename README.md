# GST Invoice Processor

## Overview
The GST Invoice Processor is an automated tool designed to extract, analyze, and store data from GST invoices. It leverages Optical Character Recognition (OCR) to read text from invoice images and PDFs, identifies GST rates based on product keywords, and calculates tax breakdowns. The application provides a dashboard for viewing processed invoices and analytics.

## Features
- **OCR Extraction**: Extracts text from image (JPG, PNG) and PDF invoices using Tesseract and Poppler.
- **Automated GST Classification**: Matches extracted product names against a database of keywords and GST rates.
- **Tax Calculation**: Computes base amount and tax components based on the identified GST rate.
- **Dashboard Analytics**: Visualizes total processed amount, tax collected, and GST rate distribution.
- **Database Storage**: Stores processed invoice data in a SQLite database for persistence.

## Technologies Used
- **Backend**: Python, FastAPI
- **OCR**: Tesseract-OCR, pdf2image (Poppler)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Jinja2 Templates
- **Data Processing**: Pandas, NumPy

## Local Installation

### Prerequisites
1.  **Python 3.8+**
2.  **Tesseract-OCR**: Must be installed on your system.
    - Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
3.  **Poppler**: Required for PDF processing.
    - Windows: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/) and add `bin/` to your PATH.

### Steps
1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/gst-invoice-processor.git
    cd gst-invoice-processor
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```
4.  Open your browser at `http://localhost:8000`.

## Deployment (Docker)
This application includes a `Dockerfile` for easy deployment to cloud platforms like Render, Railway, or Heroku.

1.  Build the Docker image:
    ```bash
    docker build -t gst-app .
    ```
2.  Run the container:
    ```bash
    docker run -p 8000:8000 gst-app
    ```

## Usage
1.  **Upload Invoice**: Navigate to the upload section and select an invoice file (image or PDF).
2.  **View Results**: The dashboard will update with the extracted details, calculated tax, and invoice status.
3.  **Upload Dataset**: You can upload a CSV file with `keyword,gst_rate` columns to update the product tax database.
