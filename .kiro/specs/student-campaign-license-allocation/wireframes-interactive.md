# Interactive Wireframes - Student Campaign License Allocation System

## Student Portal Wireframes

### 1. Application Form Page

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Claude for Students                                    [Help] [Sign Out]│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Apply for Claude License                                               │
│  ═════════════════════════════════════════════════════════════════════ │
│                                                                         │
│  📋 Personal Information                                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Full Name:                                                      │   │
│  │ [Jane Doe_________________________________]                    │   │
│  │                                                                 │   │
│  │ Email:                                                          │   │
│  │ [jane.doe@mit.edu_____________________] ✓ .edu verified        │   │
│  │                                                                 │   │
│  │ Institution:                                                    │   │
│  │ [Massachusetts Institute of Technology ▼]                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  🎓 Academic Information                                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Degree Program:                                                 │   │
│  │ [Computer Science_____________________▼]                        │   │
│  │                                                                 │   │
│  │ Degree Level:                                                   │   │
│  │ ◉ Undergraduate  ○ Graduate  ○ PhD                              │   │
│  │                                                                 │   │
│  │ Year:                                                           │   │
│  │ ○ Freshman  ○ Sophomore  ○ Junior  ◉ Senior                    │   │
│  │                                                                 │   │
│  │ ☑ I receive financial aid                                       │   │
│  │ ☐ I am a first-generation student                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  🎯 Your Objective                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Describe how you plan to use Claude (minimum 50 characters):    │   │
│  │                                                                 │   │
│  │ I plan to use Claude to assist with my research on natural     │   │
│  │ language processing and machine learning. Specifically, I want  │   │
│  │ to leverage Claude's capabilities to help me understand        │   │
│  │ complex NLP concepts, debug my code, and generate test cases    │   │
│  │ for my thesis project on sentiment analysis using transformer   │   │
│  │ models.                                                         │   │
│  │                                                                 │   │
│  │ Characters: 287/500 ✓                                           │   │
│  │                                                                 │   │
│  │ Use Case Category:                                              │   │
│  │ [Thesis_____________________________▼]                          │   │
│  │                                                                 │   │
│  │ Prior Claude Experience:                                        │   │
│  │ ○ Extensive - I use Claude regularly                            │   │
│  │ ◉ Moderate - I've used Claude occasionally                      │   │
│  │ ○ Beginner - I'm new to Claude                                  │   │
│  │ ○ None - I haven't used Claude yet                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│                          [Submit Application]                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Sample Data Used:**
- Student: Jane Doe (STU-001)
- Institution: MIT
- Degree: Computer Science (Graduate)
- Objective: NLP/ML research thesis

---

### 2. Application Status Page

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Claude for Students                                    [Help] [Sign Out]│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  My Application                                                         │
│  ═════════════════════════════════════════════════════════════════════ │
│                                                                         │
│  Status: ✅ APPROVED                          Applied: January 10, 2025│
│                                                                         │
│  📊 Score Breakdown                                    Total: 78/100    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                                                                 │   │
│  │ Degree Relevance                                                │   │
│  │ ████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │
│  │ 30/30 points                                                    │   │
│  │                                                                 │   │
│  │ Objective Quality                                               │   │
│  │ ███████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │
│  │ 22/25 points - Clear, detailed goal with feasible timeline      │   │
│  │                                                                 │   │
│  │ Academic Standing                                               │   │
│  │ ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │
│  │ 20/20 points - Graduate student (Masters)                       │   │
│  │                                                                 │   │
│  │ Demonstrated Need                                               │   │
│  │ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │
│  │ 4/15 points - Receives financial aid                            │   │
│  │                                                                 │   │
│  │ Claude Familiarity                                              │   │
│  │ ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │
│  │ 7/10 points - Moderate prior experience                         │   │
│  │                                                                 │   │
│  │ ─────────────────────────────────────────────────────────────  │   │
│  │ Cutoff Score: 60  |  Your Score: 78  |  Status: ✅ APPROVED    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  🔑 License Details                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ License ID:        CLAUDE-STU-2025-ABC123                       │   │
│  │ Status:            ● ACTIVE                                     │   │
│  │ Start Date:        January 20, 2025                             │   │
│  │ Expiration Date:   April 20, 2025                               │   │
│  │ Days Remaining:    85 days                                      │   │
│  │ Extensions Used:   0/3                                          │   │
│  │ Total Extension Days Available: 90 days                         │   │
│  │                                                                 │   │
│  │                  [Submit Progress Report for Extension]         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Sample Data Used:**
- Application: APP-001 (Jane Doe)
- Score: 78/100 (Approved)
- License: LIC-001 (Active, 85 days remaining)

---

