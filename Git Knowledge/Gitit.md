# Gitit - Complete GitHub Repository Guide

> **Orchestr8 v3.0 "The Fortress Factory"**  
> Repository: https://github.com/bozertron/Orchestr8_jr  
> Owner: bozertron

---

## Table of Contents

1. [Repository Structure](#1-repository-structure)
2. [Branching Strategy](#2-branching-strategy)
3. [Commit Message Standards](#3-commit-message-standards)
4. [GitHub CLI Setup](#4-github-cli-setup)
5. [Authentication Token Scopes](#5-authentication-token-scopes)
6. [Commit Workflow](#6-commit-workflow)
7. [Code Quality Best Practices](#7-code-quality-best-practices)
8. [Troubleshooting](#8-troubleshooting)
9. [Security Considerations](#9-security-considerations)
10. [Project Integration](#10-project-integration)

---

## 1. Repository Structure

### Overview

```
Orchestr8_jr/
├── IP/                          # Core Python modules (IP Protocol)
│   ├── orchestr8_app.py         # Main Marimo application
│   ├── carl_core.py             # TypeScript bridge
│   ├── connie.py                # DB conversion engine
│   ├── louis_core.py            # File protection system
│   └── plugins/                 # Dynamic Marimo UI plugins
│       ├── 00_welcome.py
│       ├── 01_generator.py
│       ├── 02_explorer.py
│       ├── 03_gatekeeper.py
│       ├── 04_connie_ui.py
│       └── 05_cli_bridge.py
│
├── frontend/
│   └── tools/                   # TypeScript CLI tools
│       ├── scaffold-cli.ts      # Main CLI (Commander.js)
│       ├── unified-context-system.ts
│       └── parsers/             # Plugin parsers
│
├── .taskmaster/                 # Task automation system
│   └── tasks/tasks.json         # Task definitions
│
├── .louis-control/              # Louis file protection config
│   └── louis-config.json
│
├── Agent Deployment Strategy/   # Future agent definitions
├── PRDs/                        # Product requirement documents
├── Staging/                     # Work-in-progress files
├── Git Knowledge/               # This documentation
│
├── orchestr8.py                 # v1.0 MVP (preserved)
├── CLAUDE.md                    # AI assistant guidance
├── .gitignore                   # Git ignore rules
└── package.json                 # (if present) Node config
```

### Key Directories

| Directory | Purpose | Protected |
|-----------|---------|-----------|
| `IP/` | Core Python implementation | Yes (Louis) |
| `IP/plugins/` | Dynamic UI plugins | Yes |
| `frontend/tools/` | TypeScript CLI | No |
| `.taskmaster/` | Task automation | No |
| `.louis-control/` | Protection config | Yes |

---

## 2. Branching Strategy

### Branch Types

| Branch Type | Naming Convention | Purpose | Example |
|-------------|-------------------|---------|---------|
| **Main** | `master` or `main` | Production-ready code | `master` |
| **Feature** | `feature/<name>` | New features | `feature/agent-deployment` |
| **Bugfix** | `fix/<issue>` | Bug fixes | `fix/cli-parser-error` |
| **Hotfix** | `hotfix/<name>` | Critical production fixes | `hotfix/auth-bypass` |
| **Release** | `release/v<version>` | Release preparation | `release/v3.1` |
| **Experiment** | `exp/<name>` | Experimental features | `exp/new-ui-framework` |

### Branch Workflow

```
master
  │
  ├── feature/new-parser ──────┐
  │                            │ (PR + Review)
  ├────────────────────────────┘
  │
  ├── fix/cli-timeout ─────────┐
  │                            │ (PR + Review)
  ├────────────────────────────┘
  │
  └── release/v3.1 ────────────> TAG: v3.1.0
```

### Creating a Branch

```bash
# Create and switch to a new branch
git checkout -b feature/my-feature

# Push branch to remote
git push -u origin feature/my-feature

# List all branches
git branch -a
```

---

## 3. Commit Message Standards

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(plugins): add CLI bridge plugin` |
| `fix` | Bug fix | `fix(carl): resolve timeout on large scans` |
| `docs` | Documentation | `docs(readme): update installation steps` |
| `style` | Formatting (no code change) | `style(cli): fix indentation` |
| `refactor` | Code restructure | `refactor(connie): extract export methods` |
| `test` | Adding tests | `test(parser): add overview unit tests` |
| `chore` | Maintenance | `chore(deps): update commander to v14` |
| `perf` | Performance | `perf(scan): cache file metadata` |

### Scope (Optional)

Use the component being modified:
- `plugins` - Python plugins
- `cli` - TypeScript CLI
- `carl` - CarlContextualizer
- `connie` - Conversion engine
- `louis` - File protection
- `tasks` - Taskmaster system
- `deps` - Dependencies

### Subject Rules

- Use imperative mood: "add" not "added" or "adds"
- No period at the end
- Max 50 characters
- Capitalize first letter

### Body Rules

- Wrap at 72 characters
- Explain **what** and **why**, not **how**
- Separate from subject with blank line

### Examples

```bash
# Simple commit
git commit -m "feat(plugins): add welcome tab with getting started guide"

# Commit with body
git commit -m "fix(cli): resolve commander version compatibility

The original commander@11.5.0 does not exist on npm.
Updated to commander@14.0.2 which is the latest stable version.

Closes #42"

# Breaking change
git commit -m "feat(api)!: change plugin interface signature

BREAKING CHANGE: render() now requires STATE_MANAGERS parameter"
```

---

## 4. GitHub CLI Setup

### Installation

**Linux (Debian/Ubuntu):**
```bash
# Add GitHub CLI repository
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install
sudo apt update
sudo apt install gh
```

**macOS:**
```bash
brew install gh
```

**Windows:**
```powershell
winget install --id GitHub.cli
```

### Authentication

```bash
# Interactive login (recommended)
gh auth login

# Follow prompts:
# 1. Select "GitHub.com"
# 2. Select "HTTPS"
# 3. Select "Login with a web browser"
# 4. Copy the one-time code
# 5. Press Enter to open browser
# 6. Paste code and authorize
```

### Verify Authentication

```bash
# Check auth status
gh auth status

# Expected output:
# ✓ Logged in to github.com as bozertron
# ✓ Git operations for github.com configured to use https protocol
# ✓ Token: gho_****
# ✓ Token scopes: delete_repo, gist, read:org, repo, workflow
```

### Configure Git to Use GitHub CLI

```bash
# Set gh as credential helper
gh auth setup-git

# Verify remote URL
git remote -v
# origin  https://github.com/bozertron/Orchestr8_jr.git (fetch)
# origin  https://github.com/bozertron/Orchestr8_jr.git (push)
```

---

## 5. Authentication Token Scopes

### Required Scopes for Full Access

| Scope | Purpose | Required |
|-------|---------|----------|
| `repo` | Full repository access | **Yes** |
| `workflow` | Update GitHub Actions workflows | Yes |
| `read:org` | Read org membership | Yes |
| `gist` | Create gists | Optional |
| `delete_repo` | Delete repositories | Optional |

### Checking Current Scopes

```bash
gh auth status
```

### Refreshing Scopes

```bash
# Add missing scopes
gh auth refresh -s repo,workflow,read:org

# Re-authenticate with all scopes
gh auth login --scopes "repo,workflow,read:org,gist"
```

### Personal Access Token (Alternative)

If not using `gh auth login`:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`, `read:org`
4. Copy the token
5. Configure git:

```bash
git config --global credential.helper store
# Then run any git command and enter the token as password
```

---

## 6. Commit Workflow

### Step-by-Step Process

#### 1. Check Current Status

```bash
# View modified files
git status

# View specific changes
git diff

# View staged changes
git diff --staged
```

#### 2. Stage Changes

```bash
# Stage specific files
git add IP/plugins/00_welcome.py
git add frontend/tools/scaffold-cli.ts

# Stage all changes in a directory
git add IP/plugins/

# Stage all tracked modified files
git add -u

# Stage everything (use with caution)
git add .

# Interactive staging
git add -p
```

#### 3. Review Staged Changes

```bash
# See what's staged
git status

# See staged diff
git diff --staged

# Unstage a file if needed
git restore --staged <file>
```

#### 4. Commit

```bash
# Simple commit
git commit -m "feat(plugins): add generator wizard"

# Commit with extended message
git commit

# This opens your editor for multi-line message
```

#### 5. Push to Remote

```bash
# Push to current branch
git push

# Push to specific branch
git push origin master

# Push and set upstream
git push -u origin feature/my-branch
```

### Complete Example Session

```bash
# 1. Start with clean state
git status

# 2. Make your code changes
# ... edit files ...

# 3. Review changes
git diff IP/plugins/01_generator.py

# 4. Stage specific files
git add IP/plugins/01_generator.py
git add IP/plugins/02_explorer.py

# 5. Verify staging
git status

# 6. Commit with proper message
git commit -m "feat(plugins): implement generator and explorer tabs

- Generator: 7-phase project wizard with BUILD_SPEC export
- Explorer: file table with Carl deep scan integration

Part of Tasks 10 implementation"

# 7. Push to remote
git push
```

---

## 7. Code Quality Best Practices

### Pre-Commit Checklist

- [ ] Code compiles/runs without errors
- [ ] All tests pass (if applicable)
- [ ] No debugging code left (print statements, console.log)
- [ ] No hardcoded credentials or secrets
- [ ] File paths are relative, not absolute
- [ ] Imports are organized and minimal
- [ ] No commented-out code blocks
- [ ] Docstrings/comments are accurate

### Python-Specific

```bash
# Check syntax
python -m py_compile IP/plugins/01_generator.py

# Run all Python file checks
for f in IP/*.py IP/plugins/*.py; do python -m py_compile "$f" && echo "✓ $f"; done
```

### TypeScript-Specific

```bash
# Type check
cd frontend/tools
npx tsc --noEmit

# Run specific file
npx tsx scaffold-cli.ts --help
```

### Recommended Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check Python syntax
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$'); do
    python -m py_compile "$file"
    if [ $? -ne 0 ]; then
        echo "Python syntax error in $file"
        exit 1
    fi
done

# Check TypeScript
if git diff --cached --name-only | grep -q '\.ts$'; then
    cd frontend/tools
    npx tsc --noEmit
    if [ $? -ne 0 ]; then
        echo "TypeScript error"
        exit 1
    fi
fi

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 8. Troubleshooting

### Authentication Issues

#### "Authentication failed"

```bash
# Re-authenticate
gh auth logout
gh auth login

# Verify
gh auth status
```

#### "Permission denied (publickey)"

```bash
# Check if using HTTPS (not SSH)
git remote -v

# Should show https:// URLs, not git@github.com:
# If SSH, convert to HTTPS:
git remote set-url origin https://github.com/bozertron/Orchestr8_jr.git
```

#### "Token expired or revoked"

```bash
# Refresh token
gh auth refresh

# Or re-login
gh auth login
```

### Push Issues

#### "rejected - non-fast-forward"

```bash
# Pull first, then push
git pull --rebase origin master
git push

# If conflicts, resolve them first
git status  # Shows conflicted files
# Edit files to resolve
git add <resolved-files>
git rebase --continue
git push
```

#### "remote: Permission to ... denied"

```bash
# Check remote URL
git remote -v

# Verify you have write access
gh repo view bozertron/Orchestr8_jr

# Re-authenticate with proper scopes
gh auth refresh -s repo
```

### Common Git Errors

#### "Changes not staged for commit"

```bash
# You need to stage before committing
git add <files>
git commit -m "message"
```

#### "Your branch is behind"

```bash
# Update local branch
git pull

# Or if you want to preserve local commits on top
git pull --rebase
```

#### "Merge conflict"

```bash
# See conflicting files
git status

# Edit files to resolve (look for <<<<<<< markers)
# Then mark as resolved
git add <file>

# Complete the merge
git commit
```

---

## 9. Security Considerations

### Credential Management

**DO:**
- Use `gh auth login` for authentication
- Use credential helpers instead of plaintext tokens
- Rotate tokens periodically
- Use minimal required scopes

**DON'T:**
- Commit tokens or credentials to the repository
- Store tokens in plaintext files
- Share tokens or authentication sessions
- Use tokens with excessive permissions

### Sensitive Files

Already in `.gitignore`:
```
# Credentials
*.pem
*.key
.env
.env.local
*.secret

# IDE
.vscode/settings.json
.idea/

# Build artifacts
node_modules/
__pycache__/
*.pyc
```

### Token Rotation

```bash
# Check token age
gh auth status

# Revoke and regenerate
# Go to: https://github.com/settings/tokens
# Revoke old token
# Run: gh auth login
```

### SSH Key Alternative

If you prefer SSH over HTTPS:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
gh ssh-key add ~/.ssh/id_ed25519.pub --title "My Machine"

# Convert remote to SSH
git remote set-url origin git@github.com:bozertron/Orchestr8_jr.git
```

---

## 10. Project Integration

### Taskmaster Integration

The project uses a task automation system at `.taskmaster/tasks/tasks.json`.

**View current tasks:**
```bash
cat .taskmaster/tasks/tasks.json | jq '.tasks[] | {id, title, status}'
```

**Commit with task reference:**
```bash
git commit -m "feat(plugins): implement CLI bridge

Implements Task 12 - CLI Bridge plugin with subprocess execution
and dynamic plugin discovery.

Task-ID: 12"
```

### Louis File Protection

Before modifying protected files, check Louis status:

```bash
cat .louis-control/louis-config.json
```

Protected paths require explicit unlock before modification.

### Marimo Development Workflow

```bash
# Start development server
marimo edit IP/orchestr8_app.py

# Make changes in browser
# Save (Cmd+S / Ctrl+S)
# Changes auto-save to file

# Commit
git add IP/orchestr8_app.py
git commit -m "feat(app): update main layout"
git push
```

### TypeScript CLI Development

```bash
# Navigate to tools
cd frontend/tools

# Install dependencies (if needed)
npm install

# Run CLI
npx tsx scaffold-cli.ts list-plugins

# Test changes
npx tsx scaffold-cli.ts overview --target ../..

# Commit
cd ../..
git add frontend/tools/
git commit -m "feat(cli): add new parser option"
git push
```

### Typical Development Session

```bash
# 1. Start fresh
git pull

# 2. Check task status
cat .taskmaster/tasks/tasks.json | jq '.tasks[] | select(.status == "pending")'

# 3. Create feature branch (optional)
git checkout -b feature/my-feature

# 4. Make changes
marimo edit IP/orchestr8_app.py

# 5. Test
python -m py_compile IP/orchestr8_app.py
cd frontend/tools && npx tsx scaffold-cli.ts --help

# 6. Stage and commit
git add .
git commit -m "feat: implement feature X"

# 7. Push
git push -u origin feature/my-feature

# 8. Create PR (if on branch)
gh pr create --title "Feature X" --body "Description..."

# 9. Or merge to master directly
git checkout master
git merge feature/my-feature
git push
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    Git Quick Reference                          │
├─────────────────────────────────────────────────────────────────┤
│ SETUP                                                           │
│   gh auth login              # Authenticate with GitHub         │
│   gh auth status             # Check authentication             │
│   gh auth setup-git          # Configure git credential helper  │
├─────────────────────────────────────────────────────────────────┤
│ DAILY WORKFLOW                                                  │
│   git status                 # Check current state              │
│   git pull                   # Get latest changes               │
│   git add <files>            # Stage changes                    │
│   git commit -m "msg"        # Commit with message              │
│   git push                   # Push to remote                   │
├─────────────────────────────────────────────────────────────────┤
│ BRANCHING                                                       │
│   git checkout -b <branch>   # Create and switch to branch      │
│   git checkout master        # Switch to master                 │
│   git merge <branch>         # Merge branch into current        │
│   git branch -d <branch>     # Delete local branch              │
├─────────────────────────────────────────────────────────────────┤
│ COMMIT MESSAGE FORMAT                                           │
│   <type>(<scope>): <subject>                                    │
│   Types: feat, fix, docs, style, refactor, test, chore          │
├─────────────────────────────────────────────────────────────────┤
│ TROUBLESHOOTING                                                 │
│   gh auth refresh            # Refresh token                    │
│   git pull --rebase          # Update with rebase               │
│   git remote -v              # Check remote URLs                │
│   git config -l              # View configuration               │
└─────────────────────────────────────────────────────────────────┘
```

---

*Last updated: January 2026*  
*Orchestr8 v3.0 "The Fortress Factory"*
