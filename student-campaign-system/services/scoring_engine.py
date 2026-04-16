from typing import Dict, Tuple
from datetime import datetime
from models import DegreeLevel, ClaudeFamiliarity, DegreeCategory
from config import Config

class ScoringEngineService:
    """Service for calculating application scores"""
    
    def __init__(self, config: Config = None):
        if config is None:
            config = Config()
        self.config = config
        # Get criteria from config or use defaults
        if hasattr(config, 'SCORING_CRITERIA'):
            self.criteria = config.SCORING_CRITERIA
        else:
            # Use default criteria if not in config
            from config import Config as DefaultConfig
            self.criteria = DefaultConfig.SCORING_CRITERIA
    
    def calculate_score(self, application_data: Dict) -> Dict:
        """Calculate total score and breakdown for an application"""
        breakdown = {}
        total_score = 0
        
        # 1. Degree Relevance Score
        degree_relevance = self._calculate_degree_relevance(
            application_data.get('degree_category')
        )
        breakdown['degree_relevance'] = degree_relevance
        total_score += degree_relevance
        
        # 2. Objective Quality Score
        objective_quality = self._evaluate_objective_quality(
            application_data.get('objective')
        )
        breakdown['objective_quality'] = objective_quality
        total_score += objective_quality
        
        # 3. Academic Standing Score
        academic_standing = self._calculate_academic_standing(
            application_data.get('degree_level'),
            application_data.get('year')
        )
        breakdown['academic_standing'] = academic_standing
        total_score += academic_standing
        
        # 4. Demonstrated Need Score
        demonstrated_need = self._calculate_demonstrated_need(
            application_data.get('financial_aid', False),
            application_data.get('first_generation', False),
            application_data.get('underrepresented', False)
        )
        breakdown['demonstrated_need'] = demonstrated_need
        total_score += demonstrated_need
        
        # 5. Claude Familiarity Score
        claude_familiarity = self._calculate_claude_familiarity(
            application_data.get('prior_claude_usage')
        )
        breakdown['claude_familiarity'] = claude_familiarity
        total_score += claude_familiarity
        
        # Ensure score is between 0 and 100
        total_score = min(max(total_score, 0), 100)
        
        return {
            'total': total_score,
            'breakdown': breakdown,
            'calculated_at': datetime.utcnow().isoformat()
        }
    
    def _calculate_degree_relevance(self, degree_category: str) -> int:
        """Calculate degree relevance score (0-30 points)"""
        weights = self.criteria['degree_relevance']['weights']
        return weights.get(degree_category, weights['Other'])
    
    def _evaluate_objective_quality(self, objective: str) -> int:
        """Evaluate objective quality (0-25 points)"""
        score = 0
        
        # Specificity (0-10 points)
        word_count = len(objective.split())
        if word_count >= 200:
            specificity = 10
        elif word_count >= 150:
            specificity = 8
        elif word_count >= 100:
            specificity = 6
        elif word_count >= 50:
            specificity = 4
        else:
            specificity = 0
        score += specificity
        
        # Feasibility (0-8 points)
        has_timeline = any(word in objective.lower() for word in 
                          ['timeline', 'schedule', 'plan', 'by', 'within', 'during'])
        has_deliverables = any(word in objective.lower() for word in 
                              ['deliverable', 'outcome', 'result', 'produce', 'create', 'build'])
        feasibility = (4 if has_timeline else 0) + (4 if has_deliverables else 0)
        score += feasibility
        
        # Relevance (0-7 points)
        relevance_keywords = {
            'Research': ['research', 'study', 'investigate', 'analyze'],
            'Thesis': ['thesis', 'dissertation', 'capstone'],
            'Project': ['project', 'build', 'develop', 'implement'],
            'Coursework': ['course', 'class', 'assignment'],
            'Other': []
        }
        
        relevance_weights = {
            'Research': 7,
            'Thesis': 7,
            'Project': 6,
            'Coursework': 5,
            'Other': 3
        }
        
        use_case = 'Other'
        for category, keywords in relevance_keywords.items():
            if any(keyword in objective.lower() for keyword in keywords):
                use_case = category
                break
        
        score += relevance_weights[use_case]
        
        return min(score, 25)
    
    def _calculate_academic_standing(self, degree_level: str, year: int) -> int:
        """Calculate academic standing score (0-20 points)"""
        weights = self.criteria['academic_standing']['weights']
        
        if degree_level == DegreeLevel.GRADUATE.value or degree_level == 'graduate':
            return weights['graduate']
        elif degree_level == DegreeLevel.PHD.value or degree_level == 'phd':
            return weights['graduate']  # PhD treated as graduate
        elif degree_level == DegreeLevel.UNDERGRADUATE.value or degree_level == 'undergraduate':
            if year == 4:
                return weights['undergraduate_senior']
            elif year == 3:
                return weights['undergraduate_junior']
            elif year == 2:
                return weights['undergraduate_sophomore']
            else:
                return weights['undergraduate_freshman']
        
        return 0
    
    def _calculate_demonstrated_need(self, financial_aid: bool, 
                                     first_generation: bool, 
                                     underrepresented: bool) -> int:
        """Calculate demonstrated need score (0-15 points)"""
        factors = self.criteria['demonstrated_need']['factors']
        score = 0
        
        if financial_aid:
            score += factors['financial_aid']
        if first_generation:
            score += factors['first_gen']
        if underrepresented:
            score += factors['underrepresented']
        
        return min(score, 15)
    
    def _calculate_claude_familiarity(self, prior_usage: str) -> int:
        """Calculate Claude familiarity score (0-10 points)"""
        weights = self.criteria['claude_familiarity']['weights']
        
        if isinstance(prior_usage, ClaudeFamiliarity):
            prior_usage = prior_usage.value
        
        return weights.get(prior_usage, weights['none'])
    
    def validate_score_bounds(self, score: Dict) -> Tuple[bool, str]:
        """Validate that score is within bounds (0-100)"""
        total = score.get('total', 0)
        
        if total < 0 or total > 100:
            return False, f"Score {total} is outside valid range [0, 100]"
        
        breakdown = score.get('breakdown', {})
        expected_sum = sum(breakdown.values())
        
        if expected_sum > 100:
            return False, f"Score breakdown sum {expected_sum} exceeds 100"
        
        return True, "Score is valid"
