# Design Document: Student Campaign License Allocation System

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Student Campaign System                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │  Student Portal │    │ Admin Dashboard │    │   API Gateway   │         │
│  │   (Frontend)    │    │   (Frontend)    │    │                 │         │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘         │
│           │                      │                      │                   │
│           └──────────────────────┼──────────────────────┘                   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         Application Services                           │ │
│  ├───────────────┬───────────────┬───────────────┬───────────────────────┤ │
│  │   Validator   │ Scoring_Engine│Allocation_Eng.│   License_Manager     │ │
│  └───────┬───────┴───────┬───────┴───────┬───────┴───────────┬───────────┘ │
│          │               │               │                   │             │
│          └───────────────┴───────────────┴───────────────────┘             │
│                                  │                                          │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                           Data Layer                                   │ │
│  ├─────────────────┬─────────────────┬─────────────────┬─────────────────┤ │
│  │  Applications   │    Licenses     │    Students     │   Audit_Logs    │ │
│  │     Store       │     Store       │     Store       │                 │ │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **Validator** | Verifies student identity, enrollment, degree program, and objectives |
| **Scoring_Engine** | Calculates application scores based on weighted criteria |
| **Allocation_Engine** | Allocates licenses to qualifying students, manages waitlist |
| **License_Manager** | Tracks license periods, processes extensions, manages expirations |

---

## 2. Decision Engine Design

### 2.1 Scoring Engine Logic

#### 2.1.1 Scoring Criteria and Weights

```python
SCORING_CRITERIA = {
    "degree_relevance": {
        "max_points": 30,
        "weights": {
            "STEM": 30,           # Computer Science, Engineering, Math, Sciences
            "Business": 25,       # MBA, Economics, Finance
            "Humanities": 20,     # Literature, History, Philosophy
            "Arts": 15,           # Fine Arts, Music, Design
            "Other": 10           # Uncategorized programs
        }
    },
    "objective_quality": {
        "max_points": 25,
        "factors": {
            "specificity": 10,     # Clear, detailed goal description
            "feasibility": 8,      # Realistic and achievable
            "relevance": 7         # Aligned with Claude capabilities
        }
    },
    "academic_standing": {
        "max_points": 20,
        "weights": {
            "graduate": 20,        # Masters, PhD students
            "undergraduate_senior": 15,
            "undergraduate_junior": 12,
            "undergraduate_sophomore": 8,
            "undergraduate_freshman": 5
        }
    },
    "demonstrated_need": {
        "max_points": 15,
        "factors": {
            "financial_aid": 8,    # Receives financial aid
            "first_gen": 4,        # First-generation student
            "underrepresented": 3  # Underrepresented in field
        }
    },
    "claude_familiarity": {
        "max_points": 10,
        "weights": {
            "experienced": 10,     # Used Claude extensively
            "moderate": 7,         # Used Claude occasionally
            "beginner": 4,         # New to Claude
            "none": 0              # No prior experience
        }
    }
}
```

#### 2.1.2 Score Calculation Algorithm

```
FUNCTION calculate_score(application):
    total_score = 0
    breakdown = {}
    
    // 1. Degree Relevance Score
    degree_category = classify_degree(application.degree_program)
    breakdown.degree_relevance = SCORING_CRITERIA.degree_relevance.weights[degree_category]
    total_score += breakdown.degree_relevance
    
    // 2. Objective Quality Score
    objective_score = evaluate_objective(application.objective)
    breakdown.objective_quality = objective_score
    total_score += objective_score
    
    // 3. Academic Standing Score
    standing = determine_academic_standing(application.year, application.degree_level)
    breakdown.academic_standing = SCORING_CRITERIA.academic_standing.weights[standing]
    total_score += breakdown.academic_standing
    
    // 4. Demonstrated Need Score
    need_score = calculate_need_score(application.financial_aid, application.first_gen, application.demographics)
    breakdown.demonstrated_need = need_score
    total_score += need_score
    
    // 5. Claude Familiarity Score
    familiarity = assess_familiarity(application.prior_usage)
    breakdown.claude_familiarity = SCORING_CRITERIA.claude_familiarity.weights[familiarity]
    total_score += breakdown.claude_familiarity
    
    RETURN {
        total: min(total_score, 100),
        breakdown: breakdown,
        calculated_at: current_timestamp()
    }
```

