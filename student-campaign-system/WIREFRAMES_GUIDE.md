# Interactive Wireframes Guide

## Overview

This is a fully interactive, browser-based prototype of the Student Campaign License Allocation System. It includes both the student portal and admin dashboard with real-time interactions.

## Quick Start

### Option 1: Using Python HTTP Server (Recommended)

```bash
cd student-campaign-system
python serve_static.py
```

Then open your browser to: **http://localhost:8000**

### Option 2: Using Python's Built-in Server

```bash
cd student-campaign-system/static
python -m http.server 8000
```

Then open: **http://localhost:8000**

### Option 3: Using Node.js http-server

```bash
npm install -g http-server
cd student-campaign-system/static
http-server -p 8000
```

## Features

### Student Portal

#### 1. Application Form Tab
- **Personal Information Section**
  - Full name input
  - Email with .edu domain verification badge
  - Institution selection dropdown
  
- **Academic Information Section**
  - Degree program selection
  - Degree level (Undergraduate, Graduate, PhD)
  - Year selection
  - Financial aid checkbox
  - First-generation student checkbox

- **Objective Section**
  - Textarea with real-time character counter (50-500 characters)
  - Use case category dropdown
  - Prior Claude experience radio buttons
  - Form validation on submission

**Sample Data Pre-filled:**
- Student: Jane Doe
- Email: jane.doe@mit.edu
- Institution: MIT
- Degree: Computer Science (Graduate)
- Objective: NLP/ML research thesis

#### 2. Application Status Tab
- **Status Display**
  - Approval status badge (✅ APPROVED)
  - Application date

- **Score Breakdown**
  - Visual progress bars for each criterion
  - Points earned vs. maximum
  - Total score: 78/100
  - Cutoff score comparison

- **License Details**
  - License ID: CLAUDE-STU-2025-ABC123
  - Status indicator (● ACTIVE)
  - Start and expiration dates
  - Days remaining: 85
  - Extensions used: 0/3
  - Button to submit progress report

#### 3. Progress Report Tab
- **Project Description**
  - Textarea with character counter (100-1000 characters)
  - Real-time validation

- **Claude Usage Examples**
  - Textarea for specific examples
  - Pre-filled with bullet points

- **Outcomes/Deliverables**
  - Textarea for listing achievements
  - Pre-filled with sample outcomes

- **Confirmation Checkbox**
  - Accuracy confirmation before submission

### Admin Dashboard

#### 1. Overview Tab
- **Statistics Cards**
  - Total Applications: 1,247
  - Approved: 892 (71.5%)
  - Rejected: 289 (23.2%)
  - Waitlisted: 66 (5.3%)

- **License Inventory**
  - Total Allocated: 892
  - Active: 845
  - Expired: 47
  - Available: 108
  - Total Pool: 1000
  - Visual progress bar (89.2% utilized)

- **Score Distribution Chart**
  - Bar chart showing application distribution by score range
  - Statistics: Average (62.4), Median (58), Std Dev (15.2)

- **Recent Applications Table**
  - Student name, institution, score, status, date
  - Color-coded status badges

#### 2. Applications Tab
- **Filter Controls**
  - Status filter (All, Approved, Rejected, Waitlisted)
  - Degree category filter
  - Search by student name
  - Apply filters button

- **Applications Table**
  - Checkbox selection for bulk actions
  - Student information
  - Degree program
  - Score
  - Status with color-coded badges
  - View action button

- **Pagination**
  - Previous/Next buttons
  - Current page indicator

- **Bulk Actions**
  - Export CSV
  - Bulk Approve
  - Bulk Reject

#### 3. Configuration Tab
- **Cutoff Scores Configuration**
  - STEM: 60 points
  - Business: 55 points
  - Humanities: 50 points
  - Arts: 45 points
  - Other: 50 points
  - Reset to Defaults button
  - Save Changes button

- **License Settings**
  - Default License Period: 90 days
  - Max Extensions per License: 3
  - Max Total Extension Days: 90 days
  - Extension Days per Report: 30 days

- **License Inventory**
  - Total License Pool: 1000
  - Update Inventory button

- **Scoring Weights**
  - Degree Relevance: 30 points (max)
  - Objective Quality: 25 points (max)
  - Academic Standing: 20 points (max)
  - Demonstrated Need: 15 points (max)
  - Claude Familiarity: 10 points (max)

