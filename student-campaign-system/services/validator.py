import re
from typing import Dict, List, Tuple
from models import DegreeCategory, ObjectiveCategory

class ValidatorService:
    """Service for validating student applications"""
    
    # Known institutions and their domains
    INSTITUTION_DOMAINS = {
        "mit.edu": "Massachusetts Institute of Technology",
        "stanford.edu": "Stanford University",
        "berkeley.edu": "University of California, Berkeley",
        "harvard.edu": "Harvard University",
        "ucla.edu": "University of California, Los Angeles",
        "columbia.edu": "Columbia University",
        "caltech.edu": "California Institute of Technology",
        "princeton.edu": "Princeton University",
        "yale.edu": "Yale University",
        "upenn.edu": "University of Pennsylvania",
    }
    
    # Degree program classifications
    STEM_PROGRAMS = {
        "computer science", "engineering", "mathematics", "physics", "chemistry",
        "biology", "molecular biology", "data science", "machine learning",
        "electrical engineering", "mechanical engineering", "civil engineering"
    }
    
    BUSINESS_PROGRAMS = {
        "business administration", "mba", "economics", "finance", "accounting",
        "management", "entrepreneurship", "marketing"
    }
    
    HUMANITIES_PROGRAMS = {
        "literature", "history", "philosophy", "languages", "classics",
        "art history", "music history", "cultural studies"
    }
    
    ARTS_PROGRAMS = {
        "fine arts", "music", "design", "theater", "dance", "film",
        "visual arts", "graphic design"
    }
    
    # Prohibited content patterns
    PROHIBITED_PATTERNS = [
        r"spam", r"commercial", r"advertising", r"marketing campaign",
        r"make money", r"get rich", r"cryptocurrency", r"forex"
    ]
    
    # Use case keywords
    USE_CASE_KEYWORDS = {
        ObjectiveCategory.RESEARCH: ["research", "study", "investigate", "analyze", "experiment"],
        ObjectiveCategory.THESIS: ["thesis", "dissertation", "capstone", "final project"],
        ObjectiveCategory.PROJECT: ["project", "build", "develop", "create", "implement"],
        ObjectiveCategory.COURSEWORK: ["course", "class", "assignment", "homework", "exam"],
    }
    
    @staticmethod
    def validate_email_domain(email: str) -> Tuple[bool, str]:
        """Validate that email is from an accredited institution"""
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return False, "Invalid email format"
        
        domain = email.split('@')[1].lower()
        
        if domain not in ValidatorService.INSTITUTION_DOMAINS:
            return False, f"Email domain {domain} is not from a recognized institution"
        
        return True, ValidatorService.INSTITUTION_DOMAINS[domain]
    
    @staticmethod
    def validate_institution(institution: str, domain: str) -> Tuple[bool, str]:
        """Validate that institution matches the email domain"""
        expected_institution = ValidatorService.INSTITUTION_DOMAINS.get(domain)
        
        if not expected_institution:
            return False, "Institution domain not recognized"
        
        return True, expected_institution
    
    @staticmethod
    def classify_degree_program(program: str) -> DegreeCategory:
        """Classify degree program into category"""
        program_lower = program.lower()
        
        if any(stem in program_lower for stem in ValidatorService.STEM_PROGRAMS):
            return DegreeCategory.STEM
        elif any(biz in program_lower for biz in ValidatorService.BUSINESS_PROGRAMS):
            return DegreeCategory.BUSINESS
        elif any(hum in program_lower for hum in ValidatorService.HUMANITIES_PROGRAMS):
            return DegreeCategory.HUMANITIES
        elif any(art in program_lower for art in ValidatorService.ARTS_PROGRAMS):
            return DegreeCategory.ARTS
        else:
            return DegreeCategory.OTHER
    
    @staticmethod
    def validate_objective(objective: str) -> Tuple[bool, List[str]]:
        """Validate objective content and length"""
        errors = []
        
        if len(objective) < 50:
            errors.append("Objective must be at least 50 characters")
        
        if len(objective) > 5000:
            errors.append("Objective must not exceed 5000 characters")
        
        # Check for prohibited content
        for pattern in ValidatorService.PROHIBITED_PATTERNS:
            if re.search(pattern, objective, re.IGNORECASE):
                errors.append(f"Objective contains prohibited content: {pattern}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def classify_objective(objective: str) -> ObjectiveCategory:
        """Classify objective into use case category"""
        objective_lower = objective.lower()
        
        for category, keywords in ValidatorService.USE_CASE_KEYWORDS.items():
            if any(keyword in objective_lower for keyword in keywords):
                return category
        
        return ObjectiveCategory.OTHER
    
    @staticmethod
    def validate_application(email: str, institution: str, degree_program: str, 
                            objective: str) -> Tuple[bool, Dict]:
        """Validate complete application"""
        errors = []
        warnings = []
        
        # Validate email domain
        email_valid, email_msg = ValidatorService.validate_email_domain(email)
        if not email_valid:
            errors.append(email_msg)
        else:
            institution_name = email_msg
        
        # Validate institution
        domain = email.split('@')[1].lower()
        inst_valid, inst_msg = ValidatorService.validate_institution(institution, domain)
        if not inst_valid:
            warnings.append(inst_msg)
        
        # Validate objective
        obj_valid, obj_errors = ValidatorService.validate_objective(objective)
        if not obj_valid:
            errors.extend(obj_errors)
        
        return len(errors) == 0, {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "institution_name": institution_name if email_valid else None,
            "degree_category": ValidatorService.classify_degree_program(degree_program),
            "objective_category": ValidatorService.classify_objective(objective)
        }
