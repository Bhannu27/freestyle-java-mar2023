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

def enable_branch_protection(repo_name, github_token):
    org_name = "Sanofi-GitHub"
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/branches/main/protection"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    protection_rules = {
        "required_status_checks": None,
        "enforce_admins": False,
        "required_pull_request_reviews": None,
        "restrictions": {
            "users": [],
            "teams": [""]
        },
        "dismiss_stale_reviews": False,
        "require_code_owner_reviews": False,
        "required_approving_review_count": False,
        "require_last_push_approval": False,
        "bypass_pull_request_allowances": False, 
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": False,
        "lock_branch": False
        }
    response = requests.put(url, headers=headers, json=protection_rules)
    if response.status_code == 200:
        print(f"Enabled branch protection rules for {repo_name}.")
    else:
        print(f"Failed to enable branch protection rules for {repo_name}.")
        print(f"Response: {response.text}")
 
#def disable_branch_protection(repo_name, github_token):
 #   org_name = "Sanofi-GitHub"
  #  url = f"https://api.github.com/repos/{org_name}/{repo_name}/branches/main/protection"
   # headers = {
    #    "Authorization": f"Bearer {github_token}",
     #   "Accept": "application/vnd.github.v3+json"
    #}
    #protection_rules = {
   #     "required_status_checks": None,
   #     "enforce_admins": False,
   #     "required_pull_request_reviews": None,
   #     "restrictions": {
   #         "users": [],
   #         "teams": ["chc-admins"]
   #     },
   #     "allow_force_pushes": False,
   #     "required_linear_history": True
 #   }
  #  response = requests.put(url, headers=headers, json=protection_rules)
   # if response.status_code == 200:
    #    print(f"Disabled branch protection rules for {repo_name}.")
    #else:
     #   print(f"Failed to disable branch protection rules for {repo_name}.")
      #  print(f"Response: {response.text}")
 
def merge_branches(github_token, git_email, git_username, workspace):
    main_branch = "main"
    dev_branch = "development"
    repo_file = "calling-workflows/repository.txt"

    current_dir = os.getcwd()
 
    with open(repo_file, 'r') as file:
        for repo_name in file:
            repo_name = repo_name.strip()
            print(f"Merging {dev_branch} into {main_branch} for repository: {repo_name}",flush=True)
 
            repo_details = fetch_repository_details(repo_name, github_token)
            #print ("Repo details:", repo_details)
            if repo_details is None:
                continue
 
            clone_url = repo_details.get('clone_url')
            print ("Clone URL : ",clone_url)
            if clone_url is None:
                print(f"Clone URL not found for repository: {repo_name}",flush=True)
                continue
 
            # Navigate to the repository directory
            repo_path = os.path.join(workspace, repo_name)
            os.makedirs(repo_path, exist_ok=True)
            os.chdir(repo_path)
 
            # Set the remote URL of the repository to the clone URL
            print(f"setting remote URL to: {clone_url}",flush=True)
            subprocess.run(["git", "remote", "set-url", "origin", clone_url])

            # set the Git user email and username
            subprocess.run(["git", "config", "--global", "user.email", git_email])
            subprocess.run(["git", "config", "--global", "user.name", git_username])

            enable_branch_protection(repo_name, github_token)
 
            # Checkout and pull latest changes from main branch
            print("Fetching the latest changes from main branch..",flush=True)
            subprocess.run(["git", "fetch", "origin", f"{main_branch}:{main_branch}"])
            subprocess.run(["git", "checkout", main_branch])
            subprocess.run(["git", "pull", "origin", main_branch])
 
            # Checkout and pull latest changes from development branch
            print("Fetching the latest changes from development branch..",flush=True)
            subprocess.run(["git", "fetch", "origin", f"{dev_branch}:{dev_branch}"])
            subprocess.run(["git", "checkout", dev_branch])
            subprocess.run(["git", "pull", "origin", dev_branch])
 
            # Merge development branch into main branch
            print(f"Merging {dev_branch} into {main_branch}..",flush=True)
            subprocess.run(["git", "checkout", main_branch])
            subprocess.run(["git", "merge", "--no-ff", "--allow-unrelated-histories", "--no-verify", dev_branch, "-m", f"Merge {dev_branch} into {main_branch}"])
 
            # Push changes to GitHub
            print("Pushing changes", flush=True)
            subprocess.run(["git", "push", "origin", main_branch])

         #   disable_branch_protection(repo_name, github_token)
            
            #navigate back to the initial directory
            os.chdir(current_dir)

def check_merge_conflicts(repo_name):
    # Check for merge conflicts
    print("Checking for merge conflicts in repository: {repo_name}...", flush=True)
    result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, text=True)
    Print("Merge result", result.stdout)
    conflict_files = result.stdout.splitlines()
    if conflict_files:
        print("Merge conflict detected. Conflicting files:")
        for file in conflicting_files:
            print(file)
    else:
        print("No merge conflicts detected.")
         
if __name__ == "__main__":
    github_token = sys.argv[1]
    git_email = sys.argv[2]
    git_username = sys.argv[3]
    workspace = sys.argv[4]
    merge_branches(github_token, git_email, git_username, workspace)
