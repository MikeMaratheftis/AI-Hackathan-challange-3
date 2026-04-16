#!/usr/bin/env python3
"""
Simple setup script to install dependencies and run the application
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"⚠️  {description} - Failed")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 Student Campaign License Allocation System - Setup")
    print("="*60)
    
    # Check Python version
    print(f"\n🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        sys.exit(1)
    
    # Upgrade pip
    print("\n📦 Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Pip upgrade")
    
    # Try installing with requirements-minimal.txt first
    print("\n📦 Installing minimal requirements...")
    if run_command(f"{sys.executable} -m pip install -r requirements-minimal.txt", "Minimal requirements"):
        print("✅ Minimal requirements installed successfully!")
    else:
        print("⚠️  Minimal requirements failed, trying individual packages...")
        
        packages = [
            ("Flask", "Flask>=2.0.0"),
            ("Flask-CORS", "Flask-CORS>=3.0.0"),
            ("SQLAlchemy", "SQLAlchemy>=1.4.0"),
            ("python-dotenv", "python-dotenv>=0.19.0"),
        ]
        
        for name, package in packages:
            if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {name}"):
                print(f"❌ Failed to install {name}")
                sys.exit(1)
    
    # Verify installation
    print("\n✅ Verifying installation...")
    try:
        import flask
        import flask_cors
        import sqlalchemy
        import dotenv
        print("✅ All required packages installed successfully!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    
    # Create .env if it doesn't exist
    if not os.path.exists('.env'):
        print("\n⚙️  Creating .env file...")
        with open('.env', 'w') as f:
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_APP=app.py\n")
            f.write("DATABASE_URL=sqlite:///student_campaign.db\n")
            f.write("SECRET_KEY=dev-secret-key\n")
        print("✅ .env file created")
    
    # Initialize database
    print("\n🗄️  Initializing database...")
    try:
        from app import create_app
        app = create_app()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization: {e}")
    
    print("\n" + "="*60)
    print("🎉 Setup complete!")
    print("="*60)
    print("\n📱 To start the application:")
    print("   python app.py")
    print("\n🌐 Then open: http://localhost:5000")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
