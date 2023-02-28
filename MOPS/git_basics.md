- git init 
	- initialize a new git repo 
- git add files
	- adds files to the staging area 
- git status 
	- used to check the state of the staging area 

```$ git checkout --patch branch2 file.py```
Pulls file from another branch and merges to another 

```git add --no-all```
Adds only new and modified files to the index 
```git branch -D boson```
deletes a branch called boson 
```git init```
crreates new empty repo 
```git clone```
local copy of the git repo 
```git branch```
create new development workspace for existing repo 
```git merge```
incorporates changes between two branches
```git branch -f boson```
reset an existing branch but not automatically switch to the branch
```git checkout -b boson```
create a new branch and switch to that branch 
```git checkout -B boson```
reset an *existing* branch and *switch* to the branch
```git diff```
can be used to troubleshoot commit issues and compare code between commits 
```git diff --cached```
compare *staged* changes between the last commit and the index 
```git diff HEAD```
compares changes in the working directory and the last commit 
```git diff --no-index```
compare two paths in the file syste, where at least one path is untracked by Git. 
```git add -u```
Adds only deleted and modified files to the index 
```git add -A```
Add New , Deleted , and modified files to the index same as ```git add --all```
```git commit -a```
All modified and deleted files 

```git rm --cached Underlay/*..yml```
Remove file from git but keep  local 

git add 
git commit 

