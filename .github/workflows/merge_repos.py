# merge_repos.py

import os
import subprocess

def merge_repositories(repo_file):
    try:
        with open(repo_file, 'r') as f:
            repo_names = f.read().splitlines()

        for repo_name in repo_names:
            print(f"Merging {repo_name}...")
            # Replace with your actual commands for merging
            subprocess.run(["git", "clone", f"https://github.com/your-username/{repo_name}.git"])
            subprocess.run(["git", "checkout", "main"])
            subprocess.run(["git", "pull", "origin", "main"])
            subprocess.run(["git", "merge", "development"])
            subprocess.run(["git", "push", "origin", "main"])
            print(f"{repo_name} merged successfully!")

    except FileNotFoundError:
        print("Error: repository.txt file not found.")

if __name__ == "__main__":
    repo_file_path = "repository.txt"
    merge_repositories(repo_file_path)
