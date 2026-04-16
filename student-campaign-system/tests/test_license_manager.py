import pytest
from datetime import datetime, timedelta
from services.license_manager import LicenseManagerService
from config import Config

class TestLicenseManager:
    """Test suite for license manager"""
    
    @pytest.fixture
    def license_manager(self):
        return LicenseManagerService(Config())
    
    def test_extension_limit_invariant(self, license_manager):
        """Property: Extensions should never exceed configured maximums"""
        license_data = {
            'extensions_granted': 3,
            'total_extension_days': 90,
            'expiration_date': (datetime.utcnow() + timedelta(days=5)).isoformat()
        }
        
        report_data = {
            'description': 'I have made significant progress on my project.',
            'claude_usage_examples': 'Used Claude for code review and debugging.',
            'outcomes': 'Completed 3 major milestones.'
        }
        
        result = license_manager.evaluate_extension_request(
            license_data,
            report_data,
            85
        )
        
        assert not result['approved']
        assert 'Maximum extensions' in result['reason']
    
    def test_license_creation(self, license_manager):
        """Test license creation"""
        license_data = license_manager.create_license('student-123', 'app-456')
        
        assert license_data['student_id'] == 'student-123'
        assert license_data['application_id'] == 'app-456'
        assert license_data['status'] == 'active'
        assert license_data['extensions_granted'] == 0
        assert license_data['total_extension_days'] == 0
        assert 'CLAUDE-STU' in license_data['claude_license_key']
    
    def test_license_expiration_calculation(self, license_manager):
        """Test license expiration date calculation"""
        license_data = license_manager.create_license('student-123', 'app-456')
        
        start = datetime.fromisoformat(license_data['start_date'])
        expiration = datetime.fromisoformat(license_data['expiration_date'])
        
        days_diff = (expiration - start).days
        assert days_diff == 90  # Default period
    
    def test_progress_report_validation_success(self, license_manager):
        """Test valid progress report"""
        license_data = {
            'expiration_date': (datetime.utcnow() + timedelta(days=5)).isoformat()
        }
        
        report_data = {
            'description': 'I have successfully used Claude to help me understand transformer architectures and debug my sentiment analysis model. I created a comprehensive test suite with Claude\'s assistance, achieving 92% accuracy on my validation dataset.',
            'claude_usage_examples': 'Used Claude to explain attention mechanisms, reviewed my code for bugs, generated edge case test scenarios',
            'outcomes': 'Completed sentiment analysis model with 92% accuracy, wrote 50-page thesis chapter'
        }
        
        valid, errors = license_manager.validate_progress_report(report_data, license_data)
        
        assert valid
        assert len(errors) == 0
    
    def test_progress_report_validation_short_description(self, license_manager):
        """Test progress report with short description"""
        license_data = {
            'expiration_date': (datetime.utcnow() + timedelta(days=5)).isoformat()
        }
        
        report_data = {
            'description': 'Short',
            'claude_usage_examples': 'Used Claude',
            'outcomes': 'Completed work'
        }
        
        valid, errors = license_manager.validate_progress_report(report_data, license_data)
        
        assert not valid
        assert any('100 characters' in error for error in errors)
    
    def test_progress_report_validation_missing_examples(self, license_manager):
        """Test progress report without Claude usage examples"""
        license_data = {
            'expiration_date': (datetime.utcnow() + timedelta(days=5)).isoformat()
        }
        
        report_data = {
            'description': 'I have successfully used Claude to help me understand transformer architectures.',
            'claude_usage_examples': '',
            'outcomes': 'Completed work'
        }
        
        valid, errors = license_manager.validate_progress_report(report_data, license_data)
        
        assert not valid
        assert any('Claude usage examples' in error for error in errors)
    
    def test_progress_report_validation_timing(self, license_manager):
        """Test progress report submission timing validation"""
        license_data = {
            'expiration_date': (datetime.utcnow() + timedelta(days=60)).isoformat()
        }
        
        report_data = {
            'description': 'I have successfully used Claude to help me understand transformer architectures.',
            'claude_usage_examples': 'Used Claude for code review',
            'outcomes': 'Completed work'
        }
        
        valid, errors = license_manager.validate_progress_report(report_data, license_data)
        
        assert not valid
        assert any('30 days' in error for error in errors)
    
    def test_progress_quality_evaluation(self, license_manager):
        """Test progress report quality evaluation"""
        report_data = {
            'description': 'I have successfully used Claude to help me understand transformer architectures and debug my sentiment analysis model. I created a comprehensive test suite with Claude\'s assistance, achieving 92% accuracy on my validation dataset. The model is now ready for thesis submission.' * 2,
            'claude_usage_examples': '• Used Claude to explain attention mechanisms\n• Reviewed my code for bugs\n• Generated edge case test scenarios\n• Discussed different approaches\n• Got help debugging CUDA memory issues',
            'outcomes': '• Completed sentiment analysis model with 92% accuracy\n• Wrote 50-page thesis chapter\n• Published preliminary results\n• Created reusable code library'
        }
        
        quality_score = license_manager.evaluate_progress_quality(report_data)
        
        assert 0 <= quality_score <= 100
        assert quality_score > 70  # Should be high quality
    
    def test_extension_approval(self, license_manager):
        """Test extension approval for high-quality report"""
        license_data = {
            'extensions_granted': 0,
            'total_extension_days': 0,
            'expiration_date': (datetime.utcnow() + timedelta(days=5)).isoformat()
        }
        
        report_data = {
            'description': 'I have successfully used Claude to help me understand transformer architectures and debug my sentiment analysis model. I created a comprehensive test suite with Claude\'s assistance, achieving 92% accuracy on my validation dataset. The model is now ready for thesis submission.',
            'claude_usage_examples': '• Used Claude to explain attention mechanisms\n• Reviewed my code for bugs\n• Generated edge case test scenarios',
            'outcomes': '• Completed sentiment analysis model with 92% accuracy\n• Wrote 50-page thesis chapter'
        }
        
        result = license_manager.evaluate_extension_request(
            license_data,
            report_data,
            85
        )
        
        assert result['approved']
        assert result['extension_days'] == 30
        assert result['new_expiration'] is not None
    
    def test_license_expiration_check(self, license_manager):
        """Test license expiration status check"""
        license_data = {
            'expiration_date': (datetime.utcnow() + timedelta(days=5)).isoformat()
        }
        
        expiration_check = license_manager.check_license_expiration(license_data)
        
        assert not expiration_check['expired']
        assert expiration_check['days_remaining'] == 5
        assert expiration_check['needs_7_day_notification']
