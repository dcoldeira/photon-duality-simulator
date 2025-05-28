#!/usr/bin/env python3
"""
Setup script for Photon Duality Simulator
Automates virtual environment creation and dependency installation
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a shell command and handle errors."""
    print(f"📦 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {cmd}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🌟 Photon Duality Simulator Setup")
    print("=" * 50)
    
    # Detect platform
    system = platform.system()
    print(f"Detected OS: {system}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {python_version.major}.{python_version.minor}")
        sys.exit(1)
    
    print(f"✓ Python version: {python_version.major}.{python_version.minor}")
    
    # Create virtual environment
    if not os.path.exists("venv"):
        print("\n🔧 Creating virtual environment...")
        if not run_command("python -m venv venv", "Virtual environment creation"):
            sys.exit(1)
    else:
        print("✓ Virtual environment already exists")
    
    # Determine activation command
    if system == "Windows":
        activate_cmd = r"venv\Scripts\activate"
        pip_cmd = r"venv\Scripts\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    install_cmd = f"{pip_cmd} install -r requirements.txt"
    if not run_command(install_cmd, "Dependency installation"):
        sys.exit(1)
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    verify_cmd = f"{pip_cmd} list"
    run_command(verify_cmd, "Package verification")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\nTo run the simulator:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print("2. Run simulator: python dark_light_interference_simulator.py")
    print("\nTo deactivate when finished: deactivate")
    print("\n✨ Happy quantum computing!")

if __name__ == "__main__":
    main()