#### 2.1.3 Objective Quality Evaluation

```
FUNCTION evaluate_objective(objective):
    score = 0
    
    // Specificity (0-10 points)
    word_count = count_words(objective.description)
    IF word_count >= 200: specificity = 10
    ELSE IF word_count >= 150: specificity = 8
    ELSE IF word_count >= 100: specificity = 6
    ELSE IF word_count >= 50: specificity = 4
    ELSE: specificity = 0
    score += specificity
    
    // Feasibility (0-8 points)
    has_timeline = contains_timeline(objective.description)
    has_deliverables = contains_deliverables(objective.description)
    feasibility = (has_timeline ? 4 : 0) + (has_deliverables ? 4 : 0)
    score += feasibility
    
    // Relevance (0-7 points)
    use_case = classify_use_case(objective.description)
    relevance_weights = {
        "Research": 7,
        "Thesis": 7,
        "Project": 6,
        "Coursework": 5,
        "Other": 3
    }
    score += relevance_weights[use_case]
    
    RETURN score
```

### 2.2 Allocation Engine Logic

#### 2.2.1 Allocation Decision Flow

```
FUNCTION process_allocation(application, score):
    // Get current cutoff score
    cutoff = get_cutoff_score(application.degree_category)
    
    // Check license inventory
    available_licenses = get_available_license_count()
    
    IF score.total >= cutoff:
        IF available_licenses > 0:
            license = create_license(application.student_id)
            update_status(application, "APPROVED")
            send_notification(application.student, "APPROVED", license)
            RETURN license
        ELSE:
            add_to_waitlist(application)
            update_status(application, "WAITLISTED")
            send_notification(application.student, "WAITLISTED")
            RETURN waitlist_entry
    ELSE:
        update_status(application, "REJECTED")
        send_notification(application.student, "REJECTED", score.breakdown)
        RETURN rejection_record
```

#### 2.2.2 Cutoff Score Configuration

```
DEFAULT_CUTOFF_SCORES = {
    "STEM": 60,
    "Business": 55,
    "Humanities": 50,
    "Arts": 45,
    "Other": 50
}

FUNCTION get_cutoff_score(degree_category):
    // Check for admin override
    override = get_admin_cutoff_override()
    IF override AND override.category == degree_category:
        RETURN override.value
    
    // Return default for category
    RETURN DEFAULT_CUTOFF_SCORES[degree_category]
```

### 2.3 License Manager Logic

#### 2.3.1 License Period Management

```
FUNCTION create_license(student_id):
    license = {
        id: generate_uuid(),
        student_id: student_id,
        start_date: current_date(),
        expiration_date: current_date() + DEFAULT_LICENSE_PERIOD_DAYS,
        extensions_granted: 0,
        total_extension_days: 0,
        status: "ACTIVE"
    }
    store_license(license)
    schedule_expiration_notifications(license)
    RETURN license

FUNCTION schedule_expiration_notifications(license):
    // 14 days before
    schedule_notification(
        license.student_id,
        "LICENSE_EXPIRING",
        license.expiration_date - 14
    )
    // 7 days before
    schedule_notification(
        license.student_id,
        "LICENSE_EXPIRING_URGENT",
        license.expiration_date - 7
    )
    // On expiration
    schedule_notification(
        license.student_id,
        "LICENSE_EXPIRED",
        license.expiration_date
    )
```

#### 2.3.2 Extension Evaluation Logic

```
FUNCTION evaluate_extension_request(license_id, progress_report):
    license = get_license(license_id)
    
    // Check extension limits
    IF license.extensions_granted >= MAX_EXTENSIONS:
        RETURN {
            approved: false,
            reason: "Maximum extensions reached"
        }
    
    IF license.total_extension_days >= MAX_TOTAL_EXTENSION_DAYS:
        RETURN {
            approved: false,
            reason: "Maximum extension days reached"
        }
    
    // Validate progress report
    validation = validate_progress_report(progress_report)
    IF NOT validation.valid:
        RETURN {
            approved: false,
            reason: validation.errors
        }
    
    // Evaluate progress quality
    quality_score = evaluate_progress_quality(progress_report)
    
    IF quality_score >= PROGRESS_QUALITY_THRESHOLD:
        extension_days = min(EXTENSION_DAYS_PER_REPORT, 
                            MAX_TOTAL_EXTENSION_DAYS - license.total_extension_days)
        
        license.expiration_date += extension_days
        license.extensions_granted += 1
        license.total_extension_days += extension_days
        update_license(license)
        
        RETURN {
            approved: true,
            extension_days: extension_days,
            new_expiration: license.expiration_date
        }
    ELSE:
        RETURN {
            approved: false,
            reason: "Progress report does not demonstrate sufficient progress"
        }
```

