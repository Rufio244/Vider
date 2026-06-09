import os
import subprocess
import requests
import json
from datetime import datetime
from typing import Dict, Optional

class VIDERGitHubConnector:
    def __init__(self, repo_owner: str = "Rufio244", repo_name: str = "Vider"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.local_path = "./vider_system"
        self.config_file = "./github_config.json"
        self.github_token = ""
        self.last_sync = None
        self._load_config()

    def _load_config(self):
        """โหลดการตั้งค่า"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.github_token = data.get("github_token", "")
                    self.last_sync = data.get("last_sync")
            except:
                pass

    def _save_config(self):
        """บันทึกการตั้งค่า"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump({
                "github_token": self.github_token,
                "last_sync": datetime.now().isoformat(),
                "repo": f"{self.repo_owner}/{self.repo_name}"
            }, f, indent=2)

    def set_token(self, token: str) -> Dict:
        """ตั้งค่าโทเค็น GitHub"""
        self.github_token = token.strip()
        self._save_config()
        return {"success": True, "message": "บันทึกโทเค็นเรียบร้อยแล้ว"}

    def clone_or_pull(self) -> Dict:
        """ดึงโค้ดครั้งแรก หรืออัปเดตเมื่อมีใหม่"""
        try:
            if not os.path.exists(self.local_path):
                auth = f"https://{self.github_token}@github.com" if self.github_token else "https://github.com"
                full_url = self.repo_url.replace("https://github.com", auth)
                res = subprocess.run(["git", "clone", full_url, self.local_path],
                                     capture_output=True, text=True)
                if res.returncode != 0:
                    return {"success": False, "error": res.stderr[:300]}
            else:
                os.chdir(self.local_path)
                subprocess.run(["git", "reset", "--hard"], capture_output=True)
                subprocess.run(["git", "pull", "origin", "main"], capture_output=True)
                os.chdir("..")

            self._save_config()
            return {"success": True, "message": "ดึงโค้ดเรียบร้อย", "path": os.path.abspath(self.local_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def push_changes(self, message: str = "อัปเดตระบบ") -> Dict:
        """ส่งโค้ดขึ้น GitHub"""
        if not self.github_token:
            return {"success": False, "message": "ต้องตั้งค่าโทเค็นก่อน"}
        try:
            os.chdir(self.local_path)
            subprocess.run(["git", "add", "."], capture_output=True)
            subprocess.run(["git", "commit", "-m", message], capture_output=True)
            auth_url = self.repo_url.replace("https://", f"https://{self.github_token}@")
            subprocess.run(["git", "remote", "set-url", "origin", auth_url], capture_output=True)
            res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
            os.chdir("..")
            if res.returncode == 0:
                self._save_config()
                return {"success": True, "message": "ส่งขึ้น GitHub เรียบร้อย"}
            return {"success": False, "error": res.stderr[:300]}
        except Exception as e:
            os.chdir("..") if os.getcwd() != ".." else None
            return {"success": False, "error": str(e)}

vider_github = VIDERGitHubConnector()
