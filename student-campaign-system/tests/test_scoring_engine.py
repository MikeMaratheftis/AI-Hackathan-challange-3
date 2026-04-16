import pytest
from services.scoring_engine import ScoringEngineService
from config import Config

class TestScoringEngine:
    """Test suite for scoring engine"""
    
    @pytest.fixture
    def scoring_engine(self):
        return ScoringEngineService(Config())
    
    def test_score_bounds_property(self, scoring_engine):
        """Property: Score must always be between 0 and 100"""
        test_cases = [
            {
                'degree_category': 'STEM',
                'objective': 'I want to use Claude for my research project on machine learning and AI.',
                'degree_level': 'graduate',
                'year': 2,
                'financial_aid': True,
                'first_generation': False,
                'prior_claude_usage': 'moderate'
            },
            {
                'degree_category': 'Other',
                'objective': 'Short objective',
                'degree_level': 'undergraduate',
                'year': 1,
                'financial_aid': False,
                'first_generation': False,
                'prior_claude_usage': 'none'
            }
        ]
        
        for case in test_cases:
            score = scoring_engine.calculate_score(case)
            assert 0 <= score['total'] <= 100, f"Score {score['total']} out of bounds"
    
    def test_score_component_sum_invariant(self, scoring_engine):
        """Property: Sum of components should equal total score"""
        application = {
            'degree_category': 'STEM',
            'objective': 'I want to use Claude for my research project on machine learning and AI.',
            'degree_level': 'graduate',
            'year': 2,
            'financial_aid': True,
            'first_generation': False,
            'prior_claude_usage': 'moderate'
        }
        
        score = scoring_engine.calculate_score(application)
        breakdown_sum = sum(score['breakdown'].values())
        
        assert breakdown_sum == score['total'], \
            f"Breakdown sum {breakdown_sum} != total {score['total']}"
    
    def test_score_determinism(self, scoring_engine):
        """Property: Same input should always produce same score"""
        application = {
            'degree_category': 'STEM',
            'objective': 'I want to use Claude for my research project on machine learning and AI.',
            'degree_level': 'graduate',
            'year': 2,
            'financial_aid': True,
            'first_generation': False,
            'prior_claude_usage': 'moderate'
        }
        
        score1 = scoring_engine.calculate_score(application)
        score2 = scoring_engine.calculate_score(application)
        
        assert score1['total'] == score2['total'], "Scores differ for same input"
        assert score1['breakdown'] == score2['breakdown'], "Breakdowns differ for same input"
    
    def test_degree_relevance_scoring(self, scoring_engine):
        """Test degree relevance scoring"""
        stem_app = {'degree_category': 'STEM'}
        business_app = {'degree_category': 'Business'}
        
        stem_score = scoring_engine._calculate_degree_relevance('STEM')
        business_score = scoring_engine._calculate_degree_relevance('Business')
        
        assert stem_score == 30
        assert business_score == 25
        assert stem_score > business_score
    
    def test_objective_quality_scoring(self, scoring_engine):
        """Test objective quality evaluation"""
        short_objective = "I want to use Claude."
        long_objective = "I want to use Claude for my research project on machine learning and AI. " * 5
        
        short_score = scoring_engine._evaluate_objective_quality(short_objective)
        long_score = scoring_engine._evaluate_objective_quality(long_objective)
        
        assert short_score < long_score
        assert 0 <= short_score <= 25
        assert 0 <= long_score <= 25
    
    def test_academic_standing_scoring(self, scoring_engine):
        """Test academic standing scoring"""
        grad_score = scoring_engine._calculate_academic_standing('graduate', 1)
        undergrad_senior = scoring_engine._calculate_academic_standing('undergraduate', 4)
        undergrad_freshman = scoring_engine._calculate_academic_standing('undergraduate', 1)
        
        assert grad_score == 20
        assert undergrad_senior == 15
        assert undergrad_freshman == 5
        assert grad_score > undergrad_senior > undergrad_freshman
    
    def test_demonstrated_need_scoring(self, scoring_engine):
        """Test demonstrated need scoring"""
        no_need = scoring_engine._calculate_demonstrated_need(False, False, False)
        with_aid = scoring_engine._calculate_demonstrated_need(True, False, False)
        first_gen = scoring_engine._calculate_demonstrated_need(False, True, False)
        all_factors = scoring_engine._calculate_demonstrated_need(True, True, True)
        
        assert no_need == 0
        assert with_aid == 8
        assert first_gen == 4
        assert all_factors == 15
    
    def test_claude_familiarity_scoring(self, scoring_engine):
        """Test Claude familiarity scoring"""
        experienced = scoring_engine._calculate_claude_familiarity('experienced')
        moderate = scoring_engine._calculate_claude_familiarity('moderate')
        beginner = scoring_engine._calculate_claude_familiarity('beginner')
        none = scoring_engine._calculate_claude_familiarity('none')
        
        assert experienced == 10
        assert moderate == 7
        assert beginner == 4
        assert none == 0
        assert experienced > moderate > beginner > none
    
    def test_score_validation(self, scoring_engine):
        """Test score validation"""
        valid_score = {
            'total': 75,
            'breakdown': {
                'degree_relevance': 30,
                'objective_quality': 20,
                'academic_standing': 15,
                'demonstrated_need': 10,
                'claude_familiarity': 0
            }
        }
        
        is_valid, message = scoring_engine.validate_score_bounds(valid_score)
        assert is_valid
        assert "valid" in message.lower()
