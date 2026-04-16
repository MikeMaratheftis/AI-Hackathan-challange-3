from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from config import Config, DevelopmentConfig
from models import Base
from services.validator import ValidatorService
from services.scoring_engine import ScoringEngineService
from services.allocation_engine import AllocationEngineService
from services.license_manager import LicenseManagerService

def create_app(config_class=DevelopmentConfig):
    """Application factory"""
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    app.db_session = Session
    
    # Initialize services with config_class (not app.config)
    app.validator = ValidatorService()
    app.scoring_engine = ScoringEngineService(config_class)
    app.allocation_engine = AllocationEngineService(config_class)
    app.license_manager = LicenseManagerService(config_class)
    
    # Register blueprints
    from routes.student_api import student_bp
    from routes.admin_api import admin_bp
    
    app.register_blueprint(student_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Serve static files
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Student Campaign License Allocation System")
    print("📱 Frontend: http://localhost:5000")
    print("🔌 API: http://localhost:5000/api")
    app.run(debug=True, port=5000)
