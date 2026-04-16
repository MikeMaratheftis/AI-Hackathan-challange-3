from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func
from models import Application, License, Student, ProgressReport, ApplicationStatus

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/applications', methods=['GET'])
def list_applications():
    """List applications with filtering"""
    try:
        session = current_app.db_session()
        
        # Get filter parameters
        status = request.args.get('status')
        degree_category = request.args.get('degree_category')
        min_score = request.args.get('min_score', type=int)
        max_score = request.args.get('max_score', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        
        query = session.query(Application)
        
        if status:
            query = query.filter_by(status=status)
        if degree_category:
            query = query.filter_by(degree_category=degree_category)
        if min_score is not None:
            query = query.filter(Application.score_total >= min_score)
        if max_score is not None:
            query = query.filter(Application.score_total <= max_score)
        
        total = query.count()
        applications = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return jsonify({
            'total': total,
            'page': page,
            'per_page': per_page,
            'applications': [
                {
                    'id': app.id,
                    'student_name': app.student.name,
                    'degree_category': app.degree_category,
                    'score': app.score_total,
                    'status': app.status,
                    'created_at': app.created_at.isoformat()
                }
                for app in applications
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get aggregate statistics"""
    try:
        session = current_app.db_session()
        
        total_apps = session.query(func.count(Application.id)).scalar()
        approved = session.query(func.count(Application.id)).filter_by(
            status=ApplicationStatus.APPROVED.value
        ).scalar()
        rejected = session.query(func.count(Application.id)).filter_by(
            status=ApplicationStatus.REJECTED.value
        ).scalar()
        waitlisted = session.query(func.count(Application.id)).filter_by(
            status=ApplicationStatus.WAITLISTED.value
        ).scalar()
        
        # Score statistics
        scores = session.query(Application.score_total).filter(
            Application.score_total.isnot(None)
        ).all()
        scores = [s[0] for s in scores]
        
        avg_score = sum(scores) / len(scores) if scores else 0
        median_score = sorted(scores)[len(scores)//2] if scores else 0
        
        # License statistics
        total_licenses = session.query(func.count(License.id)).scalar()
        active_licenses = session.query(func.count(License.id)).filter_by(
            status='active'
        ).scalar()
        expired_licenses = session.query(func.count(License.id)).filter_by(
            status='expired'
        ).scalar()
        
        available_licenses = current_app.allocation_engine.get_available_licenses()
        
        return jsonify({
            'applications': {
                'total': total_apps,
                'approved': approved,
                'rejected': rejected,
                'waitlisted': waitlisted,
                'approval_rate': (approved / total_apps * 100) if total_apps > 0 else 0
            },
            'scores': {
                'average': round(avg_score, 2),
                'median': median_score,
                'count': len(scores)
            },
            'licenses': {
                'total_allocated': total_licenses,
                'active': active_licenses,
                'expired': expired_licenses,
                'available': available_licenses
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/config/cutoff-scores', methods=['GET'])
def get_cutoff_scores():
    """Get current cutoff scores"""
    try:
        return jsonify({
            'cutoff_scores': current_app.allocation_engine.cutoff_scores
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/config/cutoff-scores', methods=['PUT'])
def update_cutoff_scores():
    """Update cutoff scores"""
    try:
        data = request.get_json()
        
        for degree_category, score in data.items():
            success, message = current_app.allocation_engine.update_cutoff_score(
                degree_category,
                score
            )
            if not success:
                return jsonify({'error': message}), 400
        
        return jsonify({
            'message': 'Cutoff scores updated',
            'cutoff_scores': current_app.allocation_engine.cutoff_scores
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/inventory', methods=['GET'])
def get_inventory():
    """Get license inventory status"""
    try:
        session = current_app.db_session()
        
        total_allocated = session.query(func.count(License.id)).scalar()
        available = current_app.allocation_engine.get_available_licenses()
        
        return jsonify({
            'total_pool': total_allocated + available,
            'allocated': total_allocated,
            'available': available,
            'utilization_rate': (total_allocated / (total_allocated + available) * 100) 
                               if (total_allocated + available) > 0 else 0
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
