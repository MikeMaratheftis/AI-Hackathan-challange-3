# Installation Troubleshooting Guide

## Problem: Requirements Installation Failing

If you're having trouble installing requirements, try these solutions:

---

## Solution 1: Use Minimal Requirements (Recommended)

The minimal requirements file has fewer dependencies and is more likely to work:

```bash
pip install -r requirements-minimal.txt
```

This installs only the essential packages needed to run the application.

---

## Solution 2: Install Packages Individually

If the above doesn't work, install packages one by one:

```bash
pip install Flask>=2.0.0
pip install Flask-CORS>=3.0.0
pip install SQLAlchemy>=1.4.0
pip install python-dotenv>=0.19.0
```

---

## Solution 3: Upgrade pip First

Sometimes the issue is with pip itself:

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Then try installing requirements
pip install -r requirements-minimal.txt
```

---

## Solution 4: Use Virtual Environment

Create a fresh virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Then install
pip install -r requirements-minimal.txt
```

---

## Solution 5: Check Python Version

Make sure you have Python 3.8 or higher:

```bash
python --version
```

If you have Python 3.7 or lower, upgrade Python.

---

## Solution 6: Clear pip Cache

Sometimes pip cache causes issues:

```bash
pip cache purge
pip install -r requirements-minimal.txt
```

---

## Solution 7: Use Compatible Versions

If you still have issues, try this ultra-minimal setup:

```bash
pip install Flask
pip install Flask-CORS
pip install SQLAlchemy
pip install python-dotenv
```

---

## Common Error Messages

### "No module named 'flask'"
```bash
pip install Flask
```

### "No module named 'flask_cors'"
```bash
pip install Flask-CORS
```

### "No module named 'sqlalchemy'"
```bash
pip install SQLAlchemy
```

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

---

## Verify Installation

After installing, verify everything works:

```bash
python -c "import flask; import flask_cors; import sqlalchemy; import dotenv; print('✅ All packages installed successfully!')"
```

---

## Run the Application

Once packages are installed:

```bash
python app.py
```

Then open: http://localhost:5000

---

## Still Having Issues?

### Option 1: Run Without Testing Packages
The testing packages (pytest, black, flake8) are optional. The app will run without them.

### Option 2: Use Docker
If installation is problematic, consider using Docker:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements-minimal.txt .
RUN pip install -r requirements-minimal.txt
COPY . .
CMD ["python", "app.py"]
```

### Option 3: Contact Support
If you're still stuck, provide:
1. Your Python version: `python --version`
2. Your pip version: `pip --version`
3. The error message you're getting
4. Your operating system

---

## Quick Checklist

- [ ] Python 3.8+ installed
- [ ] pip is up to date
- [ ] Virtual environment created (optional but recommended)
- [ ] Packages installed successfully
- [ ] Can import packages without errors
- [ ] Application starts on port 5000

---

## Minimal Installation (Just to Run)

If you only want to run the application without testing:

```bash
pip install Flask Flask-CORS SQLAlchemy python-dotenv
python app.py
```

That's it! The app will work with just these 4 packages.

---

## Next Steps

Once installation is complete:

1. Start the application: `python app.py`
2. Open browser: http://localhost:5000
3. Test the features
4. Review the code

---

**Need help?** Check the error message and try the corresponding solution above.
