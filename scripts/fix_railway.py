"""
Railway Fix Script
Fix Railway deployment configuration
"""

from pathlib import Path

def create_railway_fix():
    """Create fix for Railway deployment"""
    
    print("="*60)
    print("FIXING RAILWAY DEPLOYMENT")
    print("="*60)
    print()
    
    # Check if requirements.txt is in root
    root_requirements = Path("requirements.txt")
    api_requirements = Path("api/requirements.txt")
    
    if not root_requirements.exists() and api_requirements.exists():
        print("Creating root requirements.txt from api/requirements.txt...")
        with open(api_requirements, "r") as f:
            content = f.read()
        with open(root_requirements, "w") as f:
            f.write(content)
        print("[OK] Created requirements.txt in root")
    
    # Create nixpacks.toml for better Railway detection
    nixpacks = """[phases.setup]
nixPkgs = ["python311", "pip"]

[phases.install]
cmds = ["pip install -r api/requirements.txt"]

[start]
cmd = "cd api && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
"""
    
    nixpacks_file = Path("nixpacks.toml")
    with open(nixpacks_file, "w") as f:
        f.write(nixpacks)
    print("[OK] Created nixpacks.toml")
    
    print()
    print("Fixes applied!")
    print()
    print("Next steps:")
    print("1. Commit these changes:")
    print("   git add .")
    print("   git commit -m 'Fix Railway deployment'")
    print("   git push")
    print()
    print("2. Railway will auto-redeploy")
    print("3. Check logs to verify it works")
    print()

if __name__ == "__main__":
    create_railway_fix()

