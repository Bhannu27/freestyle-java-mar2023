#!/bin/bash
 
# Function to merge development branch into master branch in a repository
merge_repo() {
    local repo="$1"
    echo "Merging development branch into master in $repo"
    
    # Navigate to the repository directory
    cd "$repo" || exit
    
    # Fetch latest changes
    git fetch origin
    
    # Switch to master branch
    git checkout master
    
    # Merge changes from development branch
    git merge origin/development
    
    # Push changes to remote
    git push origin master
    
    echo "Finished merging development branch into master in $repo"
}
 
# Loop through each repository in the list
while IFS= read -r repo; do
    merge_repo "$repo"
done < repositories.txt