#### 2.3.3 Progress Report Validation

```
FUNCTION validate_progress_report(report):
    errors = []
    
    // Check minimum description length
    IF length(report.description) < 100:
        errors.append("Description must be at least 100 characters")
    
    // Check for Claude usage examples
    IF NOT contains_claude_usage_examples(report.description):
        errors.append("Report must include specific Claude usage examples")
    
    // Check for outcomes/deliverables
    IF NOT contains_outcomes(report.description):
        errors.append("Report must describe outcomes or deliverables achieved")
    
    // Check submission timing
    license = get_license(report.license_id)
    days_until_expiration = license.expiration_date - current_date()
    IF days_until_expiration > 30:
        errors.append("Progress report can only be submitted within 30 days of expiration")
    
    RETURN {
        valid: length(errors) == 0,
        errors: errors
    }
```

---

## 3. Data Model

### 3.1 Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Student      │       │   Application   │       │     License     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id              │──┐    │ id              │──┐    │ id              │
│ email           │  │    │ student_id (FK) │  │    │ application_id  │
│ name            │  └───>│ degree_program  │  └───>│ student_id (FK) │
│ institution     │       │ objective       │       │ start_date      │
│ degree_level    │       │ status          │       │ expiration_date │
│ year            │       │ score_total     │       │ extensions      │
│ created_at      │       │ score_breakdown │       │ status          │
│ updated_at      │       │ cutoff_score    │       │ created_at      │
└─────────────────┘       │ created_at      │       │ updated_at      │
                          │ updated_at      │       └─────────────────┘
                          └─────────────────┘                │
                                    │                        │
                                    │                        ▼
                                    │              ┌─────────────────┐
                                    │              │ Progress_Report │
                                    │              ├─────────────────┤
                                    │              │ id              │
                                    └─────────────>│ license_id (FK) │
                                                   │ description     │
                                                   │ status          │
                                                   │ submitted_at    │
                                                   │ reviewed_at     │
                                                   │ extension_days  │
                                                   └─────────────────┘
