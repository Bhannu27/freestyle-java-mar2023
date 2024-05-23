
import os
import subprocess
import requests
import sys
 
def fetch_repository_details(repo_name, github_token):
    org_name = "Sanofi-GitHub"
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repository details for {repo_name}.")
        print(f"Response: {response.text}")
        return None
 
def update_branch_protection(repo_name, github_token, enable_linear_history, allow_force_pushes, force_push_teams=None):
    org_name = "Sanofi-GitHub"
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/branches/main/protection"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    protection_rules = {
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismissal_restrictions": {
                "users": [
                    "DarpanGitH", 
                    "atanudg",
                    "sreedharchc",
                    "E0565043",
                    "dilipkumarsanofi",
                    "rahulsonwane03",
                    "U1005319"
                ],
                "teams": [
                    "chc-admins"
                ]
            },
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 1,
            "require_last_push_approval": False,
            "bypass_pull_request_allowances": {
                "users": [
                    "DarpanGitH", 
                    "atanudg",
                    "sreedharchc",
                    "E0565043",
                    "dilipkumarsanofi",
                    "rahulsonwane03",
                    "U1005319"
                ],
                "teams": [
                    "chc-admins"
                ]
            }
        },
        "restrictions": {
            "users": [
                "DarpanGitH", 
                "atanudg",
                "sreedharchc",
                "E0565043",
                    "dilipkumarsanofi",
                    "rahulsonwane03",
                    "U1005319"
                ],
                "teams": [
                    "chc-admins"
                ]
            },
            "required_linear_history": enable_linear_history,
            "allow_force_pushes": allow_force_pushes,
            "allow_deletions": False,
            "block_creations": False,
            "required_conversation_resolution": True,
            "lock_branch": False
        }
 
    if allow_force_pushes:
        protection_rules["bypass_force_push_allowances"] = {
            "users": [],
            "teams": force_push_teams if force_push_teams else []
        }
 
    response = requests.put(url, headers=headers, json=protection_rules)
    if response.status_code == 200:
        print(f"Updated branch protection rules for {repo_name}.")
    else:
        print(f"Failed to update branch protection rules for {repo_name}.")
        print(f"Response: {response.text}")
 
def merge_branches(github_token, git_email, git_username, workspace):
    main_branch = "main"
    dev_branch = "development"
    repo_file = "calling-workflows/repository.txt"
 
    current_dir = os.getcwd()
 
    with open(repo_file, 'r') as file:
        for repo_name in file:
            repo_name = repo_name.strip()
            print(f"Merging {dev_branch} into {main_branch} for repository: {repo_name}", flush=True)
 
            repo_details = fetch_repository_details(repo_name, github_token)
            if repo_details is None:
                continue
 
            clone_url = repo_details.get('clone_url')
            print("Clone URL:", clone_url)
            if clone_url is None:
                print(f"Clone URL not found for repository: {repo_name}", flush=True)
                continue
 
            # Navigate to the repository directory
            repo_path = os.path.join(workspace, repo_name)
            os.makedirs(repo_path, exist_ok=True)
            os.chdir(repo_path)
 
            # Set the remote URL of the repository to the clone URL
            print(f"Setting remote URL to: {clone_url}", flush=True)
            subprocess.run(["git", "remote", "set-url", "origin", clone_url])
 
            # Set the Git user email and username
            subprocess.run(["git", "config", "--global", "user.email", git_email])
            subprocess.run(["git", "config", "--global", "user.name", git_username])
 
            # Temporarily disable linear history and allow force pushes
            update_branch_protection(repo_name, github_token, enable_linear_history=False, allow_force_pushes=True, force_push_teams=["chc-admins"])
 
            # Checkout and pull latest changes from main branch
            print("Fetching the latest changes from main branch...", flush=True)
            subprocess.run(["git", "fetch", "origin", main_branch])
            subprocess.run(["git", "checkout", main_branch])
            subprocess.run(["git", "pull", "origin", main_branch])
 
            # Checkout and pull latest changes from development branch
            print("Fetching the latest changes from development branch...", flush=True)
            subprocess.run(["git", "fetch", "origin", dev_branch])
            subprocess.run(["git", "checkout", dev_branch])
            subprocess.run(["git", "pull", "origin", dev_branch])
 
            # Check if there are differences in commit histories
            commit_diff = subprocess.run(["git", "log", f"{main_branch}..{dev_branch}"], capture_output=True, text=True)
            if commit_diff.stdout.strip():
                # Rebase main branch onto development branch
                print(f"Rebasing {main_branch} onto {dev_branch}...", flush=True)
                rebase_result = subprocess.run(["git", "rebase", "origin/" + dev_branch], capture_output=True, text=True)
                if rebase_result.returncode != 0:
                    print(f"Rebase failed for {repo_name}: {rebase_result.stderr}")
                    handle_rebase_conflicts(repo_name)
                    # Re-enable linear history without force push allowances
                    update_branch_protection(repo_name, github_token, enable_linear_history=True, allow_force_pushes=False)
                    continue
 
            # Push changes to GitHub
            print("Pushing changes", flush=True)
            push_result = subprocess.run(["git", "push", "origin", main_branch], capture_output=True, text=True)
            if push_result.returncode != 0:
                print(f"Push failed for {repo_name}: {push_result.stderr}")
                # Re-enable linear history without force push allowances
                update_branch_protection(repo_name, github_token, enable_linear_history=True, allow_force_pushes=False)
                continue
 
            # Re-enable linear history without force push allowances
            update_branch_protection(repo_name, github_token, enable_linear_history=True, allow_force_pushes=False)
 
            # Navigate back to the initial directory
            os.chdir(current_dir)

def check_merge_conflicts(repo_name):
    # Check for merge conflicts
    print(f"Checking for merge conflicts in repository: {repo_name}...", flush=True)
    result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, text=True)
    print("Merge result:", result.stdout)
    conflict_files = result.stdout.splitlines()
    if conflict_files:
        print("Merge conflict detected. Conflicting files:")
        for file in conflict_files:
            print(file)
    else:
        print("No merge conflicts detected.")
 
def handle_rebase_conflicts(repo_name):
    # Handling rebase conflicts
    print(f"Rebase conflict detected in repository: {repo_name}", flush=True)
    print("Aborting the rebase...", flush=True)
    subprocess.run(["git", "rebase", "--abort"], capture_output=True, text=True)
 
if __name__ == "__main__":
    github_token = sys.argv[1]
    git_email = sys.argv[2]
    git_username = sys.argv[3]
    workspace = sys.argv[4]
    merge_branches(github_token, git_email, git_username, workspace)
