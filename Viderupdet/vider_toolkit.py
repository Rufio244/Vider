# vider_toolkit.py - ชุดเครื่องมือเสริมสำหรับระบบ VIDER
import os
import sys
import subprocess
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
import json

class ViderToolkit:
    def __init__(self):
        self.base_dir = Path("./vider_workspace/")
        self.base_dir.mkdir(exist_ok=True)
        self.tools_dir = self.base_dir / "tools"
        self.tools_dir.mkdir(exist_ok=True)
        self.backup_dir = self.base_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        print("🔧 ชุดเครื่องมือ VIDER พร้อมใช้งาน")

    # ────────────────────────────────────────────────
    # 1. ตัวจัดการสคริปต์และการรันระบบ
    # ────────────────────────────────────────────────
    def run_application(self, app_name):
        """รันระบบที่สร้างไว้"""
        app_path = Path("./created_applications") / app_name
        if not app_path.exists():
            return {"success": False, "message": f"ไม่พบระบบชื่อ {app_name}"}

        start_file = app_path / "start.py"
        app_file = app_path / "app.py"

        if start_file.exists():
            target = start_file
        elif app_file.exists():
            target = app_file
        else:
            return {"success": False, "message": "ไม่พบไฟล์เริ่มทำงาน"}

        print(f"🚀 กำลังรัน {app_name} ...")
        try:
            subprocess.run([sys.executable, str(target)], cwd=str(app_path))
            return {"success": True, "message": f"ปิดด้วยการกด Ctrl+C"}
        except KeyboardInterrupt:
            return {"success": True, "message": "ปิดระบบเรียบร้อย"}

    # ────────────────────────────────────────────────
    # 2. ตัวเปิดใช้งานออนไลน์ (ใช้ ngrok อัตโนมัติ)
    # ────────────────────────────────────────────────
    def expose_to_internet(self, port=8080):
        """เปิดระบบให้เข้าถึงได้จากทุกที่"""
        print("🌐 กำลังเตรียมเปิดใช้งานออนไลน์...")
        
        # ตรวจสอบว่ามี ngrok หรือไม่
        ngrok_names = ["ngrok.exe", "ngrok", "ngrok-linux"]
        ngrok_path = None
        for name in ngrok_names:
            test = self.tools_dir / name
            if test.exists():
                ngrok_path = test
                break

        if not ngrok_path:
            return {
                "success": False,
                "message": "❌ ยังไม่มี ngrok\nดาวน์โหลดได้ที่: https://ngrok.com/\nแล้ววางไว้ในโฟลเดอร์ vider_workspace/tools/"
            }

        print(f"🔗 เปิดพอร์ต {port} สู่โลกออนไลน์")
        try:
            proc = subprocess.Popen([str(ngrok_path), "http", str(port)])
            return {
                "success": True,
                "message": "✅ เปิดแล้ว\nดูลิงก์ได้จากหน้าต่างที่เปิดขึ้น",
                "process": proc
            }
        except Exception as e:
            return {"success": False, "message": f"ผิดพลาด: {str(e)}"}

    # ────────────────────────────────────────────────
    # 3. ตัวตรวจสอบความพร้อมของระบบ
    # ────────────────────────────────────────────────
    def check_system(self):
        """ตรวจสอบว่าคอมพิวเตอร์พร้อมสร้างระบบหรือไม่"""
        report = {"ok": True, "items": [], "missing": []}

        # ตรวจสอบ Python
        py_ver = sys.version_info
        if py_ver.major >= 3 and py_ver.minor >= 8:
            report["items"].append(f"✅ Python: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
        else:
            report["ok"] = False
            report["missing"].append("Python 3.8 ขึ้นไป")

        # ตรวจสอบแพ็กเกจพื้นฐาน
        required = ["flask", "flask-sqlalchemy", "flask-login", "flask-bcrypt"]
        for pkg in required:
            try:
                __import__(pkg.replace("-", "_"))
                report["items"].append(f"✅ {pkg} ติดตั้งแล้ว")
            except ImportError:
                report["ok"] = False
                report["missing"].append(pkg)

        if report["missing"]:
            report["items"].append("\n📥 สามารถติดตั้งได้ทั้งหมดด้วยคำสั่ง:")
            report["items"].append(f"pip install {' '.join(report['missing'])}")

        return {
            "success": report["ok"],
            "message": "\n".join(report["items"]),
            "missing": report["missing"]
        }

    # ────────────────────────────────────────────────
    # 4. ตัวสำรองและกู้คืนข้อมูล
    # ────────────────────────────────────────────────
    def backup_application(self, app_name):
        """สำรองระบบเก็บเป็นไฟล์ ZIP"""
        source = Path("./created_applications") / app_name
        if not source.exists():
            return {"success": False, "message": "ไม่พบระบบที่ต้องการสำรอง"}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"{app_name}_backup_{timestamp}.zip"

        with zipfile.ZipFile(str(backup_file), "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in source.rglob("*"):
                if file.is_file():
                    zipf.write(file, arcname=file.relative_to(source))

        return {
            "success": True,
            "message": f"✅ สำรองเสร็จ\nที่: {backup_file.resolve()}",
            "path": str(backup_file)
        }

    def list_applications(self):
        """แสดงรายการระบบที่สร้างไว้"""
        apps_dir = Path("./created_applications")
        if not apps_dir.exists():
            return {"success": True, "message": "ยังไม่มีระบบที่สร้างไว้", "apps": []}

        apps = [d.name for d in apps_dir.iterdir() if d.is_dir()]
        if not apps:
            return {"success": True, "message": "ยังไม่มีระบบ", "apps": []}

        return {
            "success": True,
            "message": f"📋 มี {len(apps)} ระบบ:\n" + "\n".join(f"• {a}" for a in apps),
            "apps": apps
        }

    # ────────────────────────────────────────────────
    # 5. ตัวติดตั้งแพ็กเกจอัตโนมัติ
    # ────────────────────────────────────────────────
    def install_requirements(self):
        """ติดตั้งสิ่งที่จำเป็นทั้งหมด"""
        print("📥 กำลังติดตั้งส่วนประกอบที่จำเป็น...")
        packages = [
            "Flask==2.3.3",
            "Flask-SQLAlchemy==3.1.1",
            "Flask-Login==0.6.3",
            "Flask-Bcrypt==1.0.1"
        ]

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
            return {"success": True, "message": "✅ ติดตั้งครบถ้วนแล้ว"}
        except Exception as e:
            return {"success": False, "message": f"❌ ผิดพลาด: {str(e)}"}

# ────────────────────────────────────────────────
# เมนูหลักใช้งานง่าย
# ────────────────────────────────────────────────
if __name__ == "__main__":
    tool = ViderToolkit()

    print("\n" + "="*55)
    print("🛠️  VIDER TOOLKIT - ชุดเครื่องมือเสริม")
    print("="*55)

    while True:
        print("\nเมนูเครื่องมือ:")
        print("1. ตรวจสอบความพร้อมระบบ")
        print("2. ติดตั้งสิ่งที่จำเป็น")
        print("3. แสดงรายการระบบที่สร้าง")
        print("4. รันระบบที่มีอยู่")
        print("5. เปิดใช้งานออนไลน์ (ngrok)")
        print("6. สำรองข้อมูลระบบ")
        print("7. ออก")

        choice = input("\nเลือกเบอร์: ").strip()

        if choice == "1":
            res = tool.check_system()
            print("\n" + res["message"])

        elif choice == "2":
            res = tool.install_requirements()
            print("\n" + res["message"])

        elif choice == "3":
            res = tool.list_applications()
            print("\n" + res["message"])

        elif choice == "4":
            name = input("\nชื่อระบบที่ต้องการรัน: ").strip()
            res = tool.run_application(name)
            print("\n" + res["message"])

        elif choice == "5":
            port = input("พอร์ต (ค่าเริ่มต้น 8080): ").strip() or "8080"
            res = tool.expose_to_internet(port)
            print("\n" + res["message"])

        elif choice == "6":
            name = input("\nชื่อระบบที่ต้องการสำรอง: ").strip()
            res = tool.backup_application(name)
            print("\n" + res["message"])

        elif choice == "7":
            print("👋 ปิดเครื่องมือ")
            break

        else:
            print("⚠️ กรุณาเลือกตัวเลข 1-7")