```

### 3.2 Schema Definitions

#### Student Schema
```json
{
  "id": "uuid",
  "email": "string (unique, indexed)",
  "name": "string",
  "institution": "string",
  "institution_domain": "string",
  "degree_program": "string",
  "degree_level": "enum[undergraduate, graduate, phd]",
  "year": "integer",
  "financial_aid": "boolean",
  "first_generation": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Application Schema
```json
{
  "id": "uuid",
  "student_id": "uuid (FK)",
  "degree_program": "string",
  "degree_category": "enum[STEM, Business, Humanities, Arts, Other]",
  "objective": "text",
  "objective_category": "enum[Research, Thesis, Project, Coursework, Other]",
  "prior_claude_usage": "enum[experienced, moderate, beginner, none]",
  "status": "enum[submitted, under_review, verified, scored, approved, rejected, waitlisted]",
  "score_total": "integer (0-100)",
  "score_breakdown": {
    "degree_relevance": "integer",
    "objective_quality": "integer",
    "academic_standing": "integer",
    "demonstrated_need": "integer",
    "claude_familiarity": "integer"
  },
  "cutoff_score_used": "integer",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "scored_at": "timestamp",
  "decided_at": "timestamp"
}
```

#### License Schema
```json
{
  "id": "uuid",
  "application_id": "uuid (FK)",
  "student_id": "uuid (FK)",
  "claude_license_key": "string (encrypted)",
  "start_date": "date",
  "expiration_date": "date",
  "extensions_granted": "integer (default: 0)",
  "total_extension_days": "integer (default: 0)",
  "status": "enum[active, expired, revoked]",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Progress Report Schema
```json
{
  "id": "uuid",
  "license_id": "uuid (FK)",
  "description": "text",
  "claude_usage_examples": "text",
  "outcomes": "text",
  "status": "enum[pending, approved, rejected]",
  "submitted_at": "timestamp",
  "reviewed_at": "timestamp",
  "reviewer_id": "uuid",
  "rejection_reason": "text",
  "extension_days_granted": "integer"
}
```

---

## 4. API Design

### 4.1 Student API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/applications` | Submit new application |
| GET | `/api/applications/{id}` | Get application status |
| GET | `/api/applications/{id}/score` | Get score breakdown |
| GET | `/api/licenses/{id}` | Get license details |
| POST | `/api/licenses/{id}/progress-reports` | Submit progress report |
| GET | `/api/licenses/{id}/progress-reports` | List progress reports |

### 4.2 Admin API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/applications` | List applications (filterable) |
| PATCH | `/api/admin/applications/{id}` | Update application status |
| GET | `/api/admin/statistics` | Get aggregate statistics |
| GET | `/api/admin/licenses` | List licenses (filterable) |
| PATCH | `/api/admin/licenses/{id}` | Update license |
| GET | `/api/admin/config/cutoff-scores` | Get cutoff score config |
| PUT | `/api/admin/config/cutoff-scores` | Update cutoff scores |
| GET | `/api/admin/inventory` | Get license inventory |

---

## 5. Wireframe Specifications

### 5.1 Student Portal Wireframes

#### 5.1.1 Application Form Page

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Logo]  Claude for Students                           [Help] [Sign Out]│
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Apply for Claude License                                              │
│  ─────────────────────────────────────────────────────────────────────│
│                                                                        │
│  Personal Information                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Full Name: [________________________________]                     │ │
│  │ Email:     [________________________________]  ✓ .edu verified    │ │
│  │ Institution: [Dropdown: Select Institution_______________▼]      │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Academic Information                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Degree Program: [Dropdown: Select Program_________________▼]     │ │
│  │ Degree Level:   ( ) Undergraduate  ( ) Graduate  ( ) PhD         │ │
│  │ Year:           ( ) Freshman ( ) Soph ( ) Junior ( ) Senior      │ │
│  │                                                                  │ │
│  │ [ ] I receive financial aid                                      │ │
│  │ [ ] I am a first-generation student                              │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Your Objective                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Describe how you plan to use Claude (min 50 characters):         │ │
│  │                                                                  │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  │                                                                  │ │
│  │ Characters: 0/500 minimum                                        │ │
│  │                                                                  │ │
│  │ Use Case Category: [Dropdown: Select Category_____________▼]     │ │
│  │                                                                  │ │
│  │ Prior Claude Experience:                                         │ │
│  │ ( ) Extensive - I use Claude regularly                          │ │
│  │ ( ) Moderate - I've used Claude occasionally                    │ │
│  │ ( ) Beginner - I'm new to Claude                                │ │
│  │ ( ) None - I haven't used Claude yet                            │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│                              [Submit Application]                       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

#### 5.1.2 Application Status Page

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Logo]  Claude for Students                           [Help] [Sign Out]│
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  My Application                                                        │
│  ─────────────────────────────────────────────────────────────────────│
│                                                                        │
│  Status: [✓ APPROVED]                    Applied: January 15, 2025    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Score Breakdown                              Total: 72/100        │ │
│  │ ────────────────────────────────────────────────────────────────│ │
│  │                                                                  │ │
│  │ Degree Relevance      ████████████████████████████████░░░░ 30/30│ │
│  │ Objective Quality     ███████████████████████░░░░░░░░░░░░░ 22/25│ │
│  │ Academic Standing     ████████████████████░░░░░░░░░░░░░░░ 15/20│ │
│  │ Demonstrated Need     ████████████░░░░░░░░░░░░░░░░░░░░░░░  5/15│ │
│  │ Claude Familiarity    ████████████████░░░░░░░░░░░░░░░░░░░░  0/10│ │
│  │                                                                  │ │
│  │ Cutoff Score: 60          Your Score: 72                        │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  License Details                                                       │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ License ID: CLAUDE-STU-2025-ABC123                               │ │
│  │ Status: [● ACTIVE]                                               │ │
│  │ Start Date: January 20, 2025                                     │ │
│  │ Expiration: April 20, 2025                                       │ │
│  │ Days Remaining: 85                                               │ │
│  │ Extensions Used: 0/3                                             │ │
│  │                                                                  │ │
│  │ [Submit Progress Report for Extension]                           │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

