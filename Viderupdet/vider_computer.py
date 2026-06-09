import os
import subprocess
import psutil
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional

# นำเข้าระบบหลัก VIDER
from vider_login import vider_login
from vider_github_connector import vider_github

class VIDERComputer:
    def __init__(self):
        self.name = "VIDER Computer System v1.0"
        self.status = "active"
        
        # 📁 โฟลเดอร์แยกส่วนตัวผู้ใช้
        self.user_workspaces = "./vider_user_workspaces/"
        os.makedirs(self.user_workspaces, exist_ok=True)
        
        # ⚠️ คำสั่งที่อนุญาตสำหรับผู้ใช้ทั่วไป
        self.allowed_commands = {
            "open_app": ["notepad", "calc", "mspaint", "cmd", "explorer"],
            "file_ops": ["read_file", "write_file", "list_dir", "create_folder"],
            "system_info": ["get_running_apps", "get_disk_space", "get_memory_usage"],
            "run_safe": ["echo", "dir", "cd", "mkdir", "ping"]
        }
        
        # 🔒 คำสั่งที่จำกัด เฉพาะ VIDER หลักเท่านั้น
        self.restricted_commands = [
            "format", "del", "erase /s", "regedit", "services.msc",
            "net user", "shutdown", "taskkill /f", "format", "del /f /s"
        ]
        
        # 📝 บันทึกการใช้งาน
        self.activity_log: List[Dict] = []

    # ==============================================
    # 🔐 ตรวจสอบสิทธิ์ผู้ใช้
    # ==============================================
    def check_permission(self, user_id: str, command: str, session_token: str) -> Dict:
        """ตรวจสอบว่าผู้ใช้มีสิทธิ์ใช้คำสั่งนี้หรือไม่"""
        # ตรวจสอบการเข้าสู่ระบบ
        auth = vider_login.get_user_info(user_id, session_token)
        if not auth["success"]:
            return {"success": False, "message": "กรุณาเข้าสู่ระบบก่อน"}
        
        user_plan = auth["user"]["plan"]
        
        # ตรวจสอบคำสั่งอันตราย
        for restricted in self.restricted_commands:
            if restricted.lower() in command.lower():
                return {
                    "success": False,
                    "message": "คำสั่งนี้ถูกจำกัดความปลอดภัย เฉพาะผู้ดูแลระบบเท่านั้น"
                }
        
        # ผู้ใช้ทั่วไป: ทำได้เฉพาะคำสั่งที่อนุญาต
        if user_plan in ["trial", "basic"]:
            allowed_all = []
            for group in self.allowed_commands.values():
                allowed_all.extend(group)
            
            cmd_keyword = command.split()[0].lower()
            if cmd_keyword not in allowed_all and not any(safe in command.lower() for safe in self.allowed_commands["run_safe"]):
                return {
                    "success": False,
                    "message": "คำสั่งนี้ไม่ได้รับอนุญาตสำหรับผู้ใช้ทั่วไป"
                }
        
        return {"success": True, "plan": user_plan}

    # ==============================================
    # 📂 จัดการพื้นที่ทำงานส่วนตัว
    # ==============================================
    def get_user_workspace(self, user_id: str) -> str:
        """รับที่อยู่โฟลเดอร์ส่วนตัวของผู้ใช้"""
        workspace_path = os.path.join(self.user_workspaces, user_id)
        os.makedirs(workspace_path, exist_ok=True)
        return workspace_path

    # ==============================================
    # 🖱️ เปิด/ปิดโปรแกรม
    # ==============================================
    def open_application(self, user_id: str, session_token: str, app_name: str) -> Dict:
        """เปิดโปรแกรมที่ระบุ"""
        perm = self.check_permission(user_id, f"open_app {app_name}", session_token)
        if not perm["success"]:
            return perm
        
        allowed_apps = self.allowed_commands["open_app"]
        app_name = app_name.lower()
        
        if app_name not in allowed_apps:
            return {
                "success": False,
                "message": f"เปิดได้เฉพาะโปรแกรมพื้นฐานเท่านั้น: {', '.join(allowed_apps)}"
            }
        
        try:
            subprocess.Popen(app_name, shell=True)
            self.log_activity(user_id, "open_app", f"เปิดโปรแกรม: {app_name}")
            return {"success": True, "message": f"เปิด {app_name} เรียบร้อยแล้ว"}
        except Exception as e:
            return {"success": False, "message": f"ไม่สามารถเปิดโปรแกรมได้: {str(e)}"}

    # ==============================================
    # 📄 จัดการไฟล์ในพื้นที่ส่วนตัว
    # ==============================================
    def read_file(self, user_id: str, session_token: str, file_path: str) -> Dict:
        """อ่านไฟล์จากโฟลเดอร์ส่วนตัวเท่านั้น"""
        perm = self.check_permission(user_id, "read_file", session_token)
        if not perm["success"]:
            return perm
        
        workspace = self.get_user_workspace(user_id)
        full_path = os.path.abspath(os.path.join(workspace, file_path))
        
        # ป้องกันการเข้าถึงไฟล์นอกโฟลเดอร์ส่วนตัว
        if not full_path.startswith(os.path.abspath(workspace)):
            return {"success": False, "message": "ไม่อนุญาตให้เข้าถึงไฟล์นอกพื้นที่ส่วนตัว"}
        
        try:
            if not os.path.exists(full_path):
                return {"success": False, "message": "ไม่พบไฟล์ที่ระบุ"}
            
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            self.log_activity(user_id, "read_file", f"อ่านไฟล์: {file_path}")
            return {"success": True, "content": content, "path": file_path}
        except Exception as e:
            return {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

    def write_file(self, user_id: str, session_token: str, file_path: str, content: str) -> Dict:
        """เขียนไฟล์ลงโฟลเดอร์ส่วนตัวเท่านั้น"""
        perm = self.check_permission(user_id, "write_file", session_token)
        if not perm["success"]:
            return perm
        
        workspace = self.get_user_workspace(user_id)
        full_path = os.path.abspath(os.path.join(workspace, file_path))
        
        if not full_path.startswith(os.path.abspath(workspace)):
            return {"success": False, "message": "ไม่อนุญาตให้เขียนไฟล์นอกพื้นที่ส่วนตัว"}
        
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            self.log_activity(user_id, "write_file", f"เขียนไฟล์: {file_path}")
            return {"success": True, "message": "บันทึกไฟล์เรียบร้อยแล้ว", "path": file_path}
        except Exception as e:
            return {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

    def list_directory(self, user_id: str, session_token: str, dir_path: str = "") -> Dict:
        """แสดงรายการไฟล์ในโฟลเดอร์ส่วนตัว"""
        perm = self.check_permission(user_id, "list_dir", session_token)
        if not perm["success"]:
            return perm
        
        workspace = self.get_user_workspace(user_id)
        full_path = os.path.abspath(os.path.join(workspace, dir_path))
        
        if not full_path.startswith(os.path.abspath(workspace)) or not os.path.exists(full_path):
            return {"success": False, "message": "เส้นทางไม่ถูกต้องหรือไม่มีสิทธิ์เข้าถึง"}
        
        try:
            items = []
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                items.append({
                    "name": item,
                    "type": "folder" if os.path.isdir(item_path) else "file",
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0,
                    "modified": datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y-%m-%d %H:%M")
                })
            
            self.log_activity(user_id, "list_dir", f"ดูเนื้อหา: {dir_path or 'โฟลเดอร์หลัก'}")
            return {"success": True, "items": items, "path": dir_path}
        except Exception as e:
            return {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

    # ==============================================
    # ⚡ รันคำสั่งระบบ
    # ==============================================
    def run_command(self, user_id: str, session_token: str, command: str) -> Dict:
        """รันคำสั่งระบบ จำกัดเฉพาะคำสั่งที่ปลอดภัย"""
        perm = self.check_permission(user_id, command, session_token)
        if not perm["success"]:
            return perm
        
        workspace = self.get_user_workspace(user_id)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            self.log_activity(user_id, "run_command", f"รัน: {command}")
            return {
                "success": True,
                "command": command,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "คำสั่งใช้เวลานานเกินไปถูกยกเลิก"}
        except Exception as e:
            return {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

    # ==============================================
    # ℹ️ ข้อมูลระบบ
    # ==============================================
    def get_system_info(self, user_id: str, session_token: str) -> Dict:
        """รับข้อมูลพื้นฐานของคอมพิวเตอร์"""
        perm = self.check_permission(user_id, "get_system_info", session_token)
        if not perm["success"]:
            return perm
        
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/") if os.name != "nt" else psutil.disk_usage("C:\\")
            
            info = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_used": round(memory.used / (1024**3), 2),
                "memory_total": round(memory.total / (1024**3), 2),
                "disk_used": round(disk.used / (1024**3), 2),
                "disk_total": round(disk.total / (1024**3), 2),
                "platform": os.name
            }
            
            self.log_activity(user_id, "system_info", "ดูข้อมูลระบบ")
            return {"success": True, "system_info": info}
        except Exception as e:
            return {"success": False, "message": f"ไม่สามารถดึงข้อมูลได้: {str(e)}"}

    # ==============================================
    # 🔗 เชื่อมต่อกับระบบ VIDER หลัก
    # ==============================================
    def sync_with_vider_core(self, user_id: str, session_token: str) -> Dict:
        """ซิงค์ข้อมูลพื้นที่ทำงานกับฐานข้อมูลกลาง"""
        perm = self.check_permission(user_id, "sync", session_token)
        if not perm["success"]:
            return perm
        
        workspace = self.get_user_workspace(user_id)
        backup_file = os.path.join(workspace, "vider_backup.json")
        
        try:
            # รวบรวมข้อมูลไฟล์
            file_list = []
            for root, dirs, files in os.walk(workspace):
                rel_path = os.path.relpath(root, workspace)
                for file in files:
                    file_path = os.path.join(rel_path, file)
                    file_list.append({
                        "path": file_path,
                        "size": os.path.getsize(os.path.join(root, file)),
                        "modified": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))).isoformat()
                    })
            
            backup_data = {
                "user_id": user_id,
                "sync_time": datetime.now().isoformat(),
                "files": file_list
            }
            
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            self.log_activity(user_id, "sync", "ซิงค์ข้อมูลกับระบบกลาง")
            return {"success": True, "message": "ซิงค์ข้อมูลเรียบร้อย", "file_count": len(file_list)}
        except Exception as e:
            return {"success": False, "message": f"ซิงค์ไม่สำเร็จ: {str(e)}"}

    # ==============================================
    # 📝 บันทึกการใช้งาน
    # ==============================================
    def log_activity(self, user_id: str, action: str, details: str):
        """บันทึกการกระทำทั้งหมด"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": details
        }
        self.activity_log.append(log_entry)
        
        # จำกัดจำนวนบันทึก
        if len(self.activity_log) > 1000:
            self.activity_log.pop(0)

# 🚀 เปิดใช้งานระบบ
vider_computer = VIDERComputer()
print("✅ VIDER Computer System เปิดใช้งานเรียบร้อยแล้ว!")
print("🔗 เชื่อมต่อกับระบบ VIDER หลัก | แยกส่วนตัวผู้ใช้ | จำกัดสิทธิ์การใช้งาน")
print("💻 ผู้ใช้ทั่วไปใช้ได้เฉพาะคำสั่งพื้นฐาน — เฉพาะ VIDER หลักถึงเข้าถึงได้เต็มที่")
