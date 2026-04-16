import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///student_campaign.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # License settings
    DEFAULT_LICENSE_PERIOD_DAYS = 90
    MAX_EXTENSIONS_PER_LICENSE = 3
    MAX_TOTAL_EXTENSION_DAYS = 90
    EXTENSION_DAYS_PER_REPORT = 30
    
    # Scoring settings
    SCORING_CRITERIA = {
        "degree_relevance": {
            "max_points": 30,
            "weights": {
                "STEM": 30,
                "Business": 25,
                "Humanities": 20,
                "Arts": 15,
                "Other": 10
            }
        },
        "objective_quality": {
            "max_points": 25,
            "factors": {
                "specificity": 10,
                "feasibility": 8,
                "relevance": 7
            }
        },
        "academic_standing": {
            "max_points": 20,
            "weights": {
                "graduate": 20,
                "undergraduate_senior": 15,
                "undergraduate_junior": 12,
                "undergraduate_sophomore": 8,
                "undergraduate_freshman": 5
            }
        },
        "demonstrated_need": {
            "max_points": 15,
            "factors": {
                "financial_aid": 8,
                "first_gen": 4,
                "underrepresented": 3
            }
        },
        "claude_familiarity": {
            "max_points": 10,
            "weights": {
                "experienced": 10,
                "moderate": 7,
                "beginner": 4,
                "none": 0
            }
        }
    }
    
    # Cutoff scores by degree category
    DEFAULT_CUTOFF_SCORES = {
        "STEM": 60,
        "Business": 55,
        "Humanities": 50,
        "Arts": 45,
        "Other": 50
    }
    
    # Progress report settings
    PROGRESS_QUALITY_THRESHOLD = 70
    PROGRESS_REPORT_MIN_CHARS = 100
    PROGRESS_REPORT_SUBMISSION_WINDOW_DAYS = 30

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