### 3. Progress Report Submission Page

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Claude for Students                                    [Help] [Sign Out]│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Submit Progress Report                                                 │
│  ═════════════════════════════════════════════════════════════════════ │
│                                                                         │
│  License: CLAUDE-STU-2025-ABC123                                        │
│  Current Expiration: April 20, 2025  |  Extensions Available: 3         │
│                                                                         │
│  📝 Project Description (minimum 100 characters)                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ I have successfully used Claude to help me understand           │   │
│  │ transformer architectures and debug my sentiment analysis       │   │
│  │ model. I created a comprehensive test suite with Claude's       │   │
│  │ assistance, achieving 92% accuracy on my validation dataset.    │   │
│  │ The model is now ready for thesis submission.                   │   │
│  │                                                                 │   │
│  │ Characters: 287/1000 ✓                                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  💡 How did you use Claude? (specific examples)                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ • Used Claude to explain attention mechanisms in transformers   │   │
│  │ • Reviewed my Python code for bugs and optimization             │   │
│  │ • Generated edge case test scenarios for my model               │   │
│  │ • Discussed different approaches to sentiment classification    │   │
│  │ • Got help debugging CUDA memory issues                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  🎯 Outcomes/Deliverables Achieved                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ • Completed sentiment analysis model with 92% accuracy          │   │
│  │ • Wrote 50-page thesis chapter on NLP techniques                │   │
│  │ • Published preliminary results in conference proceedings       │   │
│  │ • Created reusable code library for future projects             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ☑ I confirm this report accurately reflects my progress                │
│                                                                         │
│                          [Submit Progress Report]                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Sample Data Used:**
- License: LIC-001 (Jane Doe)
- Progress Report: PR-001 (Approved, 30 days extension granted)

---

## Admin Dashboard Wireframes

### 1. Main Dashboard

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Claude Campaign Admin                    [Config] [Reports] [Sign Out] │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Dashboard Overview                                      January 2025   │
│  ═════════════════════════════════════════════════════════════════════ │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   Total      │  │   Approved   │  │   Rejected   │  │  Waitlisted  ││
│  │   1,247      │  │     892      │  │     289      │  │      66      ││
│  │Applications  │  │   (71.5%)    │  │   (23.2%)    │  │    (5.3%)    ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘│
│                                                                         │
│  📦 License Inventory                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Total Allocated: 892  |  Active: 845  |  Expired: 47            │   │
│  │ Available: 108        |  Total Pool: 1000                        │   │
│  │                                                                 │   │
│  │ [████████████████████████████████████████████████░░░░░░] 89.2% │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  📊 Score Distribution                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                                                                 │   │
│  │   100│                    ██                                    │   │
│  │    90│                  ██████                                  │   │
│  │    80│                ██████████                                │   │
│  │    70│              ██████████████                              │   │
│  │    60│            ██████████████████ ← Cutoff (60)              │   │
│  │    50│          ██████████████████████                          │   │
│  │    40│        ██████████████████████████                        │   │
│  │    30│      ██████████████████████████████                      │   │
│  │    20│    ██████████████████████████████████                    │   │
│  │    10│  ██████████████████████████████████████                  │   │
│  │     0└────────────────────────────────────────────────────────  │   │
│  │                                                                 │   │
│  │ Average: 62.4  |  Median: 58  |  Std Dev: 15.2                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  📋 Recent Applications                              [View All →]       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Student          │ Institution    │ Score │ Status   │ Date     │   │
│  │ ─────────────────┼────────────────┼───────┼──────────┼──────────│   │
│  │ Emily Davis      │ Columbia       │  81   │ ✅ Appr. │ Jan 25   │   │
│  │ Sarah Williams   │ Harvard        │  72   │ ✅ Appr. │ Jan 23   │   │
│  │ Alex Johnson     │ Berkeley       │  65   │ ✅ Appr. │ Jan 22   │   │
│  │ Mike Brown       │ UCLA           │  58   │ ⏳ Wait.  │ Jan 20   │   │
│  │ John Smith       │ Stanford       │  45   │ ❌ Rej.  │ Jan 19   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Sample Data Used:**
- Statistics from sample-data.json
- Recent applications from APP-001 through APP-006

---

### 2. Application Management View

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Claude Campaign Admin                    [Config] [Reports] [Sign Out] │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Applications                                                           │
│  ═════════════════════════════════════════════════════════════════════ │
│                                                                         │
│  🔍 Filters:                                                            │
│  [Status: All ▼] [Degree: All ▼] [Score: All ▼] [Date: All ▼]         │
│  [Search: _____________________________] [Apply Filters]                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ [ ]│ Student      │ Institution │ Degree    │ Score │ Status    │   │
│  │ ───┼──────────────┼─────────────┼───────────┼───────┼───────────│   │
│  │ [ ]│ Emily Davis  │ Columbia    │ Biology   │  81   │ ✅ Appr.  │   │
│  │ [ ]│ Sarah Will.  │ Harvard     │ Economics │  72   │ ✅ Appr.  │   │
│  │ [ ]│ Alex Johnson │ Berkeley    │ Physics   │  65   │ ✅ Appr.  │   │
│  │ [ ]│ Mike Brown   │ UCLA        │ History   │  58   │ ⏳ Wait.   │   │
│  │ [ ]│ John Smith   │ Stanford    │ MBA       │  45   │ ❌ Rej.   │   │
│  │ [ ]│ Jane Doe     │ MIT         │ CS (PhD)  │  78   │ ✅ Appr.  │   │
│  │                                                                 │   │
│  │ Showing 1-25 of 1,247                  [< Prev] [1] [2] [3] [>]│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  [Export CSV]  [Bulk Approve]  [Bulk Reject]  [Manual Override]        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Sample Data Used:**
- All 6 sample applications with their scores and statuses

