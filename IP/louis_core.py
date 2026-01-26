import os
import stat
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

class LouisConfig:
    def __init__(self, root_path=None):
        self.config_dir = Path.home() / ".louis-control"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "louis-config.json"
        self.protected_list = self.config_dir / "protected-files.txt"
        self.log_file = self.config_dir / "lock-history.log"
        
        # Load Config
        self.project_root = Path(root_path) if root_path else Path.cwd()
        self.protected_folders = []
        self.ignore_patterns = ["node_modules", ".git", "__pycache__", "dist"]

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.protected_folders = data.get("protected_folders", [])
                    # Only override root if explicitly saved in global config, 
                    # otherwise default to CWD for portability
                    if "project_root" in data:
                        self.project_root = Path(data["project_root"])
            except: pass

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump({
                "project_root": str(self.project_root),
                "protected_folders": self.protected_folders
            }, f, indent=2)

    def log(self, action: str):
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {action}\n")

class LouisWarden:
    def __init__(self, config: LouisConfig):
        self.config = config

    def scan_and_protect(self) -> int:
        """Refreshes the protected-files.txt based on folders."""
        protected_files = []
        for folder in self.config.protected_folders:
            folder_path = self.config.project_root / folder
            if not folder_path.exists(): continue
            
            for file in folder_path.rglob('*'):
                if file.is_file() and not any(ign in str(file) for ign in self.config.ignore_patterns):
                    protected_files.append(str(file.relative_to(self.config.project_root)))
        
        with open(self.config.protected_list, 'w') as f:
            f.write("\n".join(protected_files))
        return len(protected_files)

    def is_locked(self, rel_path: str) -> bool:
        full = self.config.project_root / rel_path
        return full.exists() and not (os.stat(full).st_mode & stat.S_IWUSR)

    def lock_file(self, rel_path: str) -> Tuple[bool, str]:
        full = self.config.project_root / rel_path
        if not full.exists(): return False, "Not Found"
        try:
            os.chmod(full, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH) # 444
            self.config.log(f"LOCKED: {rel_path}")
            return True, "Locked"
        except Exception as e: return False, str(e)

    def unlock_file(self, rel_path: str) -> Tuple[bool, str]:
        full = self.config.project_root / rel_path
        if not full.exists(): return False, "Not Found"
        try:
            os.chmod(full, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH) # 644
            self.config.log(f"UNLOCKED: {rel_path}")
            return True, "Unlocked"
        except Exception as e: return False, str(e)

    def install_git_hook(self) -> Tuple[bool, str]:
        """Restored from v1.0: Installs the pre-commit hook."""
        hook_path = self.config.project_root / ".git" / "hooks" / "pre-commit"
        if not hook_path.parent.exists(): return False, ".git not found"
        
        script = f"""#!/bin/bash
# Louis Warden Hook
PROTECTED="{self.config.protected_list}"
if [ -f "$PROTECTED" ]; then
    STAGED=$(git diff --cached --name-only)
    if echo "$STAGED" | grep -qxF -f "$PROTECTED"; then
        echo "⛔ LOUIS SAYS: You are trying to commit a protected file!"
        echo "Please unlock it via Orchestr8 first."
        exit 1
    fi
fi
"""
        try:
            with open(hook_path, 'w') as f: f.write(script)
            os.chmod(hook_path, 0o755)
            return True, "Git Hook Installed"
        except Exception as e: return False, str(e)
