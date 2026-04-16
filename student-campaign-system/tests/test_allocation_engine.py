import pytest
from services.allocation_engine import AllocationEngineService
from models import ApplicationStatus
from config import Config

class TestAllocationEngine:
    """Test suite for allocation engine"""
    
    @pytest.fixture
    def allocation_engine(self):
        engine = AllocationEngineService(Config())
        engine.set_available_licenses(100)
        return engine
    
    def test_cutoff_enforcement_property(self, allocation_engine):
        """Property: Applications below cutoff should never be approved"""
        test_cases = [
            {'score': 65, 'category': 'STEM', 'should_approve': True},
            {'score': 59, 'category': 'STEM', 'should_approve': False},
            {'score': 55, 'category': 'Business', 'should_approve': True},
            {'score': 54, 'category': 'Business', 'should_approve': False},
        ]
        
        for case in test_cases:
            decision = allocation_engine.process_allocation(
                {},
                case['score'],
                case['category']
            )
            
            if case['should_approve']:
                assert decision['meets_cutoff'], \
                    f"Score {case['score']} should meet cutoff for {case['category']}"
            else:
                assert not decision['meets_cutoff'], \
                    f"Score {case['score']} should not meet cutoff for {case['category']}"
    
    def test_inventory_conservation_property(self, allocation_engine):
        """Property: Allocated + Available licenses should equal total pool"""
        initial_available = allocation_engine.get_available_licenses()
        
        # Allocate some licenses
        for _ in range(5):
            allocation_engine.process_allocation({}, 75, 'STEM')
        
        final_available = allocation_engine.get_available_licenses()
        allocated = initial_available - final_available
        
        assert allocated == 5, "Inventory not properly tracked"
        assert final_available == initial_available - 5
    
    def test_cutoff_score_retrieval(self, allocation_engine):
        """Test cutoff score retrieval by category"""
        stem_cutoff = allocation_engine.get_cutoff_score('STEM')
        business_cutoff = allocation_engine.get_cutoff_score('Business')
        
        assert stem_cutoff == 60
        assert business_cutoff == 55
    
    def test_cutoff_score_override(self, allocation_engine):
        """Test cutoff score override"""
        default_cutoff = allocation_engine.get_cutoff_score('STEM')
        override_cutoff = allocation_engine.get_cutoff_score('STEM', override=70)
        
        assert default_cutoff == 60
        assert override_cutoff == 70
    
    def test_allocation_decision_approved(self, allocation_engine):
        """Test allocation decision for approved application"""
        decision = allocation_engine.process_allocation({}, 75, 'STEM')
        
        assert decision['meets_cutoff']
        assert decision['status'] == ApplicationStatus.APPROVED.value
        assert decision['action'] == 'allocate_license'
    
    def test_allocation_decision_rejected(self, allocation_engine):
        """Test allocation decision for rejected application"""
        decision = allocation_engine.process_allocation({}, 45, 'STEM')
        
        assert not decision['meets_cutoff']
        assert decision['status'] == ApplicationStatus.REJECTED.value
        assert decision['action'] == 'reject_application'
    
    def test_allocation_decision_waitlisted(self, allocation_engine):
        """Test allocation decision when inventory exhausted"""
        allocation_engine.set_available_licenses(0)
        
        decision = allocation_engine.process_allocation({}, 75, 'STEM')
        
        assert decision['meets_cutoff']
        assert decision['status'] == ApplicationStatus.WAITLISTED.value
        assert decision['action'] == 'add_to_waitlist'
    
    def test_update_cutoff_score(self, allocation_engine):
        """Test updating cutoff scores"""
        success, message = allocation_engine.update_cutoff_score('STEM', 65)
        
        assert success
        assert allocation_engine.get_cutoff_score('STEM') == 65
    
    def test_update_cutoff_score_invalid(self, allocation_engine):
        """Test updating cutoff score with invalid value"""
        success, message = allocation_engine.update_cutoff_score('STEM', 150)
        
        assert not success
        assert allocation_engine.get_cutoff_score('STEM') == 60  # Unchanged
    
    def test_allocation_decision_validation(self, allocation_engine):
        """Test allocation decision validation"""
        valid_decision = {
            'meets_cutoff': True,
            'status': ApplicationStatus.APPROVED.value
        }
        
        is_valid, message = allocation_engine.validate_allocation_decision(valid_decision)
        assert is_valid
