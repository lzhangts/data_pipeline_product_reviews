import os
import subprocess

def load_data(repo_url):
    git_cmd = "git"

    # Initialize Git repo if it doesn't exist
    if not os.path.exists(".git"):
        subprocess.run([git_cmd, "init"], check=True)
        subprocess.run([git_cmd, "branch", "-M", "main"], check=True)
        subprocess.run([git_cmd, "remote", "add", "origin", repo_url], check=True)
    else:
        # Update remote URL in case it changed
        subprocess.run([git_cmd, "remote", "set-url", "origin", repo_url], check=True)

    # Stage all changes
    subprocess.run([git_cmd, "add", "."], check=True)

    # Configure Git user info
    subprocess.run([git_cmd, "config", "user.name", "auto-user"], check=True)
    subprocess.run([git_cmd, "config", "user.email", "auto@example.com"], check=True)

    # Commit changes (allow empty commit)
    subprocess.run([git_cmd, "commit", "--allow-empty", "-m", "Publish processed data"], check=True)

    # Force push to make remote match local
    subprocess.run([git_cmd, "push", "-u", "origin", "main", "--force"], check=True)

    print(f"Published updates to GitHub repo: {repo_url}")