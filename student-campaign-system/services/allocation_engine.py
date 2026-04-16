from typing import Dict, Tuple, Optional
from datetime import datetime
from models import ApplicationStatus, LicenseStatus
from config import Config

class AllocationEngineService:
    """Service for allocating licenses to qualified students"""
    
    def __init__(self, config: Config = None):
        if config is None:
            config = Config()
        self.config = config
        # Get cutoff scores from config or use defaults
        if hasattr(config, 'DEFAULT_CUTOFF_SCORES'):
            self.cutoff_scores = config.DEFAULT_CUTOFF_SCORES
        else:
            from config import Config as DefaultConfig
            self.cutoff_scores = DefaultConfig.DEFAULT_CUTOFF_SCORES
        self.available_licenses = 1000  # Default pool
    
    def get_cutoff_score(self, degree_category: str, override: Optional[int] = None) -> int:
        """Get cutoff score for degree category"""
        if override is not None:
            return override
        
        return self.cutoff_scores.get(degree_category, self.cutoff_scores['Other'])
    
    def process_allocation(self, application_data: Dict, score: int, 
                          degree_category: str) -> Dict:
        """Process allocation decision for an application"""
        cutoff = self.get_cutoff_score(degree_category)
        
        decision = {
            'score': score,
            'cutoff_score': cutoff,
            'meets_cutoff': score >= cutoff,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if score >= cutoff:
            if self.available_licenses > 0:
                decision['status'] = ApplicationStatus.APPROVED.value
                decision['action'] = 'allocate_license'
                self.available_licenses -= 1
            else:
                decision['status'] = ApplicationStatus.WAITLISTED.value
                decision['action'] = 'add_to_waitlist'
        else:
            decision['status'] = ApplicationStatus.REJECTED.value
            decision['action'] = 'reject_application'
        
        return decision
    
    def set_available_licenses(self, count: int):
        """Set the number of available licenses"""
        self.available_licenses = count
    
    def get_available_licenses(self) -> int:
        """Get current available licenses"""
        return self.available_licenses
    
    def update_cutoff_score(self, degree_category: str, new_score: int):
        """Update cutoff score for a degree category"""
        if 0 <= new_score <= 100:
            self.cutoff_scores[degree_category] = new_score
            return True, f"Cutoff score for {degree_category} updated to {new_score}"
        
        return False, "Cutoff score must be between 0 and 100"
    
    def validate_allocation_decision(self, decision: Dict) -> Tuple[bool, str]:
        """Validate allocation decision logic"""
        if decision['meets_cutoff'] and decision['status'] == ApplicationStatus.APPROVED.value:
            return True, "Allocation decision is valid"
        elif not decision['meets_cutoff'] and decision['status'] == ApplicationStatus.REJECTED.value:
            return True, "Rejection decision is valid"
        elif decision['meets_cutoff'] and decision['status'] == ApplicationStatus.WAITLISTED.value:
            return True, "Waitlist decision is valid (no licenses available)"
        
        return False, "Allocation decision is inconsistent"
