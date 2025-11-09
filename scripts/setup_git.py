"""
GitHub Setup Script
Set up git and prepare for GitHub push
"""

import subprocess
from pathlib import Path

def setup_git():
    """Set up git repository"""
    print("="*60)
    print("SETTING UP GIT FOR GITHUB")
    print("="*60)
    print()
    
    # Check if git is installed
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Git installed: {result.stdout.strip()}")
        else:
            print("[ERROR] Git not found")
            return False
    except:
        print("[ERROR] Git not found. Please install Git first.")
        return False
    
    # Check if already a git repo
    git_dir = Path(".git")
    if git_dir.exists():
        print("[INFO] Already a git repository")
        return True
    
    # Initialize git
    print("Initializing git repository...")
    try:
        subprocess.run(["git", "init"], check=True, timeout=5)
        print("[OK] Git repository initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize git: {e}")
        return False
    
    # Check .gitignore
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        print("[WARNING] .gitignore not found, creating one...")
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# API Keys and Secrets
api_keys.json
*.env
.env
.env.local

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backups
BACKUP_*/
backups/

# Analytics
api_analytics.json
health_monitor.log
"""
        with open(gitignore, "w") as f:
            f.write(gitignore_content)
        print("[OK] .gitignore created")
    
    print()
    print("[SUCCESS] Git repository ready!")
    print()
    print("Next steps:")
    print("1. Create repository on GitHub (github.com)")
    print("2. Run these commands:")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/your-username/your-repo.git")
    print("   git push -u origin main")
    print()
    print("Then come back to Railway and select your repository!")
    
    return True

if __name__ == "__main__":
    setup_git()

