#!/usr/bin/env python3
# 🐙 GITHUB CORE ENGINE — ระบบเชื่อมต่อหลักกับ GitHub
import requests
import json
import base64
from typing import List, Dict, Optional

class GitHubCore:
    def __init__(self, token: str, username: str, org_name: str = None):
        self.API_URL = "https://api.github.com"
        self.token = token
        self.username = username
        self.org_name = org_name
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PROJECT-VIDER-GITHUB-AGENT"
        }

    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """ส่งคำขอไปยัง GitHub API"""
        url = f"{self.API_URL}{endpoint}"
        resp = requests.request(method, url, headers=self.headers, json=data, timeout=30)
        if resp.status_code >= 400:
            raise ConnectionError(f"GitHub API Error: {resp.status_code} - {resp.text}")
        return resp.json() if resp.text else {}

    # ================ 📦 จัดการ Repository ================
    def create_repository(self, name: str, description: str, private: bool = True, 
                          auto_init: bool = True, gitignore_template: str = None, 
                          license_template: str = None) -> Dict:
        """สร้าง Repository ใหม่ (ถ้ามี Org จะสร้างใน Org, ไม่มีสร้างที่ User)"""
        endpoint = f"/orgs/{self.org_name}/repos" if self.org_name else "/user/repos"
        
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
            "gitignore_template": gitignore_template,
            "license_template": license_template,
            "has_issues": False,
            "has_projects": False,
            "has_wiki": False
        }
        return self._request("POST", endpoint, payload)

    def get_repo(self, repo_name: str) -> Dict:
        """ดึงข้อมูล Repo"""
        owner = self.org_name or self.username
        return self._request("GET", f"/repos/{owner}/{repo_name}")

    def delete_repository(self, repo_name: str) -> bool:
        """ลบ Repo ถาวร"""
        owner = self.org_name or self.username
        self._request("DELETE", f"/repos/{owner}/{repo_name}")
        return True

    # ================ 📄 จัดการไฟล์ / โค้ด ================
    def create_file(self, repo_name: str, path: str, content: str, message: str, branch: str = "main") -> Dict:
        """สร้าง/อัปโหลดไฟล์เดียว"""
        owner = self.org_name or self.username
        content_b64 = base64.b64encode(content.encode()).decode()
        payload = {
            "message": message,
            "content": content_b64,
            "branch": branch
        }
        return self._request("PUT", f"/repos/{owner}/{repo_name}/contents/{path}", payload)