#### 5.1.3 Progress Report Submission Page

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Logo]  Claude for Students                           [Help] [Sign Out]│
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Submit Progress Report                                                │
│  ─────────────────────────────────────────────────────────────────────│
│                                                                        │
│  License: CLAUDE-STU-2025-ABC123                                       │
│  Current Expiration: April 20, 2025                                    │
│  Extensions Available: 3                                               │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Project Description (min 100 characters):                        │ │
│  │                                                                  │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  │                                                                  │ │
│  │ Characters: 0/1000                                               │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ How did you use Claude? (specific examples):                     │ │
│  │                                                                  │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Outcomes/Deliverables Achieved:                                  │ │
│  │                                                                  │ │
│  │ [________________________________________________________]       │ │
│  │ [________________________________________________________]       │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  [ ] I confirm this report accurately reflects my progress            │
│                                                                        │
│                              [Submit Progress Report]                   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Administrator Dashboard Wireframes

#### 5.2.1 Main Dashboard

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Logo]  Claude Campaign Admin          [Config] [Reports] [Sign Out] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Dashboard Overview                                    January 2025    │
│  ─────────────────────────────────────────────────────────────────────│
│                                                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │   Total      │ │   Approved   │ │   Rejected   │ │  Waitlisted  │  │
│  │    1,247     │ │     892      │ │     289      │ │      66      │  │
│  │ Applications │ │   (71.5%)    │ │   (23.2%)    │ │    (5.3%)    │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘  │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ License Inventory                                                │ │
│  │ ────────────────────────────────────────────────────────────────│ │
│  │ Total Allocated: 892    Active: 845    Expired: 47              │ │
│  │ Available: 108          Total Pool: 1000                        │ │
│  │                                                                  │ │
│  │ [████████████████████████████████████████████████░░░░░░] 89.2%  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Score Distribution                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │                                                                  │ │
│  │   100│                    ██                                     │ │
│  │    90│                  ██████                                   │ │
│  │    80│                ██████████                                 │ │
│  │    70│              ██████████████                               │ │
│  │    60│            ██████████████████ ← Cutoff                    │ │
│  │    50│          ██████████████████████                           │ │
│  │    40│        ██████████████████████████                         │ │
│  │    30│      ██████████████████████████████                       │ │
│  │    20│    ██████████████████████████████████                     │ │
│  │    10│  ██████████████████████████████████████                   │ │
│  │     0└────────────────────────────────────────────────────────── │ │
│  │                                                                  │ │
│  │   Average Score: 62.4    Median: 58    Std Dev: 15.2            │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Recent Applications                        [View All →]              │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Student          │ Institution    │ Score │ Status   │ Date     │ │
│  │ ─────────────────┼────────────────┼───────┼──────────┼─────────│ │
│  │ Jane Doe         │ MIT            │  78   │ Approved │ Jan 20   │ │
│  │ John Smith       │ Stanford       │  45   │ Rejected │ Jan 20   │ │
│  │ Alex Johnson     │ Berkeley       │  65   │ Approved │ Jan 20   │ │
│  │ Sarah Williams   │ Harvard        │  72   │ Approved │ Jan 20   │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

