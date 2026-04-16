# 🚀 START HERE

## Welcome to the Student Campaign License Allocation System!

You have a **complete, production-ready full-stack application** with both a real frontend and backend.

---

## ⚡ Quick Start (30 seconds)

### Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

### Windows
```bash
run.bat
```

### Manual
```bash
pip install -r requirements.txt
python app.py
```

**Then open your browser to:** http://localhost:5000

---

## 📱 What You Can Do

### As a Student
1. **Apply for Claude License**
   - Fill out application form
   - Get instant score (0-100)
   - See if you're approved, rejected, or waitlisted

2. **View Your Application**
   - See score breakdown
   - View license details
   - Check days remaining

3. **Submit Progress Report**
   - Report your progress
   - Get extension approval
   - Extend your license

### As an Admin
1. **View Dashboard**
   - See statistics
   - View score distribution
   - Check license inventory

2. **Manage Applications**
   - Filter applications
   - Search by student
   - View details

3. **Configure System**
   - Update cutoff scores
   - Adjust license settings
   - Manage inventory

---

## 🎯 Key Features

✅ **Real Application** - Connected to backend, not mock data
✅ **Scoring Engine** - 5-criterion scoring system (0-100)
✅ **License Allocation** - Automatic approval/rejection/waitlist
✅ **Progress Tracking** - Submit reports for extensions
✅ **Admin Dashboard** - Full management interface
✅ **Database** - Real data persistence
✅ **API** - 14 RESTful endpoints
✅ **Tests** - Comprehensive test suite
✅ **Preserved Wireframe** - Original design for reference

---

## 📊 Scoring System

Your application is scored on 5 criteria (total 100 points):

| Criterion | Points | Example |
|-----------|--------|---------|
| Degree Relevance | 0-30 | STEM=30, Business=25 |
| Objective Quality | 0-25 | Detailed goal=25 |
| Academic Standing | 0-20 | Graduate=20 |
| Demonstrated Need | 0-15 | Financial aid=8 |
| Claude Familiarity | 0-10 | Experienced=10 |

**Allocation:**
- Score ≥ 60 (STEM) → ✅ APPROVED
- Score ≥ 60 + No licenses → ⏳ WAITLISTED
- Score < 60 → ❌ REJECTED

---

## 📁 What's Included

```
✅ Real Application (static/app.js)
✅ Preserved Wireframe (static-wireframe/script.js)
✅ Backend API (app.py + services/)
✅ Database Models (models.py)
✅ Test Suite (tests/)
✅ Documentation (*.md files)
✅ Quick Start Scripts (run.sh, run.bat)
```

---

## 🧪 Test It Out

### Try These Steps:

1. **Submit an Application**
   - Name: Jane Doe
   - Email: jane.doe@mit.edu
   - Degree: Computer Science
   - Objective: "I want to use Claude for my NLP research..."
   - Click Submit

2. **View Your Score**
   - Go to "My Application" tab
   - See score breakdown
   - Check if approved

3. **Submit Progress Report**
   - Go to "Progress Report" tab
   - Describe your work
   - Submit for extension

4. **Access Admin Dashboard**
   - Click "Admin Dashboard" button
   - View statistics
   - See applications list
   - Update configuration

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **QUICK_REFERENCE.md** | Quick lookup guide |
| **FULL_STACK_SETUP.md** | Detailed setup & deployment |
| **IMPLEMENTATION_SUMMARY.md** | What was built |
| **WIREFRAMES_GUIDE.md** | Wireframe version guide |
| **README.md** | Backend API docs |

---

## 🔧 Configuration

### Change Cutoff Scores
Edit `config.py`:
```python
DEFAULT_CUTOFF_SCORES = {
    "STEM": 65,        # Changed from 60
    "Business": 55,
    "Humanities": 50,
    "Arts": 45,
    "Other": 50
}
```

### Change License Period
Edit `config.py`:
```python
DEFAULT_LICENSE_PERIOD_DAYS = 120  # Changed from 90
```

### Adjust Scoring Weights
Edit `config.py`:
```python
SCORING_CRITERIA['degree_relevance']['max_points'] = 35  # Changed from 30
```

---

## 🧪 Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_scoring_engine.py -v

# With coverage
pytest tests/ --cov=services
```

---

## 🌐 API Examples

### Submit Application
```bash
curl -X POST http://localhost:5000/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.doe@mit.edu",
    "name": "Jane Doe",
    "institution": "MIT",
    "degree_program": "Computer Science",
    "degree_level": "graduate",
    "year": 2,
    "objective": "I want to use Claude for my NLP research...",
    "prior_claude_usage": "moderate",
    "financial_aid": true,
    "first_generation": false
  }'
```

### Get Statistics
```bash
curl http://localhost:5000/api/admin/statistics
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :5000

# Kill it
kill -9 <PID>
```

### Database Error
```bash
rm student_campaign.db
python app.py
```

### Import Error
```bash
pip install -r requirements.txt
```

---

## 📋 Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Application running on port 5000
- [ ] Frontend accessible at http://localhost:5000
- [ ] Can submit application
- [ ] Can view admin dashboard
- [ ] Tests passing

---

## 🎯 Next Steps

1. **Start the application** (see Quick Start above)
2. **Test the features** (submit app, view status, etc.)
3. **Review the code** (understand the architecture)
4. **Customize** (adjust scoring, cutoff scores, etc.)
5. **Deploy** (see FULL_STACK_SETUP.md)

---

## 💡 Key Differences from Wireframe

| Aspect | Wireframe | Real App |
|--------|-----------|----------|
| Data | Mock | Real Database |
| API | None | Full Integration |
| Scoring | Hardcoded | Calculated |
| Persistence | None | Database |
| Backend | None | Python Flask |

---

## 🎉 You're All Set!

Everything is ready to go. Just run the application and start testing!

**Questions?** Check the documentation files or review the code.

**Ready?** Let's go! 🚀

---

## 📞 Quick Links

- **Start Application**: `run.sh` or `run.bat`
- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api
- **Documentation**: See `*.md` files
- **Tests**: `pytest tests/ -v`

---

**Happy coding! 🎊**
