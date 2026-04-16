# Full-Stack Application Setup Guide

## Overview

This is a complete full-stack application with:
- **Frontend**: Interactive React-like HTML/CSS/JavaScript with real API integration
- **Backend**: Python Flask API with SQLAlchemy ORM
- **Database**: SQLite (development) or PostgreSQL (production)
- **Services**: Scoring engine, allocation engine, license manager, validator

## Directory Structure

```
student-campaign-system/
├── static/                    # Frontend (Real Application)
│   ├── index.html            # Main HTML
│   ├── styles.css            # Styling
│   ├── app.js                # Real app with API integration
│   └── script.js             # Wireframe version (preserved)
│
├── static-wireframe/         # Wireframe Version (Preserved)
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── app.py                    # Flask application
├── config.py                 # Configuration
├── models.py                 # Database models
├── requirements.txt          # Python dependencies
│
├── services/                 # Business logic
│   ├── validator.py
│   ├── scoring_engine.py
│   ├── allocation_engine.py
│   └── license_manager.py
│
├── routes/                   # API endpoints
│   ├── student_api.py
│   └── admin_api.py
│
└── tests/                    # Test suite
    ├── test_scoring_engine.py
    ├── test_allocation_engine.py
    └── test_license_manager.py
```

## Installation

### 1. Install Python Dependencies

```bash
cd student-campaign-system
pip install -r requirements.txt
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` if needed:
```
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///student_campaign.db
SECRET_KEY=your-secret-key-here
```

### 3. Initialize Database

```bash
python -c "from app import create_app; app = create_app(); print('✅ Database initialized')"
```

## Running the Application

### Start the Full-Stack Application

```bash
python app.py
```

This will:
- Start Flask server on `http://localhost:5000`
- Serve frontend from `http://localhost:5000`
- Serve API from `http://localhost:5000/api`
- Enable CORS for cross-origin requests

### Access the Application

Open your browser to: **http://localhost:5000**

## Features

### Student Portal

#### 1. Application Form
- Submit application with validation
- Real-time character counting
- Form validation before submission
- API integration for scoring and allocation

**Scoring Calculation:**
- Degree Relevance (0-30 points)
- Objective Quality (0-25 points)
- Academic Standing (0-20 points)
- Demonstrated Need (0-15 points)
- Claude Familiarity (0-10 points)

**Allocation Decision:**
- Score ≥ Cutoff → APPROVED (if licenses available)
- Score ≥ Cutoff + No licenses → WAITLISTED
- Score < Cutoff → REJECTED

#### 2. Application Status
- View application score breakdown
- See license details
- Check days remaining
- Submit progress reports

#### 3. Progress Report
- Submit progress report
- Get extension approval/rejection
- Track extension usage

### Admin Dashboard

#### 1. Overview
- Statistics cards (total, approved, rejected, waitlisted)
- License inventory tracking
- Score distribution chart
- Recent applications table

#### 2. Applications Management
- Filter by status, degree, score
- Search by student name
- View application details
- Bulk actions (approve, reject, export)

#### 3. Configuration
- Update cutoff scores per degree category
- Configure license settings
- Manage license inventory
- Adjust scoring weights

## API Endpoints

### Student Endpoints

```
POST   /api/applications
GET    /api/applications/<app_id>
GET    /api/applications/<app_id>/score
GET    /api/licenses/<license_id>
POST   /api/licenses/<license_id>/progress-reports
GET    /api/licenses/<license_id>/progress-reports
```

### Admin Endpoints

```
GET    /api/admin/applications
PATCH  /api/admin/applications/<app_id>
GET    /api/admin/statistics
GET    /api/admin/licenses
PATCH  /api/admin/licenses/<app_id>
GET    /api/admin/config/cutoff-scores
PUT    /api/admin/config/cutoff-scores
GET    /api/admin/inventory
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
pytest tests/test_scoring_engine.py -v
pytest tests/test_allocation_engine.py -v
pytest tests/test_license_manager.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=services --cov-report=html
```

## Example Usage

### 1. Submit Application

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
    "objective": "I want to use Claude for my NLP research thesis...",
    "prior_claude_usage": "moderate",
    "financial_aid": true,
    "first_generation": false
  }'
