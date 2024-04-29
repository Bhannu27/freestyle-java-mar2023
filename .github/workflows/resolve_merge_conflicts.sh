#!/bin/bash
 
# Checkout the branch where you want to merge changes
git checkout $GITHUB_HEAD_REF
 
# Pull the latest changes from the remote repository
git pull origin $GITHUB_HEAD_REF
 
# Merge changes from the target branch
git merge $GITHUB_BASE_REF
 
# Check for merge conflicts
if git diff --check | grep -q '<<<<<<<'; then
    # If there are merge conflicts, handle them
    echo "Merge conflicts detected. Resolving..."
    
    # You can use a merge tool like 'git mergetool' to resolve conflicts
    # Or you can manually resolve conflicts by editing the files
    
    # Once conflicts are resolved, add the resolved files
    git add .
    
    # Continue with the merge process
    git merge --continue
    
    # If conflicts are not resolved, exit the script
    if [ $? -ne 0 ]; then
        echo "Merge conflicts were not resolved. Exiting..."
        exit 1
    fi
fi
