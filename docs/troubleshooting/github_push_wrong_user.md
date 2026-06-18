# Overview
After setting up a new user's GitHub PAT for the BatteryLab repository and using it to push some changes to the remote repository, the past user's profile showed up on the remote repo as the author of the changes. 

## Fix
Git stores local author settings, which may have been set by the past user. These can be changed with:

```bash
git config user.email "new-email@example.com"
git config user.name "GitHub Username"
```

If the error was spotted early (i.e., you push a commit and see the old user's profile), this can be amended using
```bash
git commit --amend --author="Author Name <email@address.com>"
git push -f
```
which will correct the previous commit. Note that this must be done immediately after the commit has been pushed, or it may not work.