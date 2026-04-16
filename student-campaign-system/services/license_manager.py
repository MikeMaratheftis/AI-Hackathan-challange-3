from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import uuid
from models import LicenseStatus, ProgressReportStatus
from config import Config

class LicenseManagerService:
    """Service for managing licenses and extensions"""
    
    def __init__(self, config: Config = None):
        if config is None:
            config = Config()
        self.config = config
        # Get settings from config or use defaults
        if not hasattr(config, 'DEFAULT_LICENSE_PERIOD_DAYS'):
            from config import Config as DefaultConfig
            self.config = DefaultConfig()
    
    def create_license(self, student_id: str, application_id: str) -> Dict:
        """Create a new license for a student"""
        start_date = datetime.utcnow()
        expiration_date = start_date + timedelta(
            days=self.config.DEFAULT_LICENSE_PERIOD_DAYS
        )
        
        license_key = f"CLAUDE-STU-{start_date.year}-{uuid.uuid4().hex[:6].upper()}"
        
        return {
            'id': str(uuid.uuid4()),
            'student_id': student_id,
            'application_id': application_id,
            'claude_license_key': license_key,
            'start_date': start_date.isoformat(),
            'expiration_date': expiration_date.isoformat(),
            'extensions_granted': 0,
            'total_extension_days': 0,
            'status': LicenseStatus.ACTIVE.value,
            'created_at': start_date.isoformat()
        }
    
    def validate_progress_report(self, report_data: Dict, license_data: Dict) -> Tuple[bool, list]:
        """Validate progress report submission"""
        errors = []
        
        # Check minimum description length
        description = report_data.get('description', '')
        if len(description) < self.config.PROGRESS_REPORT_MIN_CHARS:
            errors.append(
                f"Description must be at least {self.config.PROGRESS_REPORT_MIN_CHARS} characters"
            )
        
        # Check for Claude usage examples
        claude_examples = report_data.get('claude_usage_examples', '')
        if not claude_examples or len(claude_examples.strip()) == 0:
            errors.append("Report must include specific Claude usage examples")
        
        # Check for outcomes
        outcomes = report_data.get('outcomes', '')
        if not outcomes or len(outcomes.strip()) == 0:
            errors.append("Report must describe outcomes or deliverables achieved")
        
        # Check submission timing
        expiration_date = datetime.fromisoformat(license_data['expiration_date'])
        days_until_expiration = (expiration_date - datetime.utcnow()).days
        
        if days_until_expiration > self.config.PROGRESS_REPORT_SUBMISSION_WINDOW_DAYS:
            errors.append(
                f"Progress report can only be submitted within "
                f"{self.config.PROGRESS_REPORT_SUBMISSION_WINDOW_DAYS} days of expiration"
            )
        
        return len(errors) == 0, errors
    
    def evaluate_extension_request(self, license_data: Dict, 
                                   report_data: Dict, 
                                   quality_score: int) -> Dict:
        """Evaluate extension request based on progress report"""
        result = {
            'approved': False,
            'extension_days': 0,
            'reason': None,
            'new_expiration': None
        }
        
        # Check extension limits
        if license_data['extensions_granted'] >= self.config.MAX_EXTENSIONS_PER_LICENSE:
            result['reason'] = "Maximum extensions reached"
            return result
        
        if license_data['total_extension_days'] >= self.config.MAX_TOTAL_EXTENSION_DAYS:
            result['reason'] = "Maximum total extension days reached"
            return result
        
        # Validate progress report
        valid, errors = self.validate_progress_report(report_data, license_data)
        if not valid:
            result['reason'] = f"Progress report validation failed: {'; '.join(errors)}"
            return result
        
        # Evaluate progress quality
        if quality_score >= self.config.PROGRESS_QUALITY_THRESHOLD:
            extension_days = min(
                self.config.EXTENSION_DAYS_PER_REPORT,
                self.config.MAX_TOTAL_EXTENSION_DAYS - license_data['total_extension_days']
            )
            
            expiration_date = datetime.fromisoformat(license_data['expiration_date'])
            new_expiration = expiration_date + timedelta(days=extension_days)
            
            result['approved'] = True
            result['extension_days'] = extension_days
            result['new_expiration'] = new_expiration.isoformat()
            result['reason'] = "Extension approved based on progress quality"
        else:
            result['reason'] = "Progress report does not demonstrate sufficient progress"
        
        return result
    
    def evaluate_progress_quality(self, report_data: Dict) -> int:
        """Evaluate quality of progress report (0-100 scale)"""
        score = 0
        
        # Description quality (0-40 points)
        description = report_data.get('description', '')
        desc_length = len(description)
        if desc_length >= 500:
            score += 40
        elif desc_length >= 300:
            score += 30
        elif desc_length >= 150:
            score += 20
        else:
            score += 10
        
        # Claude usage examples (0-30 points)
        examples = report_data.get('claude_usage_examples', '')
        example_count = len([e for e in examples.split('\n') if e.strip().startswith('•') or e.strip().startswith('-')])
        if example_count >= 5:
            score += 30
        elif example_count >= 3:
            score += 20
        elif example_count >= 1:
            score += 10
        
        # Outcomes/deliverables (0-30 points)
        outcomes = report_data.get('outcomes', '')
        outcome_count = len([o for o in outcomes.split('\n') if o.strip().startswith('•') or o.strip().startswith('-')])
        if outcome_count >= 4:
            score += 30
        elif outcome_count >= 2:
            score += 20
        elif outcome_count >= 1:
            score += 10
        
        return min(score, 100)
    
    def check_license_expiration(self, license_data: Dict) -> Dict:
        """Check license expiration status"""
        expiration_date = datetime.fromisoformat(license_data['expiration_date'])
        now = datetime.utcnow()
        days_remaining = (expiration_date - now).days
        
        return {
            'expired': days_remaining < 0,
            'days_remaining': max(days_remaining, 0),
            'expiration_date': license_data['expiration_date'],
            'needs_14_day_notification': 0 <= days_remaining <= 14,
            'needs_7_day_notification': 0 <= days_remaining <= 7,
            'needs_expiration_notification': days_remaining < 0
        }