---

### 3. Configuration Panel

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Claude Campaign Admin                    [Config] [Reports] [Sign Out] │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Configuration                                                          │
│  ═════════════════════════════════════════════════════════════════════ │
│                                                                         │
│  ⚙️  Cutoff Scores by Degree Category                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ STEM:        [60] points                                        │   │
│  │ Business:    [55] points                                        │   │
│  │ Humanities:  [50] points                                        │   │
│  │ Arts:        [45] points                                        │   │
│  │ Other:       [50] points                                        │   │
│  │                                                                 │   │
│  │                    [Reset to Defaults] [Save Changes]           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  📅 License Settings                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Default License Period:     [90] days                           │   │
│  │ Max Extensions per License: [3]                                 │   │
│  │ Max Total Extension Days:   [90] days                           │   │
│  │ Extension Days per Report:  [30] days                           │   │
│  │                                                                 │   │
│  │                    [Reset to Defaults] [Save Changes]           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  📦 License Inventory                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Total License Pool: [1000]                                      │   │
│  │                                                                 │   │
│  │                              [Update Inventory]                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  🎯 Scoring Weights                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Degree Relevance:      [30] points (max)                        │   │
│  │ Objective Quality:     [25] points (max)                        │   │
│  │ Academic Standing:     [20] points (max)                        │   │
│  │ Demonstrated Need:     [15] points (max)                        │   │
│  │ Claude Familiarity:    [10] points (max)                        │   │
│  │                                                                 │   │
│  │                    [Reset to Defaults] [Save Changes]           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Configuration Values:**
- All default values from design.md

---

## Data Flow Examples

### Example 1: Jane Doe's Application Journey

```
1. Application Submission (APP-001)
   └─ Student: Jane Doe (STU-001)
   └─ Degree: Computer Science (STEM)
   └─ Objective: NLP/ML thesis research
   └─ Prior Experience: Moderate

2. Scoring Calculation
   ├─ Degree Relevance: 30/30 (STEM category)
   ├─ Objective Quality: 22/25 (detailed, feasible)
   ├─ Academic Standing: 20/20 (Graduate student)
   ├─ Demonstrated Need: 4/15 (receives financial aid)
   ├─ Claude Familiarity: 7/10 (moderate experience)
   └─ Total Score: 78/100

3. Allocation Decision
   ├─ Cutoff Score: 60 (STEM category)
   ├─ Score vs Cutoff: 78 ≥ 60 ✅
   ├─ License Inventory: Available ✅
   └─ Status: APPROVED

4. License Allocation
   ├─ License ID: CLAUDE-STU-2025-ABC123
   ├─ Start Date: January 20, 2025
   ├─ Expiration: April 20, 2025 (90 days)
   └─ Status: ACTIVE

5. Progress Report (PR-001)
   ├─ Submitted: April 10, 2025
   ├─ Description: 287 characters ✓
   ├─ Claude Usage Examples: Provided ✓
   ├─ Outcomes: Provided ✓
   ├─ Status: APPROVED
   └─ Extension Granted: 30 days (New expiration: May 20, 2025)
```

### Example 2: John Smith's Application Journey

```
1. Application Submission (APP-002)
   └─ Student: John Smith (STU-002)
   └─ Degree: Business Administration (Business)
   └─ Objective: MBA coursework and case studies (vague)
   └─ Prior Experience: None

2. Scoring Calculation
   ├─ Degree Relevance: 25/30 (Business category)
   ├─ Objective Quality: 8/25 (vague, lacks specificity)
   ├─ Academic Standing: 12/20 (Graduate student, year 1)
   ├─ Demonstrated Need: 0/15 (no financial aid, not first-gen)
   ├─ Claude Familiarity: 0/10 (no prior experience)
   └─ Total Score: 45/100

3. Allocation Decision
   ├─ Cutoff Score: 55 (Business category)
   ├─ Score vs Cutoff: 45 < 55 ❌
   └─ Status: REJECTED

4. Rejection Notification
   ├─ Reason: Score below cutoff
   ├─ Score Breakdown: Provided to student
   └─ Feedback: Objective needs more detail and specificity
```

---

## Key Metrics from Sample Data

| Metric | Value |
|--------|-------|
| Total Applications | 1,247 |
| Approved | 892 (71.5%) |
| Rejected | 289 (23.2%) |
| Waitlisted | 66 (5.3%) |
| Active Licenses | 845 |
| Available Licenses | 108 |
| License Pool | 1,000 |
| Average Score | 62.4 |
| Median Score | 58 |
| Std Dev | 15.2 |

---

## Next Steps

The wireframes and sample data are ready for:
1. **Frontend Development** - Use these wireframes as design specifications
2. **API Testing** - Use sample data to test endpoints
3. **User Testing** - Share wireframes with stakeholders
4. **Implementation** - Reference these when building components

All sample data is available in `sample-data.json` for integration testing.
