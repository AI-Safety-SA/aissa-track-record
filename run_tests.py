#!/usr/bin/env python3
"""
Test runner script for the AISSA Track Record application.
Run this script to execute all unit tests.

Usage:
    python run_tests.py

Make sure to install dependencies first:
    pip install -r requirements.txt
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'altair'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def run_tests():
    """Run the unit tests"""
    print("🧪 Running AISSA Track Record Unit Tests")
    print("=" * 50)
    
    if not check_dependencies():
        return False
    
    try:
        # Run the tests
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'test_app.py', '-v'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main function"""
    print("🤖 AISSA Track Record - Test Runner")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n🎉 Test run completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Test run failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
