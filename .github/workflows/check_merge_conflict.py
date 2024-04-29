import gitpython
from github import Github
 
def check_merge_conflict(pull_request_number, base_branch, head_branch, github_token):
 
  # Create a GitHub object using your personal access token
  github = Github(github_token)
 
  # Get the repository object
  repo = github.get_repo(base_branch.split("/")[0] + "/" + base_branch.split("/")[1])
 
  # Try getting the PullRequest object (might raise an error if PR doesn't exist)
  try:
    pull_request = repo.get_pull(pull_request_number)
  except Exception as e:
    print(f"Error fetching Pull Request: {e}")
    return False  # Assume conflict for any errors
 
  # Check if the pull request is mergeable
  return pull_request.mergeable
 
# Example usage (assuming you have logic to send email using send_email.py)
if __name__ == "__main__":
# your logic to retrieve pull_request_number, base_branch, head_branch, and github_token
  if check_merge_conflict(pull_request_number, base_branch, head_branch, github_token):
    print("No merge conflicts detected.")
  else:
    print("Merge conflicts detected.")
    # Call your send_email function here to send notification
