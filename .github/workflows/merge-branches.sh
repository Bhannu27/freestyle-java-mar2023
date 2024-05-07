#!/bin/bash
 
# Function to merge development branch into main branch in a repository
merge_repo() {
  local repo="$1"
  echo "Merging development branch into main in $repo"
 
  # Navigate to the repository directory
  cd "$repo" || exit
 
  # Fetch latest changes
  git fetch origin
 
  # Switch to main branch
  git checkout main
 
  # Merge with conflict handling
  merge_result=$(git merge origin/development 2>&1)
 
  # Check for merge conflicts
  if grep -q "conflict" <<< "$merge_result"; then
    echo "Merge conflicts detected in $repo! Please resolve manually."
    # Optionally, exit script with an error code (uncomment the following line)
    # exit 1
  else
    echo "Merge successful in $repo"
    # Push changes to remote (optional)
    git push origin main
  fi
}
 
# Get repository names from a file (replace 'repository.txt' with your actual file name)
repos=$(cat repository.txt)
 
# Loop through each repository
for repo in $repos; do
  merge_repo "$repo"
done
