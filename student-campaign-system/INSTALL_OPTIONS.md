# Installation Options

Choose the option that works best for you:

---

## ⭐ Option 1: Automated Setup (Recommended)

**Easiest - Let the script handle everything**

```bash
python setup.py
```

This will:
- ✅ Upgrade pip
- ✅ Install minimal requirements
- ✅ Create .env file
- ✅ Initialize database
- ✅ Verify installation

Then start the app:
```bash
python app.py
```

---

## 🚀 Option 2: Minimal Requirements (Fast)

**Fastest - Only essential packages**

```bash
pip install -r requirements-minimal.txt
python app.py
```

This installs only:
- Flask
- Flask-CORS
- SQLAlchemy
- python-dotenv

---

## 📦 Option 3: Full Requirements (Complete)

**Complete - All packages including testing**

```bash
pip install -r requirements.txt
python app.py
```

This installs everything including:
- pytest (for testing)
- black (for code formatting)
- flake8 (for linting)

---

## 🔧 Option 4: Manual Installation

**Step-by-step - Install each package**

```bash
pip install Flask>=2.0.0
pip install Flask-CORS>=3.0.0
pip install SQLAlchemy>=1.4.0
pip install python-dotenv>=0.19.0
python app.py
```

---

## 🐳 Option 5: Docker (If installed)

**Container - No Python dependencies needed**

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements-minimal.txt .
RUN pip install -r requirements-minimal.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t student-campaign .
docker run -p 5000:5000 student-campaign
```

---

## 🌐 Option 6: Wireframe Only (No Backend)

**No installation - Just view the design**

```bash
python serve_static.py
```

Then open: http://localhost:8000

No backend dependencies needed!

---

## 📋 Comparison

| Option | Speed | Complexity | Features | Best For |
|--------|-------|-----------|----------|----------|
| 1. Automated | ⭐⭐⭐ | ⭐ | All | First time users |
| 2. Minimal | ⭐⭐⭐ | ⭐ | Core | Quick start |
| 3. Full | ⭐⭐ | ⭐⭐ | All | Development |
| 4. Manual | ⭐ | ⭐⭐⭐ | All | Troubleshooting |
| 5. Docker | ⭐⭐ | ⭐⭐ | All | Production |
| 6. Wireframe | ⭐⭐⭐ | ⭐ | UI/UX | Design review |

---

## 🎯 Recommended Path

### For Most Users:
```bash
python setup.py
python app.py
```

### If That Fails:
```bash
pip install -r requirements-minimal.txt
python app.py
```

### If Still Failing:
```bash
pip install Flask Flask-CORS SQLAlchemy python-dotenv
python app.py
```

### If Backend Won't Work:
```bash
python serve_static.py
```

---

## ✅ Verification

After installation, verify everything works:

```bash
# Check packages
python -c "import flask; import flask_cors; import sqlalchemy; import dotenv; print('✅ All packages OK')"

# Check app loads
python -c "from app import create_app; print('✅ App loads')"

# Check API responds
curl http://localhost:5000/health
```

---

## 🆘 Troubleshooting

### If pip install fails:
1. Try `requirements-minimal.txt`
2. Try `python setup.py`
3. See TROUBLESHOOTING.md

### If Flask won't start:
1. Check port 5000 is free
2. Check all packages installed
3. See TROUBLESHOOTING.md

### If API not responding:
1. Check Flask is running
2. Check browser console (F12)
3. See TROUBLESHOOTING.md

---

## 📚 Documentation

- **INSTALLATION_HELP.md** - Detailed installation help
- **TROUBLESHOOTING.md** - Common issues and solutions
- **START_HERE.md** - Quick start guide
- **QUICK_REFERENCE.md** - Quick lookup

---

## 🚀 Next Steps

1. **Choose an option above**
2. **Run the installation**
3. **Start the app:** `python app.py`
4. **Open browser:** http://localhost:5000
5. **Start testing!**

---

**Pick Option 1 or 2 to get started quickly! 🎉**
