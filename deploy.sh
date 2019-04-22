#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

SOURCE_BRANCH="master"
TARGET_BRANCH="validation-reports"

function runValidation {
    python ValidationEngine.py
    python -m unittest
}

# This could be useful once the system is in production
# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
# if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
#     echo "Skipping deploy; just doing a build."
#     runValidation
#     exit 0
# fi

# Save some useful information
REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

# Clone the existing gh-pages for this repo into out/
# Create a new empty branch if gh-pages doesn't exist yet (should only happen on first deply)
# Delete all existing contents except .git (we will re-create them)
git clone $REPO reports
cd reports
git checkout $TARGET_BRANCH || git checkout --orphan $TARGET_BRANCH
find -maxdepth 1 ! -name .git ! -name .gitignore ! -name . | xargs rm -rf
cd ..

# Gets backend credentials
rm -rf backendProvider.json
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K $encrypted_db6b38dbc639_key -iv $encrypted_db6b38dbc639_iv -in secrets.tar.enc -out secrets.tar -d
tar xvf secrets.tar


echo "Running validation"
runValidation

# Now let's go have some fun with the cloned repo
cd reports
git config user.name "Travis CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"

# If there are no changes to the compiled out (e.g. this is a README update) then just bail.
if git diff --quiet; then
    echo "No changes to the output on this push; exiting."
    exit 0
fi

# Commit the "changes", i.e. the new version.
# The delta will show diffs between new and old versions.

echo "Commiting to Github Pages"
git add -A .
git commit -m "Deploy to GitHub Pages: ${SHA}"

# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
chmod 600 ../openeo
eval `ssh-agent -s`
ssh-add ../openeo

# Now that we're all set up, we can push.
git push $SSH_REPO $TARGET_BRANCH