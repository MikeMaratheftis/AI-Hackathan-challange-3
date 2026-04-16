# Student Campaign License Allocation System

A Python-based system for managing Claude license allocation to students based on validated applications and scoring mechanisms.

## Project Structure

```
student-campaign-system/
├── app.py                 # Flask application factory
├── config.py             # Configuration settings
├── models.py             # SQLAlchemy data models
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
│
├── services/             # Business logic services
│   ├── validator.py      # Application validation
│   ├── scoring_engine.py # Score calculation
│   ├── allocation_engine.py # License allocation
│   └── license_manager.py   # License management
│
├── routes/               # API endpoints
│   ├── student_api.py    # Student-facing endpoints
│   └── admin_api.py      # Admin endpoints
│
└── tests/                # Test suite
    ├── test_scoring_engine.py
    ├── test_allocation_engine.py
    └── test_license_manager.py
```

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Run the application:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Student Endpoints

- `POST /api/applications` - Submit new application
- `GET /api/applications/<app_id>` - Get application status
- `GET /api/licenses/<license_id>` - Get license details
- `POST /api/licenses/<license_id>/progress-reports` - Submit progress report

### Admin Endpoints

- `GET /api/admin/applications` - List applications with filtering
- `GET /api/admin/statistics` - Get aggregate statistics
- `GET /api/admin/config/cutoff-scores` - Get cutoff scores
- `PUT /api/admin/config/cutoff-scores` - Update cutoff scores
- `GET /api/admin/inventory` - Get license inventory status

## Running Tests

```bash
pytest tests/ -v
```

## Scoring Mechanism

Applications are scored on 5 criteria (0-100 total):

1. **Degree Relevance** (0-30 points)
   - STEM: 30 points
   - Business: 25 points
   - Humanities: 20 points
   - Arts: 15 points
   - Other: 10 points

2. **Objective Quality** (0-25 points)
   - Specificity: 0-10 points
   - Feasibility: 0-8 points
   - Relevance: 0-7 points

3. **Academic Standing** (0-20 points)
   - Graduate: 20 points
   - Undergraduate Senior: 15 points
   - Undergraduate Junior: 12 points
   - Undergraduate Sophomore: 8 points
   - Undergraduate Freshman: 5 points

4. **Demonstrated Need** (0-15 points)
   - Financial Aid: 8 points
   - First Generation: 4 points
   - Underrepresented: 3 points

5. **Claude Familiarity** (0-10 points)
   - Experienced: 10 points
   - Moderate: 7 points
   - Beginner: 4 points
   - None: 0 points

## Cutoff Scores

Default cutoff scores by degree category:
- STEM: 60
- Business: 55
- Humanities: 50
- Arts: 45
- Other: 50

## License Management

- **Default Period:** 90 days
- **Max Extensions:** 3 per license
- **Max Total Extension Days:** 90 days
- **Extension Days per Report:** 30 days
- **Progress Quality Threshold:** 70/100

## Property-Based Testing

The system includes property-based tests for core invariants:

1. **Score Bounds Property:** Scores always 0-100
2. **Score Component Sum:** Breakdown sum equals total
3. **Score Determinism:** Same input produces same score
4. **Cutoff Enforcement:** Below cutoff never approved
5. **Inventory Conservation:** Allocated + Available = Total
6. **Extension Limits:** Never exceed configured maximums

## Example Usage

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
    "objective": "I want to use Claude for my NLP research thesis...",
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
  -d '{
    "STEM": 65,
    "Business": 60
  }'
```

## Implementation Status

- ✅ Phase 1: Foundation & Infrastructure
- ✅ Phase 2: Core Services (Validator, Scoring, Allocation, License Manager)
- ✅ Phase 3: API Layer (Student & Admin endpoints)
- ⏳ Phase 4: Frontend - Student Portal
- ⏳ Phase 5: Frontend - Admin Dashboard
- ⏳ Phase 6: Integration & Testing
- ⏳ Phase 7: Deployment & Documentation
