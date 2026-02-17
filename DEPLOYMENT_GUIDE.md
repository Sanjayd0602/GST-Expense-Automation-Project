# Simple Deployment Guide

This guide will help you put your project on the internet so your instructor can see it and you can get a public link.

**Goal**: Get a website link like `https://gst-app.onrender.com` that works on ANY laptop.

---

## Phase 1: Upload Your Code to GitHub
You need to put your code in a place where the cloud server can find it. GitHub is that place.

### Option A: The Easiest Way (No Commands)
1.  **Create an Account**: Go to [github.com](https://github.com/) and sign up (it's free).
2.  **Create a New Repository**:
    *   Click the **+** icon in the top-right corner -> **New repository**.
    *   Repository name: `gst-project`.
    *   Make sure it is **Public**.
    *   Click **Create repository**.
3.  **Upload Files**:
    *   Look for the link: **uploading an existing file** (it's small text in the "Quick setup" box).
    *   **Drag and Drop** ALL your project files/folders (app, data, requirements.txt, Dockerfile, etc.) into the browser window.
    *   **Important**: Do NOT upload `__pycache__` or `.git` folders if you see them.
    *   Wait for the files to upload.
    *   In the "Commit changes" box at the bottom, type "Initial upload" and click **Commit changes**.

### Option B: The "Pro" Way (If you know Git)
If you already use Git, just push your code:
```bash
git init
git add .
git commit -m "Ready for deploy"
git remote add origin https://github.com/YOUR_USERNAME/gst-project.git
git push origin main
```

---

## Phase 2: Put it on the Cloud (Render)
Render is a cloud provider that will run your code.

1.  **Sign Up**: Go to [render.com](https://render.com/) and sign up using your **GitHub** account.
2.  **New Web Service**:
    *   Click the **New +** button at the top right.
    *   Select **Web Service**.
3.  **Connect Repo**:
    *   You will see your `gst-project` repository in the list. Click **Connect**.
4.  **Settings (Very Important)**:
    *   **Name**: `my-gst-app` (or whatever you like).
    *   **Region**: Singapore (or nearest).
    *   **Runtime**: Select **Docker** (Do NOT select Python).
    *   **Instance Type**: Free.
5.  **Deploy**:
    *   Scroll down and click **Create Web Service**.

---

## Phase 3: Wait and Verify
1.  Render will verify your files and install the necessary software (Tesseract OCR). This takes about **3-5 minutes**.
2.  Watch the logs ("black screen with text"). When it says **"Live"** or **"Application startup complete"**, you are done!
3.  **Copy the URL** at the top (`https://my-gst-app.onrender.com`).
4.  **Share this link**. Open it on your phone or a friend's laptop to test.

---

## Frequently Asked Questions
*   **Why does it take so long?**
    It's installing Tesseract and other heavy tools for you. The first time is slow; updates are faster.
*   **What if it fails?**
    Check the "Logs" tab. If you missed uploading a file (like `Dockerfile`), it will tell you.
