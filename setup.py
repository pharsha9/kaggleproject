"""
Setup script to help users configure the BI Intelligence Agent System.
Guides through installation and configuration process.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_step(number, text):
    """Print a step number and description."""
    print(f"\n{'='*70}")
    print(f"STEP {number}: {text}")
    print('='*70)


def check_python_version():
    """Check if Python version is compatible."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 9:
        print("✅ Python version is compatible (3.9+)")
        return True
    else:
        print("❌ Python 3.9 or higher is required")
        print("Please upgrade Python: https://www.python.org/downloads/")
        return False


def install_dependencies():
    """Install required Python packages."""
    print_step(2, "Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install dependencies: {e}")
        print("Try manually: pip install -r requirements.txt")
        return False


def setup_environment():
    """Set up environment configuration."""
    print_step(3, "Setting Up Environment Configuration")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("Overwrite? (y/n): ").lower()
        if response != 'y':
            print("Keeping existing .env file")
            return True
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    # Copy example to .env
    with open(env_example, 'r') as f:
        content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ Created .env file from template")
    return True


def configure_api_key():
    """Guide user through API key configuration."""
    print_step(4, "Configuring Google AI API Key")
    
    print("You need a Google AI API key to use this system.")
    print("Get one for free at: https://aistudio.google.com/app/apikey")
    print()
    
    has_key = input("Do you have an API key? (y/n): ").lower()
    
    if has_key != 'y':
        print("\n📝 Please:")
        print("   1. Visit https://aistudio.google.com/app/apikey")
        print("   2. Create an API key")
        print("   3. Run this setup script again")
        return False
    
    api_key = input("\nEnter your API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    # Update .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        with open(env_file, 'w') as f:
            for line in lines:
                if line.startswith("GOOGLE_API_KEY="):
                    f.write(f"GOOGLE_API_KEY={api_key}\n")
                else:
                    f.write(line)
        
        print("✅ API key configured successfully")
        return True
    else:
        print("❌ .env file not found")
        return False


def create_directories():
    """Create necessary directories."""
    print_step(5, "Creating Output Directories")
    
    directories = ['data', 'outputs', 'reports', 'memory', 'data/examples']
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    return True


def verify_setup():
    """Verify the setup is complete."""
    print_step(6, "Verifying Setup")
    
    checks = []
    
    # Check .env exists
    if Path(".env").exists():
        print("✅ Configuration file (.env) exists")
        checks.append(True)
    else:
        print("❌ Configuration file (.env) not found")
        checks.append(False)
    
    # Check API key is set
    try:
        from config import Config
        Config.validate()
        print("✅ API key is configured")
        checks.append(True)
    except Exception as e:
        print(f"❌ API key not configured: {e}")
        checks.append(False)
    
    # Check sample data exists
    if Path("data/examples/sales_data.csv").exists():
        print("✅ Sample data files exist")
        checks.append(True)
    else:
        print("❌ Sample data files not found")
        checks.append(False)
    
    # Check required modules can be imported
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        from google import genai
        print("✅ All required packages are importable")
        checks.append(True)
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        checks.append(False)
    
    return all(checks)


def run_test():
    """Run a simple test to verify everything works."""
    print_step(7, "Running Test Analysis")
    
    print("Testing the system with sample data...")
    print("This may take 30-60 seconds...\n")
    
    try:
        # Import and run a quick test
        from agents import CoordinatorAgent
        from memory import MemoryBank
        from config import Config
        
        Config.validate()
        
        data_file = "data/examples/sales_data.csv"
        if not Path(data_file).exists():
            print(f"❌ Sample data not found: {data_file}")
            return False
        
        print(f"Analyzing: {data_file}")
        
        memory_bank = MemoryBank()
        coordinator = CoordinatorAgent(memory_bank)
        
        results = coordinator.analyze_file(data_file)
        
        if results.get("success"):
            print("\n✅ Test completed successfully!")
            print(f"   Report: {results['report_path']}")
            print(f"   Insights: {len(results.get('insights', []))}")
            print(f"   Visualizations: {len(results.get('visualizations', []))}")
            return True
        else:
            print(f"\n❌ Test failed: {results.get('error', 'Unknown error')}")
            return False
    
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_next_steps():
    """Print next steps after setup."""
    print_header("🎉 SETUP COMPLETE!")
    
    print("Your BI Intelligence Agent System is ready to use!\n")
    
    print("📖 Quick Commands:\n")
    print("   # Run feature demo")
    print("   python demo.py\n")
    
    print("   # Analyze sample data")
    print("   python main.py analyze data/examples/sales_data.csv\n")
    
    print("   # Analyze your own data")
    print("   python main.py analyze path/to/your/data.csv\n")
    
    print("   # View previous sessions")
    print("   python main.py list-sessions\n")
    
    print("📚 Documentation:\n")
    print("   README.md         - Complete documentation")
    print("   QUICKSTART.md     - 5-minute quick start")
    print("   DEPLOYMENT.md     - Production deployment")
    print("   CAPSTONE_WRITEUP.md - Project details\n")
    
    print("🎯 Next Steps:\n")
    print("   1. Run: python demo.py")
    print("   2. Open generated HTML report in browser")
    print("   3. Try analyzing your own data\n")
    
    print("💡 Need Help?")
    print("   Check README.md for detailed documentation\n")


def main():
    """Main setup function."""
    print_header("🚀 BI Intelligence Agent System - Setup Wizard")
    
    print("This wizard will guide you through setting up the system.\n")
    print("You'll need:")
    print("  • Python 3.9 or higher")
    print("  • Internet connection")
    print("  • Google AI API key (free)\n")
    
    input("Press Enter to begin setup...")
    
    # Run setup steps
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        print("\n⚠️  Warning: Dependency installation failed")
        print("Try manually: pip install -r requirements.txt")
        cont = input("\nContinue anyway? (y/n): ").lower()
        if cont != 'y':
            sys.exit(1)
    
    if not setup_environment():
        print("❌ Failed to set up environment")
        sys.exit(1)
    
    if not configure_api_key():
        print("\n⚠️  Setup incomplete - API key not configured")
        print("You can set it later in the .env file")
        sys.exit(1)
    
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    if not verify_setup():
        print("\n⚠️  Setup verification failed")
        print("Please check the errors above and fix them")
        sys.exit(1)
    
    # Ask if user wants to run test
    run_test_now = input("\nRun test analysis now? (y/n): ").lower()
    if run_test_now == 'y':
        if not run_test():
            print("\n⚠️  Test failed, but system may still work")
            print("Check the error messages above")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

