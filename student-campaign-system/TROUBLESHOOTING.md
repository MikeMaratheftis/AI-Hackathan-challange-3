# Troubleshooting Guide

## Installation Issues

### Problem: pip install fails

**Solution 1: Use Minimal Requirements**
```bash
pip install -r requirements-minimal.txt
```

**Solution 2: Install Individually**
```bash
pip install Flask>=2.0.0
pip install Flask-CORS>=3.0.0
pip install SQLAlchemy>=1.4.0
pip install python-dotenv>=0.19.0
```

**Solution 3: Use Setup Script**
```bash
python setup.py
```

**Solution 4: Upgrade pip**
```bash
python -m pip install --upgrade pip
pip install -r requirements-minimal.txt
```

---

## Runtime Issues

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install Flask
```

### Problem: "ModuleNotFoundError: No module named 'flask_cors'"

**Solution:**
```bash
pip install Flask-CORS
```

### Problem: "ModuleNotFoundError: No module named 'sqlalchemy'"

**Solution:**
```bash
pip install SQLAlchemy
```

### Problem: Port 5000 already in use

**Solution (Linux/Mac):**
```bash
lsof -i :5000
kill -9 <PID>
```

**Solution (Windows):**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Alternative:** Use different port
```bash
# Edit app.py and change:
app.run(debug=True, port=5001)
```

---

## Database Issues

### Problem: Database locked error

**Solution:**
```bash
rm student_campaign.db
python app.py
```

### Problem: "No such table" error

**Solution:**
```bash
python -c "from app import create_app; app = create_app()"
```

---

## Frontend Issues

### Problem: Page not loading

**Check:**
1. Is Flask running? (should see output in terminal)
2. Is port 5000 accessible?
3. Try: http://localhost:5000

**Solution:**
```bash
# Restart Flask
python app.py
```

### Problem: API calls failing

**Check:**
1. Is backend running?
2. Check browser console (F12)
3. Check Flask terminal for errors

**Solution:**
```bash
# Check if API is responding
curl http://localhost:5000/health
```

---

## Testing Issues

### Problem: pytest not found

**Solution:**
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

### Problem: Tests failing

**Solution:**
```bash
# Run with verbose output
pytest tests/ -v -s

# Run specific test
pytest tests/test_scoring_engine.py -v
```

---

## Common Error Messages

### "Address already in use"
Port 5000 is taken. Kill the process or use different port.

### "Connection refused"
Flask not running. Start with: `python app.py`

### "No module named"
Package not installed. Install with: `pip install <package>`

### "Database is locked"
Delete database and restart: `rm student_campaign.db && python app.py`

### "CORS error"
Check Flask-CORS is installed: `pip install Flask-CORS`

---

## Verification Checklist

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Verify packages
python -c "import flask; import flask_cors; import sqlalchemy; import dotenv; print('✅ All OK')"

# Check if Flask runs
python -c "from app import create_app; print('✅ App loads')"

# Check if API responds
curl http://localhost:5000/health
```

---

## Step-by-Step Troubleshooting

### 1. Clean Installation

```bash
# Remove virtual environment (if using one)
rm -rf venv

# Create fresh virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install minimal requirements
pip install -r requirements-minimal.txt

# Run setup
python setup.py

# Start app
python app.py
```

### 2. Verify Each Step

```bash
# Step 1: Check Python
python --version

# Step 2: Check pip
pip --version

# Step 3: Install Flask
pip install Flask
python -c "import flask; print('Flask OK')"

# Step 4: Install Flask-CORS
pip install Flask-CORS
python -c "import flask_cors; print('Flask-CORS OK')"

# Step 5: Install SQLAlchemy
pip install SQLAlchemy
python -c "import sqlalchemy; print('SQLAlchemy OK')"

# Step 6: Install python-dotenv
pip install python-dotenv
python -c "import dotenv; print('python-dotenv OK')"

# Step 7: Run app
python app.py
```

### 3. Test Application

```bash
# In another terminal:
curl http://localhost:5000/health
```

---

## Getting Help

### Provide This Information

1. **Python version:**
   ```bash
   python --version
   ```

2. **pip version:**
   ```bash
   pip --version
   ```

3. **Error message:** (full error text)

4. **Operating system:** (Windows/Mac/Linux)

5. **What you tried:** (steps taken)

---

## Quick Fixes

### "Just make it work" approach

```bash
# 1. Clear everything
pip cache purge

# 2. Upgrade pip
python -m pip install --upgrade pip

# 3. Install minimal
pip install Flask Flask-CORS SQLAlchemy python-dotenv

# 4. Run
python app.py
```

### If that doesn't work

```bash
# Use the setup script
python setup.py
```

---

## Alternative: Use Wireframe Only

If you can't get the backend running, you can still use the wireframe:

```bash
python serve_static.py
```

Then open: http://localhost:8000

The wireframe has mock data and doesn't require backend dependencies.

---

## Still Stuck?

1. **Check INSTALLATION_HELP.md** - Detailed installation guide
2. **Check START_HERE.md** - Quick start guide
3. **Check README.md** - Backend documentation
4. **Review error message** - Google the exact error
5. **Try setup.py** - Automated setup script

---

## Summary

| Issue | Solution |
|-------|----------|
| pip install fails | Use `requirements-minimal.txt` |
| Module not found | Install individually |
| Port in use | Kill process or use different port |
| Database error | Delete `student_campaign.db` |
| API not responding | Check Flask is running |
| Tests failing | Run with `-v` flag for details |

---

**Most issues are resolved by:**
1. Using `requirements-minimal.txt`
2. Running `python setup.py`
3. Restarting Flask

Try these first! 🚀