#### 5.2.2 Application Management View

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Logo]  Claude Campaign Admin          [Config] [Reports] [Sign Out] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Applications                                                          │
│  ─────────────────────────────────────────────────────────────────────│
│                                                                        │
│  Filters:                                                              │
│  [Status: All ▼] [Degree: All ▼] [Score Range: All ▼] [Date: All ▼]  │
│  [Search: _____________________________] [Apply Filters]               │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ [ ]│ Student      │ Institution │ Degree    │ Score │ Status    │ │
│  │ ───┼──────────────┼─────────────┼───────────┼───────┼───────────│ │
│  │ [ ]│ Jane Doe     │ MIT         │ CS (PhD)  │  78   │ ✓Approved │ │
│  │ [ ]│ John Smith   │ Stanford    │ MBA       │  45   │ ✗Rejected │ │
│  │ [ ]│ Alex Johnson │ Berkeley    │ Physics   │  65   │ ✓Approved │ │
│  │ [ ]│ Sarah Will.  │ Harvard     │ Economics │  72   │ ✓Approved │ │
│  │ [ ]│ Mike Brown   │ UCLA        │ History   │  58   │ ⏳Waitlist│ │
│  │ [ ]│ Emily Davis  │ Columbia    │ Biology   │  81   │ ✓Approved │ │
│  │                                                                  │ │
│  │ Showing 1-25 of 1,247                    [< Prev] [1] [2] [3] [>]│ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  [Export CSV]  [Bulk Approve]  [Bulk Reject]                          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

#### 5.2.3 Configuration Panel

```
┌────────────────────────────────────────────────────────────────────────┐
│  [Logo]  Claude Campaign Admin          [Config] [Reports] [Sign Out] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Configuration                                                         │
│  ─────────────────────────────────────────────────────────────────────│
│                                                                        │
│  Cutoff Scores by Degree Category                                      │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │                                                                  │ │
│  │ STEM:        [____60____] points                                 │ │
│  │ Business:    [____55____] points                                 │ │
│  │ Humanities:  [____50____] points                                 │ │
│  │ Arts:        [____45____] points                                 │ │
│  │ Other:       [____50____] points                                 │ │
│  │                                                                  │ │
│  │                              [Reset to Defaults] [Save Changes]  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  License Settings                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Default License Period:     [____90____] days                    │ │
│  │ Max Extensions per License: [____3_____]                         │ │
│  │ Max Total Extension Days:   [____90____] days                    │ │
│  │ Extension Days per Report:  [____30____] days                    │ │
│  │                                                                  │ │
│  │                              [Reset to Defaults] [Save Changes]  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  License Inventory                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Total License Pool: [____1000____]                               │ │
│  │                                                                  │ │
│  │                              [Update Inventory]                  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Scoring Weights                                                       │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Degree Relevance:      [____30____] points (max)                 │ │
│  │ Objective Quality:     [____25____] points (max)                 │ │
│  │ Academic Standing:     [____20____] points (max)                 │ │
│  │ Demonstrated Need:     [____15____] points (max)                 │ │
│  │ Claude Familiarity:    [____10____] points (max)                 │ │
│  │                                                                  │ │
│  │                              [Reset to Defaults] [Save Changes]  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Correctness Properties

### 6.1 Prework Analysis

#### 6.1.1 Score Calculation Properties

**Property 1: Score Bounds**
- **Thoughts**: The score calculation must always produce values within the defined range. This is testable as a property by generating random application data and verifying the output is always 0-100.
- **Testable**: yes - property

**Property 2: Score Component Sum**
- **Thoughts**: The total score should equal the sum of all component scores. This is an invariant that can be tested with property-based testing.
- **Testable**: yes - property

**Property 3: Score Determinism**
- **Thoughts**: The same application input should always produce the same score. This is testable as an idempotence property.
- **Testable**: yes - property

#### 6.1.2 Allocation Properties

**Property 4: Cutoff Score Enforcement**
- **Thoughts**: Applications with scores below cutoff should never be approved. This is testable with property-based testing by generating applications with various scores.
- **Testable**: yes - property

**Property 5: License Inventory Conservation**
- **Thoughts**: The number of allocated licenses plus available licenses should equal the total pool. This is an invariant that can be tested.
- **Testable**: yes - property

**Property 6: Waitlist Ordering**
- **Thoughts**: When licenses become available, waitlisted applications should be processed in score order (or submission order for ties). This is testable as a confluence property.
- **Testable**: yes - property

#### 6.1.3 License Management Properties

**Property 7: Extension Limits**
- **Thoughts**: Extensions should never exceed the configured maximums (3 extensions, 90 total days). This is an invariant that can be tested.
- **Testable**: yes - property

**Property 8: Expiration Date Calculation**
- **Thoughts**: After extensions, the new expiration date should equal the original plus extension days granted. This is testable as a round-trip property.
- **Testable**: yes - property

**Property 9: Progress Report Timing**
- **Thoughts**: Progress reports submitted{}