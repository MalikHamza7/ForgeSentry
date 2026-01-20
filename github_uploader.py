import subprocess
import os

def run_git_command(args):
    try:
        result = subprocess.run(['git'] + args, capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during {' '.join(args)}:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")
        return False

def main():
    print("ForgeSentry GitHub Auto-Uploader")
    print("===============================")

    # 1. Check Git version
    if not run_git_command(['--version']):
        return

    # 2. Configure Git Identity
    print("Configuring Git Identity (MalikHamza7)...")
    run_git_command(['config', 'user.email', 'malikhamza7@example.com'])
    run_git_command(['config', 'user.name', 'MalikHamza7'])

    # 3. Initialize repository if not already one
    if not os.path.exists(".git"):
        print("Initializing new Git repository...")
        run_git_command(['init'])

    # 4. Add all files
    print("Staging files...")
    run_git_command(['add', '.'])

    # 5. Commit
    commit_msg = "Final Titan V3 Update: Enterprise A-Z Threat Intelligence System"
    print(f"Committing changes: {commit_msg}")
    run_git_command(['commit', '-m', commit_msg])

    # 6. Branch
    run_git_command(['branch', '-M', 'main'])

    # 7. Push
    repo_url = input("Please enter your GitHub repository URL (e.g., https://github.com/MalikHamza7/ForgeSentry.git): ")
    if repo_url:
        print(f"Adding remote origin: {repo_url}")
        # Remove existing origin if exists
        subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
        run_git_command(['remote', 'add', 'origin', repo_url])
        
        print("Pushing to GitHub...")
        print("Note: You may be prompted for your username and Personal Access Token (PAT).")
        run_git_command(['push', '-u', 'origin', 'main', '--force'])

if __name__ == "__main__":
    main()
