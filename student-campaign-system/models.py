from datetime import datetime, timedelta
from enum import Enum
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DegreeLevel(str, Enum):
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    PHD = "phd"

class DegreeCategory(str, Enum):
    STEM = "STEM"
    BUSINESS = "Business"
    HUMANITIES = "Humanities"
    ARTS = "Arts"
    OTHER = "Other"

class ApplicationStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    VERIFIED = "verified"
    SCORED = "scored"
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"

class ObjectiveCategory(str, Enum):
    RESEARCH = "Research"
    THESIS = "Thesis"
    PROJECT = "Project"
    COURSEWORK = "Coursework"
    OTHER = "Other"

class ClaudeFamiliarity(str, Enum):
    EXPERIENCED = "experienced"
    MODERATE = "moderate"
    BEGINNER = "beginner"
    NONE = "none"

class LicenseStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"

class ProgressReportStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    institution_domain = Column(String(255), nullable=False)
    degree_program = Column(String(255), nullable=False)
    degree_level = Column(SQLEnum(DegreeLevel), nullable=False)
    year = Column(Integer, nullable=False)
    financial_aid = Column(Boolean, default=False)
    first_generation = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    applications = relationship("Application", back_populates="student")
    licenses = relationship("License", back_populates="student")

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey('students.id'), nullable=False)
    degree_program = Column(String(255), nullable=False)
    degree_category = Column(SQLEnum(DegreeCategory), nullable=False)
    objective = Column(Text, nullable=False)
    objective_category = Column(SQLEnum(ObjectiveCategory), nullable=True)
    prior_claude_usage = Column(SQLEnum(ClaudeFamiliarity), nullable=False)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.SUBMITTED)
    score_total = Column(Integer, nullable=True)
    score_breakdown = Column(JSON, nullable=True)
    cutoff_score_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scored_at = Column(DateTime, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    
    student = relationship("Student", back_populates="applications")
    license = relationship("License", back_populates="application", uselist=False)

class License(Base):
    __tablename__ = 'licenses'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id = Column(String(36), ForeignKey('applications.id'), nullable=False)
    student_id = Column(String(36), ForeignKey('students.id'), nullable=False)
    claude_license_key = Column(String(255), nullable=False, unique=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=False)
    extensions_granted = Column(Integer, default=0)
    total_extension_days = Column(Integer, default=0)
    status = Column(SQLEnum(LicenseStatus), default=LicenseStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    application = relationship("Application", back_populates="license")
    student = relationship("Student", back_populates="licenses")
    progress_reports = relationship("ProgressReport", back_populates="license")

class ProgressReport(Base):
    __tablename__ = 'progress_reports'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    license_id = Column(String(36), ForeignKey('licenses.id'), nullable=False)
    description = Column(Text, nullable=False)
    claude_usage_examples = Column(Text, nullable=False)
    outcomes = Column(Text, nullable=False)
    status = Column(SQLEnum(ProgressReportStatus), default=ProgressReportStatus.PENDING)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    reviewer_id = Column(String(36), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    extension_days_granted = Column(Integer, default=0)
    
    license = relationship("License", back_populates="progress_reports")
