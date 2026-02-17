# Research Project Submission: Automated GST Invoice Processing System

**Author:** [Your Name]
**Date:** February 2026
**Subject:** Submission for Research Journal / Project Evaluation

---

## Abstract
The Automated GST Invoice Processing System is a web-based application developed to streamline the extraction and analysis of tax invoice data. Manual entry of invoice details is error-prone and time-consuming. This project automates the process using Optical Character Recognition (OCR) and keyword-based classification algorithms. The system accepts invoice images or PDFs, extracts relevant text, identifies applicable Goods and Services Tax (GST) rates, and computes tax liabilities with high accuracy.

## 1. Introduction
With the implementation of GST, businesses face increased compliance requirements involving detailed invoice tracking. This project addresses the need for an efficient, automated solution to digitize and process paper-based or digital image invoices. The goal is to reduce human error and provide real-time analytics on tax obligations.

## 2. Methodology

### 2.1 System Architecture
The application is built on a client-server architecture:
- **Frontend**: A responsive web interface for file uploads and dashboard visualization (HTML/CSS).
- **Backend**: A Python-based REST API using the FastAPI framework for high performance.
- **OCR Engine**: Tesseract-OCR is employed for text extraction, with Poppler used for rendering PDF documents into processable images.
- **Database**: SQLite is used for persistent storage of invoice records and GST rate lookups.

### 2.2 Core Algorithms
1.  **Preprocessing**: Input images are converted to grayscale and thresholded to improve OCR accuracy.
2.  **Text Extraction**: Tesseract-OCR processes the image to generate raw text.
3.  **Keyword Matching**: The extracted text is tokenized and matched against a pre-populated database of product keywords (e.g., "Electronics", "Textiles") to determine the specific GST rate (5%, 12%, 18%, 28%).
4.  **Tax Calculation**:
    $$ \text{Base Amount} = \frac{\text{Total Amount}}{1 + (\text{GST Rate}/100)} $$
    $$ \text{Tax Amount} = \text{Total Amount} - \text{Base Amount} $$

## 3. Implementation and Results
The system was tested with a variety of invoice formats. It successfully identified key fields such as Total Amount and Product Descriptions. The keyword matching algorithm demonstrated effective classification for standard inventory items. The integrated dashboard provides immediate visual feedback on tax distribution, aiding in financial decision-making.

## 4. Conclusion
The Automated GST Invoice Processor demonstrates the viability of using open-source OCR tools for financial document processing. It offers a scalable, cost-effective solution for small to medium enterprises to manage their GST compliance.

## 5. Future Scope
- Integration with Deep Learning models (e.g., LayoutLM) for better structure understanding.
- Support for multi-page invoices and bulk processing.
- Direct export to government GST portals.

---
**Repository Link:** [Link to your GitHub Repository]
