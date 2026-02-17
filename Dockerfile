# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Install system dependencies for Tesseract and Poppler
# - tesseract-ocr: The OCR engine
# - poppler-utils: Required by pdf2image to convert PDFs to images
# - libgl1-mesa-glx: Required by some OpenCV builds (if used, good to have)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code/app
# Also copy data or other necessary folders if they exist and are needed at runtime
COPY ./sample_product_gst.csv /code/sample_product_gst.csv

# Set environment variable to ensure output matches expected encoding
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on (Render uses 10000 by default, but we can make it configurable)
EXPOSE 8000

# Command to run the application
# We use the generic "app.main:app" assuming main.py is in app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



