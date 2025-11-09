"""
Git Push Guide
Step-by-step guide to push code to GitHub
"""

def create_push_guide():
    """Create push guide"""
    
    guide = """# Push Code to GitHub - Step by Step

## Step 1: Create the Repository on GitHub

On the GitHub page you're on:

1. ✅ Repository name: `ai-decision-engine-api` (already filled, looks good!)
2. ✅ Owner: `lowriskbtc` (your username)
3. ✅ Visibility: **Public** (good for open source)
4. ❌ **DON'T check** "Add README" (we already have code)
5. ❌ **DON'T check** "Add .gitignore" (we already have one)
6. ❌ **DON'T check** "Add license" (optional, skip for now)

7. **Click the green "Create repository" button**

---

## Step 2: After Creating Repository

GitHub will show you a page with setup instructions. 

**IGNORE those instructions** - we'll use the commands below instead.

---

## Step 3: Push Your Code

Open PowerShell in your project folder and run these commands **one at a time**:

### Command 1: Add all files
```powershell
git add .
```
This stages all your files for commit.

### Command 2: Commit the files
```powershell
git commit -m "Initial commit - AI Decision Engine API"
```
This creates your first commit.

### Command 3: Set main branch
```powershell
git branch -M main
```
This ensures you're on the main branch.

### Command 4: Add GitHub remote
```powershell
git remote add origin https://github.com/lowriskbtc/ai-decision-engine-api.git
```
This connects your local repo to GitHub.

### Command 5: Push to GitHub
```powershell
git push -u origin main
```
This uploads your code to GitHub.

**Note:** If this asks for username/password:
- Username: `lowriskbtc`
- Password: Use a **Personal Access Token** (not your GitHub password)
  - Get token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Create token with "repo" permissions
  - Use token as password

---

## Step 4: Verify

After pushing, go to:
`https://github.com/lowriskbtc/ai-decision-engine-api`

You should see all your files there!

---

## Step 5: Back to Railway

1. Go back to Railway
2. Type: `lowriskbtc/ai-decision-engine-api`
3. Railway will find your repo
4. Click to deploy!

---

## Troubleshooting

### "Repository not found"
- Make sure you clicked "Create repository" on GitHub first
- Check the repository name matches exactly

### "Authentication failed"
- GitHub requires Personal Access Token (not password)
- Create token: GitHub → Settings → Developer settings → Personal access tokens
- Use token as password when pushing

### "Remote origin already exists"
- Run: `git remote remove origin`
- Then run the `git remote add origin` command again

---

**Ready? Let's do it step by step!**

"""
    
    with open("PUSH_TO_GITHUB_STEPS.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("Push guide created: PUSH_TO_GITHUB_STEPS.md")

if __name__ == "__main__":
    create_push_guide()

