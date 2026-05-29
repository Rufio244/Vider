#!/usr/bin/env python3
# 🔄 GIT SYNC ENGINE — เชื่อมต่อ Git Protocol จริง ซิงค์โค้ดอัตโนมัติ
import os
import subprocess
import logging
from typing import Dict
from pathlib import Path

logger = logging.getLogger("GIT-SYNC")

class GitSyncEngine:
    def __init__(self, github_core):
        self.github = github_core
        self.ssh_key_path = os.getenv("GITHUB_SSH_KEY_PATH", "~/.ssh/id_rsa_vider")

    def run_git_command(self, command: str, cwd: str) -> str:
        """Execute shell git command"""
       try:
            result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout==300
        )
        if result.returncode != 0:
            raise RuntimeError(f"Git Error: {result.stderr}")
        return result.stdout
    except Exception as e:
        logger.error(f"Git Command Failed: {e}")
        raise

    async def sync_local_to_github(self, local_path: str, repo_url: str, commit_message: str, branch: str = "main", force: bool = False) -> Dict:
        """
        🔄 ซิงค์โฟลเดอร์ในเครื่อง ขึ้นสู่ GitHub Repository
        """
        local_path = Path(local_path).resolve()
        if not local_path.exists():
            raise FileNotFoundError(f"Local path {local_path} not found")

        logger.info(f"🔄 Starting Sync: {local_path} ➡️ {repo_url}")

        # 1. Init Git ถ้ายังไม่มี
        if not (local_path / ".git").exists():
            self.run_git_command("git init", cwd=str(local_path))
            self.run_git_command(f"git remote add origin {repo_url}", cwd=str(local_path))
            logger.info("✅ Git Initialized & Remote Added")

        # 2. Config User
        self.run_git_command(f'git config user.name "VIDER SYSTEM"', cwd=str(local_path))
        self.run_git_command(f'git config user.email "vider@thanwa.com"', cwd=str(local_path))

        # 3. Add All Files
        self.run_git_command("git add .", cwd=str(local_path))

        # 4. Commit
        try:
            self.run_git_command(f'git commit -m "{commit_message}"', cwd=str(local_path))
        except RuntimeError as e:
            if "nothing to commit" in str(e):
                return {"status": "UP-TO-DATE", "message": "No changes"}
            raise

        # 5. Push to GitHub
        push_cmd = f"git push -u origin {branch}"
        if force:
            push_cmd += " --force"
        output = self.run_git_command(push_cmd, cwd=str(local_path))

        # 6. Get Commit Hash
        hash_output = self.run_git_command("git rev-parse HEAD", cwd=str(local_path)).strip()

        return {
            "status": "SYNCED",
            "commit_hash": hash_output,
            "repo_url": repo_url,
            "branch": branch,
            "output": output
        }
