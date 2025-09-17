#!/usr/bin/env python3
"""
Complete setup script for the Career Tracking Application
This script will:
1. Install all Python dependencies
2. Create ML models
3. Seed the database with sample data
4. Verify the setup
"""

import subprocess
import sys
import os
from pathlib import Path
import asyncio

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        print(f"✅ {command}")
        return True
    except Exception as e:
        print(f"❌ Error running {command}: {e}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    # Change to backend directory
    backend_dir = Path("career-tracking-backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Install requirements
    success = run_command("pip install -r requirements.txt", cwd=backend_dir)
    if success:
        print("✅ Python dependencies installed successfully!")
    return success

def create_ml_models():
    """Create and save ML models"""
    print("\n🤖 Creating ML models...")
    
    backend_dir = Path("career-tracking-backend")
    
    # Run the ML model creation script
    success = run_command("python create_ml_model.py", cwd=backend_dir)
    if success:
        print("✅ ML models created successfully!")
    return success

def seed_database():
    """Seed the database with sample data"""
    print("\n🌱 Seeding database with sample data...")
    
    backend_dir = Path("career-tracking-backend")
    
    # Run the database seeding script
    success = run_command("python seed_data.py", cwd=backend_dir)
    if success:
        print("✅ Database seeded successfully!")
    return success

def install_frontend_dependencies():
    """Install Node.js dependencies for frontend"""
    print("\n🎨 Installing Frontend dependencies...")
    
    frontend_dir = Path("Frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Install npm dependencies
    success = run_command("npm install", cwd=frontend_dir)
    if success:
        print("✅ Frontend dependencies installed successfully!")
    return success

def verify_setup():
    """Verify that everything is set up correctly"""
    print("\n🔍 Verifying setup...")
    
    # Check if required files exist
    required_files = [
        "career-tracking-backend/app/ml/models/career_recommender.pkl",
        "career-tracking-backend/app/ml/models/course_features.pkl",
        "Frontend/node_modules",
        "career-tracking-backend/.env"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing!")
            all_good = False
    
    return all_good

def main():
    """Main setup function"""
    print("🚀 Setting up Career Tracking Application...")
    print("=" * 50)
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    steps = [
        ("Installing Python Dependencies", install_python_dependencies),
        ("Creating ML Models", create_ml_models),
        ("Installing Frontend Dependencies", install_frontend_dependencies),
        ("Seeding Database", seed_database),
        ("Verifying Setup", verify_setup)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        try:
            if not step_function():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    if not failed_steps:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Make sure PostgreSQL is running on port 5433")
        print("2. Run 'start-all.bat' to start both servers")
        print("3. Access the application:")
        print("   - Frontend: http://localhost:3000")
        print("   - Backend API: http://localhost:8000")
        print("   - API Documentation: http://localhost:8000/docs")
    else:
        print("❌ Setup completed with some issues:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease check the errors above and try running the failed steps manually.")

if __name__ == "__main__":
    main()
