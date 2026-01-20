import subprocess
import os
import sys

def run_command(command, description):
    print(f"--- {description} ---")
    try:
        # We use shell=True for Windows compatibility with git
        process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}:")
        print(e.stderr)
        return False

def main():
    print("🚀 ForgeSentry GitHub Auto-Uploader")
    print("===============================")

    # 1. Check if Git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git from git-scm.com")
        return

    # 2. Check if .git exists, if not init
    if not os.path.exists(".git"):
        run_command("git init", "Initializing Git repository")
    
    # NEW: Set identity automatically
    run_command('git config user.email "MalikHamza7@users.noreply.github.com"', "Setting Git Email")
    run_command('git config user.name "MalikHamza7"', "Setting Git Name")
    
    # 3. Ask for the GitHub Repo URL if origin doesn't exist
    try:
        check_remote = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
        if check_remote.returncode != 0:
            repo_url = input("\n📝 Enter your GitHub Repository URL (e.g., https://github.com/your-username/your-repo.git): ").strip()
            if not repo_url:
                print("❌ Repository URL is required.")
                return
            run_command(f"git remote add origin {repo_url}", "Adding remote origin")
    except Exception:
        pass

    # 4. Git Add
    run_command("git add .", "Staging all files and screenshots")

    # 5. Git Commit
    commit_msg = "Initial commit: ForgeSentry AI-Powered IoT Threat Intelligence System"
    run_command(f'git commit -m "{commit_msg}"', "Committing changes")

    # 6. Branch setup
    run_command("git branch -M main", "Setting branch to main")

    # 7. Push
    print("\n📦 Attempting to push to GitHub...")
    print("💡 NOTE: If prompted for a password, use your 'Personal Access Token' (PAT).")
    success = run_command("git push -u origin main", "Pushing to main branch")

    if success:
        print("\n✅ PROJECT SUCCESSFULLY UPLOADED TO GITHUB!")
        print("Check your repository online now.")
    else:
        print("\n❌ Push failed. If it asked for a password, ensure you used a PAT.")

if __name__ == "__main__":
    main()