```

### 2. Get Application Status

```bash
curl http://localhost:5000/api/applications/<app_id>
```

### 3. Get Admin Statistics

```bash
curl http://localhost:5000/api/admin/statistics
```

### 4. Update Cutoff Scores

```bash
curl -X PUT http://localhost:5000/api/admin/config/cutoff-scores \
  -H "Content-Type: application/json" \
  -d '{
    "STEM": 65,
    "Business": 60
  }'
```

## Wireframe Version

The original wireframe (mock data, no backend) is preserved in `static-wireframe/`.

To run the wireframe:

```bash
python serve_static.py
```

Then open: **http://localhost:8000**

## Database Schema

### Students Table
- id (UUID)
- email (unique)
- name
- institution
- degree_program
- degree_level
- year
- financial_aid
- first_generation
- created_at, updated_at

### Applications Table
- id (UUID)
- student_id (FK)
- degree_program
- degree_category
- objective
- objective_category
- prior_claude_usage
- status
- score_total
- score_breakdown (JSON)
- cutoff_score_used
- created_at, updated_at, scored_at, decided_at

### Licenses Table
- id (UUID)
- application_id (FK)
- student_id (FK)
- claude_license_key
- start_date
- expiration_date
- extensions_granted
- total_extension_days
- status
- created_at, updated_at

### Progress Reports Table
- id (UUID)
- license_id (FK)
- description
- claude_usage_examples
- outcomes
- status
- submitted_at, reviewed_at
- reviewer_id
- rejection_reason
- extension_days_granted

## Configuration

### Scoring Weights

Edit `config.py` to adjust:
- Degree relevance points (0-30)
- Objective quality points (0-25)
- Academic standing points (0-20)
- Demonstrated need points (0-15)
- Claude familiarity points (0-10)

### Cutoff Scores

Default cutoff scores by degree category:
- STEM: 60
- Business: 55
- Humanities: 50
- Arts: 45
- Other: 50

### License Settings

- Default License Period: 90 days
- Max Extensions: 3 per license
- Max Total Extension Days: 90 days
- Extension Days per Report: 30 days
- Progress Quality Threshold: 70/100

## Deployment

### Production Setup

1. **Use PostgreSQL instead of SQLite:**
   ```
   DATABASE_URL=postgresql://user:password@localhost/student_campaign
   ```

2. **Set environment variables:**
   ```
   FLASK_ENV=production
   SECRET_KEY=<strong-random-key>
   ```

3. **Use production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
   ```

4. **Enable HTTPS:**
   - Use reverse proxy (nginx, Apache)
   - Install SSL certificate

5. **Set up monitoring:**
   - Application logs
   - Error tracking (Sentry)
   - Performance monitoring

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Database Errors

```bash
# Reset database
rm student_campaign.db
python -c "from app import create_app; app = create_app()"
```

### CORS Errors

- Ensure Flask-CORS is installed
- Check CORS configuration in app.py
- Verify frontend URL in CORS settings

### API Not Responding

- Check Flask server is running
- Verify port 5000 is accessible
- Check firewall settings
- Review server logs

## Performance Optimization

1. **Database Indexing:**
   - Email (unique)
   - Student ID (foreign key)
   - Application status
   - License expiration date

2. **Caching:**
   - Cache cutoff scores
   - Cache scoring criteria
   - Cache admin statistics

3. **Query Optimization:**
   - Use eager loading for relationships
   - Implement pagination
   - Add database indexes

## Security

1. **Authentication:**
   - Implement JWT tokens
   - Add password hashing
   - Session management

2. **Authorization:**
   - Role-based access control
   - Student can only see own data
   - Admin-only endpoints

3. **Data Protection:**
   - Encrypt sensitive data
   - HTTPS only
   - Rate limiting
   - Input validation

## Next Steps

1. **Frontend Enhancements:**
   - Add user authentication UI
   - Implement real-time notifications
   - Add data export (PDF, CSV)

2. **Backend Features:**
   - Email notifications
   - Audit logging
   - Advanced analytics
   - Batch processing

3. **DevOps:**
   - Docker containerization
   - CI/CD pipeline
   - Automated testing
   - Deployment automation

## Support

For issues or questions:
1. Check application logs
2. Review error messages
3. Check database state
4. Review API responses
5. Check browser console (F12)

## License

This is a prototype for the Student Campaign License Allocation System.
