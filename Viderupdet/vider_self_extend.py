# vider_self_extend.py - ระบบขยายความสามารถอัตโนมัติ รองรับดึงจาก GitHub
import os
import importlib.util
import requests
from datetime import datetime
from pathlib import Path

class ViderSelfExtend:
    def __init__(self, root_path=None):
        self.root = Path(root_path) if root_path else Path(__file__).parent.resolve()
        self.modules_dir = self.root
        self.registry_file = self.root / "vider_module_registry.json"
        self._registry = self._load_registry()
        print("🔧 VIDER SELF-EXTEND พร้อมทำงาน - สร้าง/ติดตั้ง/ดึงจาก GitHub ได้เลย")

    def _load_registry(self):
        """โหลดรายการโมดูลที่มีอยู่"""
        if self.registry_file.exists():
            import json
            with open(self.registry_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {"modules": {}, "last_update": None}

    def _save_registry(self):
        """บันทึกรายการโมดูล"""
        import json
        self._registry["last_update"] = datetime.utcnow().isoformat()
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self._registry, f, ensure_ascii=False, indent=2)

    # --- สร้างและติดตั้งจากโค้ดโดยตรง ---
    def create_and_install_module(self, module_name, module_code, description=""):
        """สร้างไฟล์โมดูลและลงทะเบียนใช้งานทันที"""
        if not module_name.endswith(".py"):
            module_name += ".py"

        module_path = self.modules_dir / module_name

        try:
            with open(module_path, "w", encoding="utf-8") as f:
                f.write(module_code.strip())
        except Exception as e:
            return {"success": False, "error": f"เขียนไฟล์ไม่ได้: {str(e)}"}

        self._registry["modules"][module_name] = {
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "source": "local",
            "enabled": True
        }
        self._save_registry()

        try:
            spec = importlib.util.spec_from_file_location(module_name[:-3], module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            setattr(self, module_name[:-3], module)
        except Exception as e:
            return {"success": True, "warning": f"สร้างสำเร็จ โหลดใหม่อีกครั้งจะใช้งานได้: {str(e)}"}

        return {
            "success": True,
            "message": f"✅ ติดตั้ง '{module_name}' เรียบร้อย",
            "path": str(module_path)
        }

    # --- ✅ เพิ่มใหม่: ดึงและติดตั้งจาก GitHub ---
    def install_from_github(self, raw_url, module_name=None, description=""):
        """
        ดึงไฟล์ .py จาก GitHub มาติดตั้งอัตโนมัติ
        raw_url = ลิงก์ดิบของไฟล์ (เช่น https://raw.githubusercontent.com/.../module.py)
        """
        try:
            response = requests.get(raw_url, timeout=15)
            response.raise_for_status()
            code = response.text

            if not module_name:
                module_name = raw_url.split("/")[-1]

            if not description:
                description = f"ดึงจาก GitHub: {raw_url}"

            return self.create_and_install_module(module_name, code, description)

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"ดึงข้อมูลไม่สำเร็จ: {str(e)}"}

    def list_installed_modules(self):
        """แสดงรายการโมดูลทั้งหมด"""
        return self._registry["modules"]

# vider_self_extend.py - ระบบขยายความสามารถอัตโนมัติ ไม่ต้องคัดลอกวางเอง
import os
import importlib.util
from datetime import datetime
from pathlib import Path

class ViderSelfExtend:
    def __init__(self, root_path=None):
        self.root = Path(root_path) if root_path else Path(__file__).parent.resolve()
        self.modules_dir = self.root
        self.registry_file = self.root / "vider_module_registry.json"
        self._registry = self._load_registry()
        print("🔧 VIDER SELF-EXTEND พร้อมทำงาน - สร้าง/ติดตั้งฟีเจอร์ได้เองอัตโนมัติ")

    def _load_registry(self):
        """โหลดรายการโมดูลที่มีอยู่"""
        if self.registry_file.exists():
            import json
            with open(self.registry_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {"modules": {}, "last_update": None}

    def _save_registry(self):
        """บันทึกรายการโมดูล"""
        import json
        self._registry["last_update"] = datetime.utcnow().isoformat()
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self._registry, f, ensure_ascii=False, indent=2)

    # --- ฟังก์ชันหลัก: สร้างและลงทะเบียนโมดูลใหม่ทันที ---
    def create_and_install_module(self, module_name, module_code, description=""):
        """
        รับชื่อโมดูลและโค้ด -> สร้างไฟล์ -> บันทึก -> เชื่อมต่อ -> พร้อมใช้งานทันที
        คุณไม่ต้องทำอะไรเพิ่ม
        """
        if not module_name.endswith(".py"):
            module_name += ".py"

        module_path = self.modules_dir / module_name

        # 1. เขียนไฟล์ลงดิสก์
        try:
            with open(module_path, "w", encoding="utf-8") as f:
                f.write(module_code.strip())
        except Exception as e:
            return {"success": False, "error": f"เขียนไฟล์ไม่ได้: {str(e)}"}

        # 2. ลงทะเบียนในระบบ
        self._registry["modules"][module_name] = {
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "enabled": True
        }
        self._save_registry()

        # 3. โหลดเข้าหน่วยความจำเพื่อใช้งานได้ทันที
        try:
            spec = importlib.util.spec_from_file_location(module_name[:-3], module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            setattr(self, module_name[:-3], module)
        except Exception as e:
            return {"success": True, "warning": f"สร้างสำเร็จ แต่โหลดทันทีไม่ได้: {str(e)}"}

        return {
            "success": True,
            "message": f"✅ สร้างและติดตั้ง '{module_name}' เรียบร้อย พร้อมใช้งานทันที",
            "path": str(module_path)
        }

    def list_installed_modules(self):
        """แสดงรายการทุกส่วนที่มีในระบบ"""
        return self._registry["modules"]
