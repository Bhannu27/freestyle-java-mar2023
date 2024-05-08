import os
import subprocess
import requests
import sys
 
def fetch_repository_details(org_name, repo_name, github_token):
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
 
def merge_branches(org_name, github_token):
    main_branch = "main"
    dev_branch = "development"
    repo_file = "calling-workflows/repository.txt"
 
    with open(repo_file, 'r') as file:
        for repo_name in file:
            repo_name = repo_name.strip()
            print(f"Merging {dev_branch} into {main_branch} for repository: {repo_name}")
 
            repo_details = fetch_repository_details(repo_name, github_token)
            print ("Repo details:", repo_details)
            if repo_details is None:
                continue
 
            clone_url = repo_details.get('clone_url')
            if clone_url is None:
                print(f"Clone URL not found for repository: {repo_name}")
                continue
 
            # Navigate to the repository directory
            os.chdir(repo_name)
 
            # Set the remote URL of the repository to the clone URL
            subprocess.run(["git", "remote", "set-url", "origin", clone_url])
 
            # Checkout and pull latest changes from main branch
            subprocess.run(["git", "fetch", "origin", f"{main_branch}:{main_branch}"])
            subprocess.run(["git", "checkout", main_branch])
            subprocess.run(["git", "pull", "origin", main_branch])
 
            # Checkout and pull latest changes from development branch
            subprocess.run(["git", "fetch", "origin", f"{dev_branch}:{dev_branch}"])
            subprocess.run(["git", "checkout", dev_branch])
            subprocess.run(["git", "pull", "origin", dev_branch])
 
            # Merge development branch into main branch
            subprocess.run(["git", "checkout", main_branch])
            subprocess.run(["git", "merge", "--no-ff", dev_branch, "-m", f"Merge {dev_branch} into {main_branch}"])
 
            # Push changes to GitHub
            # subprocess.run(["git", "push", "origin", main_branch])

if __name__ == "__main__":
    org_name = sys.argv[1]
    github_token = sys.argv[2]
    merge_branches(org_name, github_token)