#### **Git Stash and get old files**
git stash list 
git stash show -p stash@{1}
git checkout stash@{3} -- local.env
git diff stash@{0}^! -- filename
git show stash@{3}:local.env'
git rm --cached Underlay/*..yml

#### **Push New Branch to Remote**
- git branch -a
	- Confirms branch is created

-  git push -set-upstream gitlab dev-dcjobs


#### **Update the remote url from SSH to HTTPS**
git remote set-url
git remote set-url gitlab https://gitlab.webair.com/ldevictoria/dc_fabric.git

git config http.postBuffer 524288000

devicto@ldevictoria-gsc-mac opti9_obsidian % more .git/config 

```
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
[remote "origin"]
        url = https://github.com/purplecomputer/opti9_obsidian.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
        remote = origin
        merge = refs/heads/main
[remote "github"]
        url = https://github.com/purplecomputer/opti9_obsidian.git
        fetch = +refs/heads/*:refs/remotes/github/*
```

Updating / Undoing Things
```
git commit --amend 
	-Fix the last commit 
	-Updates last commit using staging area 
		git commit -m "my first update"
		git add newfile.txt
		git commit --amend 
		THe last commit takes the place of the previous commit (updates instead of adding another in the chain)

```

Initial User Configuration
```commandline
git config
	username
			git config --global user.name "Louis DeVictoria"
	email 
			git config --global user.email "loud@loudnetworking.org"
	Notes 
		--global persists options for all repos of the user
		Check the config
			git config --list
			git config <property> 
	When using a single dash <-> this is an abbrevation 
	When using a double dash <--> this is the full name 
	git config --global core.editor "vim"
	git config --global core.editor "path_to_program"
```

Git and File Directory Layout
- Working Directory Git Snapshot tree.sh -".git"


Getting Help / Autocomplete
```commandline
git list --s<tab> 
git <command> -h 
git help <command> 
	brings up HTML page 
```

Git Configuration Files
```commandline
System Configuration File git config --system /etc/gitconfig Global Configuration Files git config --global ~/.gitconfig Local Configuration Files git config or git config --local <repo-dir>/.git/config
```

Git Status
```commandline
git status 
?? - untracked 
M - Modified 
A - Added 
D - Deleted 
R - Renamed 
C - Copied 
U - Updated / Unmerged 
-b option - always show branch and tracking info** 
```
Git Reference
```commandline
HEAD Snapshot of the last commit Next Parent (in chain of commits) Pointer to the current branch reference Think of HEAD as pointer to last commit on current branch Index (Staging Area) Place where changes for the next commit get registed Proposed next commit Cache = Index

Show Differences
git diff 
git diff head 
git diff --staged
git diff <reference> <refernce>
```

Support Files
```commandline
.gitignore 
	instruction what to save and what to ignore in the project 
	you can use file patterns 
git rm 
	removes from working directory 
	stages removal 
git rm -f forced the removal 
Rolling back
Reset 
	- rollback so branch points at a previous commit 
	- can roll back working directory to that commit 
	- hard overwrites all 
Revert 
	- allows a "undo" by adding a new change that cancels out the effects of the previous one 
git reset --hard 87ba8bc The goal is to avoid reset hard ![[Pasted image 20210916105308.png]]

git reset current~1[--mixed] this points back one before moves the pointer in the repository ![[Pasted image 20210916105604.png]]

git revert HEAD

```
Git Stash
```commandline
Keep a backup queue of your work 
git stash [push]
saves off state 
use git stash pop or git stash apply to get old state back
```

This covers only work NOT commited into the local repository 
Branch in Source Control
```commandline
Line of Development Collection of specific versions of a group of files tagged in a common way cvs rtage -a-D<date/time> -r Derives_from -b New_Branch Paths_to_Branch End result is easy handle to get all files in the repository with the identifier - the branch name

SnapShot Line of development associated with a specific change collection of specific versions of a group of files associated with a specific commit

Lightweight Branching A lightweight movable pointer in git every commit can be a branch -Unique Identifier in a set of content in time Create a new reference or tag reference You can create new branch do testing , then merge it back in if you want

Creating & Using a new Branch Git pointer called HEAD always points to current branch

git branch <branch> Creates new branch , creates a new pointer git branch testing Change Branch git checkout <branch> Moved HEAD to point to branch Updates working directory contents with lat commit from branch if existing branch reverts files in working directory to snapshot pointed to by branch Updates indicators git checkout testing Branch pointers advance with new commits git checkout  master

What Branch am I in git branch

Topic & Feature Branches
Topic Branches Term for temp branch to try something maintainer of a project may namespace git branch abc/web_client git checkout -b web_client Feature Branches Terms for a branch to develop a feature Intended for limited lifetime Merge back into main line of development

```


Merging Branches
git merge <branch>
Relative to the current branch Current branch is branch being merged into branch is branch merged from Ensure everything is commit first

Merging: What is a Fast Forward
```commandline
You want to merge hotfix into master , so mater will have the hotfix in for future development ![[Pasted image 20210916121234.png]]

git checkout master
git merge hotfix 


Now the hotfix was pulled into the master branch and the pointer has been moved to the same one.

Fast Forward because commit pointed to by branch merged was directly upstream of the current commit , git moves the pointer forward

```
Merging : 3 Way Merge
```commandline
git branch <branch> Creates new branch , creates a new pointer git branch testing Change Branch git checkout <branch> Moved HEAD to point to branch Updates working directory contents with lat commit from branch if existing branch reverts files in working directory to snapshot pointed to by branch Updates indicators git checkout testing Branch pointers advance with new commits git checkout  master

What Branch am I in git branch

Topic & Feature Branches
Topic Branches Term for temp branch to try something maintainer of a project may namespace git branch abc/web_client git checkout -b web_client Feature Branches Terms for a branch to develop a feature Intended for limited lifetime Merge back into main line of development

```

Merge Conflicts
```commandline
git status 
Will show un-merged or both modified Adds <<<<< and >>>> markers in the file When in conflict you are stuck in merge git merge --abort You have to resolve the conflict manually after resolution git add and git commit You can also run git mergetool for graphical help

```
Rebase
Rebase is merging with history 
```commandline
indivudual commits from one branch into another 
Takes all of the changes that were committed on one brancg and merge them in a time sequence into another -Goes to common ancestor of the two branches -Gets the diff introductrewd by each commit , saves to temp files -Applies each change in turn -Moved the branch to the new rebase point git checkout feature git rebase master

Cloning a remote repo to get a local repo git clone git clone URL Clone vs Checkout

Git Remote References "remotes" An actual remote repo A reference t such a repo For local use GIT provides references /alias nicknames that map to remote repo location default is "origin" origin = https://github.com/path

Git Remote Repos
-Remote Server Repos of projects -Push / Pull from -SSH/ Git / HTTPS to pull data git remote show Add Remote git remote add [shortname(handle)][url] Rename shortname git remote rename <old><new> Retrieve latest from git remote git fetch


```
