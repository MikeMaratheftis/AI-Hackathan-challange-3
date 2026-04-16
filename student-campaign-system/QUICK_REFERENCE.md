# Quick Reference Guide

## 🚀 Start the Application

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

**Then open:** http://localhost:5000

---

## 📁 File Locations

| What | Where |
|------|-------|
| Frontend (Real) | `static/index.html` + `static/app.js` |
| Frontend (Wireframe) | `static-wireframe/index.html` + `static-wireframe/script.js` |
| Backend | `app.py` |
| Database Models | `models.py` |
| Services | `services/` |
| API Routes | `routes/` |
| Tests | `tests/` |
| Configuration | `config.py` |

---

## 🎯 Key Features

### Student Portal
- **Apply**: Submit application with scoring
- **Status**: View score breakdown and license
- **Progress**: Submit progress reports for extensions

### Admin Dashboard
- **Overview**: Statistics and charts
- **Applications**: Filter and manage applications
- **Configuration**: Update settings and cutoff scores

---

## 🔌 API Examples

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

### Update Cutoff Scores
```bash
curl -X PUT http://localhost:5000/api/admin/config/cutoff-scores \
  -H "Content-Type: application/json" \
  -d '{"STEM": 65, "Business": 60}'
```

---

## 📊 Scoring System

| Criterion | Points | Details |
|-----------|--------|---------|
| Degree Relevance | 0-30 | STEM=30, Business=25, Humanities=20, Arts=15, Other=10 |
| Objective Quality | 0-25 | Specificity (10) + Feasibility (8) + Relevance (7) |
| Academic Standing | 0-20 | Graduate=20, Senior=15, Junior=12, Sophomore=8, Freshman=5 |
| Demonstrated Need | 0-15 | Financial Aid (8) + First Gen (4) + Underrepresented (3) |
| Claude Familiarity | 0-10 | Experienced=10, Moderate=7, Beginner=4, None=0 |

**Total: 0-100 points**

---

## 🎓 Cutoff Scores

| Degree Category | Cutoff |
|-----------------|--------|
| STEM | 60 |
| Business | 55 |
| Humanities | 50 |
| Arts | 45 |
| Other | 50 |

---

## 📅 License Settings

| Setting | Value |
|---------|-------|
| Default Period | 90 days |
| Max Extensions | 3 |
| Max Total Extension Days | 90 days |
| Extension Days per Report | 30 days |
| Progress Quality Threshold | 70/100 |

---

## 🧪 Testing

```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_scoring_engine.py -v

# With coverage
pytest tests/ --cov=services
```

---

## 🗄️ Database

### Reset Database
```bash
rm student_campaign.db
python -c "from app import create_app; app = create_app()"
```

### View Database
```bash
sqlite3 student_campaign.db
.tables
.schema students
```

---

## 🔧 Configuration

Edit `config.py` to change:
- Scoring weights
- Cutoff scores
- License settings
- Database URL
- Secret key

---

## 📱 Wireframe Version

Run the original wireframe (mock data):
```bash
python serve_static.py
```

Open: http://localhost:8000

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :5000

# Kill process
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

### CORS Error
- Check Flask-CORS is installed
- Verify CORS config in app.py

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `FULL_STACK_SETUP.md` | Detailed setup and deployment |
| `IMPLEMENTATION_SUMMARY.md` | What was built and how |
| `WIREFRAMES_GUIDE.md` | Wireframe version guide |
| `README.md` | Backend API documentation |
| `QUICK_REFERENCE.md` | This file |

---

## 🎯 Common Tasks

### Add New Cutoff Score
```python
# In app.py or via API
app.allocation_engine.update_cutoff_score('STEM', 65)
```

### Change License Period
```python
# In config.py
DEFAULT_LICENSE_PERIOD_DAYS = 120
```

### Adjust Scoring Weights
```python
# In config.py
SCORING_CRITERIA['degree_relevance']['max_points'] = 35
```

---

## 📞 Support

1. Check documentation files
2. Review application logs
3. Check browser console (F12)
4. Review API responses
5. Check database state

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created
- [ ] Database initialized
- [ ] Application running on port 5000
- [ ] Frontend accessible at http://localhost:5000
- [ ] Can submit application
- [ ] Can view admin dashboard
- [ ] Tests passing (`pytest tests/ -v`)

---

## 🚀 Next Steps

1. **Test the application**
   - Submit applications
   - View scores
   - Submit progress reports

2. **Review the code**
   - Understand scoring logic
   - Review API endpoints
   - Check database models

3. **Customize**
   - Adjust scoring weights
   - Change cutoff scores
   - Modify license settings

4. **Deploy**
   - Set up production database
   - Configure environment variables
   - Deploy to server

---

**Happy coding! 🎉**
