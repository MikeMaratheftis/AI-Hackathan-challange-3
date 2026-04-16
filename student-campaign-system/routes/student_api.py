from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from models import (
    Student, Application, License, ProgressReport,
    ApplicationStatus, DegreeLevel, ClaudeFamiliarity
)

student_bp = Blueprint('student', __name__)

@student_bp.route('/applications', methods=['POST'])
def submit_application():
    """Submit a new application"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'name', 'institution', 'degree_program', 
                          'degree_level', 'year', 'objective', 'prior_claude_usage']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate application
        valid, validation_result = current_app.validator.validate_application(
            data['email'],
            data['institution'],
            data['degree_program'],
            data['objective']
        )
        
        if not valid:
            return jsonify({
                'error': 'Application validation failed',
                'errors': validation_result['errors']
            }), 400
        
        # Create or get student
        session = current_app.db_session()
        student = session.query(Student).filter_by(email=data['email']).first()
        
        if not student:
            student = Student(
                email=data['email'],
                name=data['name'],
                institution=data['institution'],
                institution_domain=data['email'].split('@')[1],
                degree_program=data['degree_program'],
                degree_level=data['degree_level'],
                year=data['year'],
                financial_aid=data.get('financial_aid', False),
                first_generation=data.get('first_generation', False)
            )
            session.add(student)
            session.commit()
        
        # Calculate score
        score_result = current_app.scoring_engine.calculate_score({
            'degree_category': validation_result['degree_category'].value,
            'objective': data['objective'],
            'degree_level': data['degree_level'],
            'year': data['year'],
            'financial_aid': data.get('financial_aid', False),
            'first_generation': data.get('first_generation', False),
            'prior_claude_usage': data['prior_claude_usage']
        })
        
        # Process allocation
        allocation_result = current_app.allocation_engine.process_allocation(
            data,
            score_result['total'],
            validation_result['degree_category'].value
        )
        
        # Create application
        application = Application(
            student_id=student.id,
            degree_program=data['degree_program'],
            degree_category=validation_result['degree_category'].value,
            objective=data['objective'],
            objective_category=validation_result['objective_category'].value,
            prior_claude_usage=data['prior_claude_usage'],
            status=allocation_result['status'],
            score_total=score_result['total'],
            score_breakdown=score_result['breakdown'],
            cutoff_score_used=allocation_result['cutoff_score'],
            scored_at=datetime.utcnow(),
            decided_at=datetime.utcnow()
        )
        session.add(application)
        session.commit()
        
        # Create license if approved
        if allocation_result['status'] == ApplicationStatus.APPROVED.value:
            license_data = current_app.license_manager.create_license(
                student.id,
                application.id
            )
            license = License(
                id=license_data['id'],
                application_id=application.id,
                student_id=student.id,
                claude_license_key=license_data['claude_license_key'],
                start_date=datetime.fromisoformat(license_data['start_date']),
                expiration_date=datetime.fromisoformat(license_data['expiration_date']),
                status=license_data['status']
            )
            session.add(license)
            session.commit()
            
            return jsonify({
                'application_id': application.id,
                'status': allocation_result['status'],
                'score': score_result['total'],
                'license_id': license.id,
                'license_key': license.claude_license_key,
                'expiration_date': license.expiration_date.isoformat()
            }), 201
        
        return jsonify({
            'application_id': application.id,
            'status': allocation_result['status'],
            'score': score_result['total'],
            'message': allocation_result['status'].replace('_', ' ').title()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/applications/<app_id>', methods=['GET'])
def get_application(app_id):
    """Get application status"""
    try:
        session = current_app.db_session()
        application = session.query(Application).filter_by(id=app_id).first()
        
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        return jsonify({
            'id': application.id,
            'status': application.status,
            'score': application.score_total,
            'score_breakdown': application.score_breakdown,
            'cutoff_score': application.cutoff_score_used,
            'created_at': application.created_at.isoformat(),
            'decided_at': application.decided_at.isoformat() if application.decided_at else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/licenses/<license_id>', methods=['GET'])
def get_license(license_id):
    """Get license details"""
    try:
        session = current_app.db_session()
        license = session.query(License).filter_by(id=license_id).first()
        
        if not license:
            return jsonify({'error': 'License not found'}), 404
        
        expiration_check = current_app.license_manager.check_license_expiration({
            'expiration_date': license.expiration_date.isoformat()
        })
        
        return jsonify({
            'id': license.id,
            'license_key': license.claude_license_key,
            'status': license.status,
            'start_date': license.start_date.isoformat(),
            'expiration_date': license.expiration_date.isoformat(),
            'days_remaining': expiration_check['days_remaining'],
            'extensions_used': license.extensions_granted,
            'total_extension_days': license.total_extension_days
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_bp.route('/licenses/<license_id>/progress-reports', methods=['POST'])
def submit_progress_report(license_id):
    """Submit progress report for license extension"""
    try:
        data = request.get_json()
        session = current_app.db_session()
        
        license = session.query(License).filter_by(id=license_id).first()
        if not license:
            return jsonify({'error': 'License not found'}), 404
        
        # Validate progress report
        valid, errors = current_app.license_manager.validate_progress_report(
            data,
            {
                'expiration_date': license.expiration_date.isoformat()
            }
        )
        
        if not valid:
            return jsonify({
                'error': 'Progress report validation failed',
                'errors': errors
            }), 400
        
        # Evaluate quality
        quality_score = current_app.license_manager.evaluate_progress_quality(data)
        
        # Evaluate extension
        extension_result = current_app.license_manager.evaluate_extension_request(
            {
                'extensions_granted': license.extensions_granted,
                'total_extension_days': license.total_extension_days,
                'expiration_date': license.expiration_date.isoformat()
            },
            data,
            quality_score
        )
        
        # Create progress report
        progress_report = ProgressReport(
            license_id=license.id,
            description=data.get('description', ''),
            claude_usage_examples=data.get('claude_usage_examples', ''),
            outcomes=data.get('outcomes', ''),
            status='approved' if extension_result['approved'] else 'pending',
            extension_days_granted=extension_result['extension_days']
        )
        session.add(progress_report)
        
        # Update license if extension approved
        if extension_result['approved']:
            license.extensions_granted += 1
            license.total_extension_days += extension_result['extension_days']
            license.expiration_date = datetime.fromisoformat(extension_result['new_expiration'])
        
        session.commit()
        
        return jsonify({
            'progress_report_id': progress_report.id,
            'status': progress_report.status,
            'quality_score': quality_score,
            'extension_approved': extension_result['approved'],
            'extension_days': extension_result['extension_days'],
            'new_expiration': extension_result['new_expiration'],
            'reason': extension_result['reason']
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