## Interactive Features

### Form Validation
- Real-time character counting
- Minimum/maximum length validation
- Required field validation
- Email domain verification badge

### Tab Navigation
- Smooth transitions between tabs
- Active tab highlighting
- Persistent state within session

### Filtering & Search
- Real-time application filtering
- Multi-criteria filtering
- Search by student name

### Notifications
- Success notifications (green)
- Error notifications (red)
- Info notifications (blue)
- Auto-dismiss after 3 seconds

### Responsive Design
- Mobile-friendly layout
- Tablet optimization
- Desktop full-width support
- Flexible grid layouts

## Sample Data

### Students
1. **Jane Doe** - MIT, Computer Science (PhD), Score: 78
2. **Emily Davis** - Columbia, Molecular Biology (PhD), Score: 81
3. **Sarah Williams** - Harvard, Economics, Score: 72
4. **Alex Johnson** - Berkeley, Physics, Score: 65
5. **Mike Brown** - UCLA, History, Score: 58
6. **John Smith** - Stanford, MBA, Score: 45

### Application Statuses
- ✅ **Approved**: Score ≥ Cutoff
- ❌ **Rejected**: Score < Cutoff
- ⏳ **Waitlisted**: Score ≥ Cutoff but no licenses available

### Scoring Breakdown (Jane Doe - 78/100)
- Degree Relevance: 30/30 (STEM)
- Objective Quality: 22/25 (detailed, feasible)
- Academic Standing: 20/20 (Graduate)
- Demonstrated Need: 4/15 (financial aid)
- Claude Familiarity: 7/10 (moderate)

## Color Scheme

- **Primary**: #6366f1 (Indigo)
- **Secondary**: #8b5cf6 (Purple)
- **Success**: #10b981 (Green)
- **Danger**: #ef4444 (Red)
- **Warning**: #f59e0b (Amber)
- **Info**: #3b82f6 (Blue)

## File Structure

```
static/
├── index.html          # Main HTML structure
├── styles.css          # Complete styling
├── script.js           # Interactive functionality
└── README.md           # This file
```

## Browser Compatibility

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Testing Scenarios

### Student Portal Testing

1. **Application Submission**
   - Fill out application form
   - Verify character counter works
   - Submit application
   - See success notification
   - Auto-navigate to status tab

2. **Score Breakdown Viewing**
   - View score breakdown with progress bars
   - Verify total score calculation
   - Check cutoff score comparison

3. **Progress Report Submission**
   - Navigate to progress report tab
   - Fill out all required fields
   - Verify character counter
   - Submit report
   - See extension approval notification

### Admin Dashboard Testing

1. **Statistics Viewing**
   - Check all stat cards display correctly
   - Verify license inventory bar
   - View score distribution chart

2. **Application Filtering**
   - Filter by status
   - Filter by degree category
   - Search by student name
   - Combine multiple filters

3. **Configuration Management**
   - Update cutoff scores
   - Modify license settings
   - Change scoring weights
   - Save and verify changes

## Keyboard Shortcuts

- `Tab` - Navigate between form fields
- `Enter` - Submit forms
- `Escape` - Close modals (when implemented)

## Accessibility Features

- Semantic HTML structure
- ARIA labels on form inputs
- Keyboard navigation support
- Color contrast compliance
- Focus indicators on interactive elements

## Performance

- Lightweight CSS (no frameworks)
- Vanilla JavaScript (no dependencies except Chart.js)
- Fast load times
- Smooth animations
- Responsive to user interactions

## Future Enhancements

1. **Backend Integration**
   - Connect to Python Flask API
   - Real API calls instead of mock data
   - Database persistence

2. **Advanced Features**
   - Email notifications
   - PDF export
   - Advanced analytics
   - User authentication
   - Role-based access control

3. **Mobile App**
   - React Native version
   - iOS/Android apps
   - Offline support

4. **Analytics**
   - Application trends
   - Score distribution analysis
   - License utilization reports
   - Student success metrics

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Chart Not Displaying
- Ensure Chart.js CDN is accessible
- Check browser console for errors
- Verify JavaScript is enabled

### Styles Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- Check file paths in HTML

## Support

For issues or questions:
1. Check browser console for errors (F12)
2. Verify all files are in the `static/` directory
3. Ensure Python/Node server is running
4. Try a different browser

## License

This is a prototype for the Student Campaign License Allocation System.
