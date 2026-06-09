# vider_computer_agent.py - จุดควบคุมหลัก
from pathlib import Path
from vider_self_extend import ViderSelfExtend

class ViderMainAgent:
    def __init__(self):
        self.root = Path(__file__).parent
        self.extender = ViderSelfExtend(self.root)
        self._load_core_modules()
        print("🤖 VIDER AGENT พร้อมทำงานอย่างสมบูรณ์")

    def _load_core_modules(self):
        """โหลดส่วนหลักที่มีอยู่แล้ว"""
        try:
            from vider_language_analyzer import ViderLanguageAnalyzer
            from vider_value_optimizer import ViderValueOptimizer
            from vider_api_manager import ViderAPIManager
            from vider_sonthi import ViderSonthi

            self.lang = ViderLanguageAnalyzer()
            self.optimizer = ViderValueOptimizer()
            self.api = ViderAPIManager()
            self.sonthi = ViderSonthi()
            print("📚 โหลดส่วนหลักครบถ้วน")
        except Exception as e:
            print(f"⚠️ บางส่วนยังไม่พร้อม: {e}")

    # --- ฟังก์ชันสำคัญ: สั่งสร้างฟีเจอร์ใหม่ที่นี่เลย ---
    def create_new_feature(self, name, code, description=""):
        """สั่งสร้างส่วนขยายใหม่ -> สร้างไฟล์และเปิดใช้งานให้เลย"""
        result = self.extender.create_and_install_module(name, code, description)
        print(result["message"])
        return result

    def run(self):
        """เมนูหลักแบบรวมศูนย์"""
        print("\n=== ระบบ VIDER หลัก ===")
        print("1. สร้าง/พัฒนาระบบตามความต้องการ")
        print("2. ตรวจสอบความสัมพันธ์ข้อมูล (SONTHI)")
        print("3. จัดการข้อมูลจาก API")
        print("4. ดูรายการส่วนขยายทั้งหมด")
        print("5. สร้างส่วนขยายใหม่อัตโนมัติ")
        print("0. ออกจากระบบ")

if __name__ == "__main__":
    agent = ViderMainAgent()
    agent.run()

from vider_sonthi import ViderSonthi

09๐from vider_api_manager import ViderAPIManager  # เพิ่มบรรทัดนี้

# vider_computer_agent.py - ตัวแทนทำงานอัตโนมัติสำหรับคอมพิวเตอร์
import os
import sys
import subprocess
import urllib.request
import json
import shutil
import socket
from pathlib import Path
from datetime import datetime

# ────────────────────────────────────────────────
# การตั้งค่าการเชื่อมต่อระบบ VIDER
# ────────────────────────────────────────────────
VIDER_CORE_ENDPOINT = "https://vider-core-system.example.com/api"  # เปลี่ยนเป็นที่อยู่จริงเมื่อติดตั้ง
AGENT_ID_FILE = Path("./vider_agent_id.txt")
CONFIG_FILE = Path("./vider_config.json")

class ViderComputerAgent:
    def __init__(self):
        self.work_dir = Path("./vider_environment/")
        self.work_dir.mkdir(exist_ok=True)
        self.tools_dir = self.work_dir / "tools"
        self.tools_dir.mkdir(exist_ok=True)
        self.data_dir = self.work_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.log_file = self.work_dir / "agent.log"
        
        print("🤖 VIDER COMPUTER AGENT เริ่มทำงาน")
        self._log("ตัวแทนเริ่มทำงาน", "INFO")

    def _log(self, message, level="INFO"):
        """บันทึกเหตุการณ์"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())

    # ────────────────────────────────────────────────
    # 1. ตรวจสอบและติดตั้งสิ่งที่จำเป็นอัตโนมัติ
    # ────────────────────────────────────────────────
    def install_all_requirements(self):
        """ตรวจสอบและติดตั้งทุกอย่างที่ต้องใช้เอง"""
        self._log("เริ่มตรวจสอบและติดตั้งส่วนประกอบ")

        # ตรวจสอบ Python
        py_version = sys.version_info
        if py_version < (3, 8):
            self._log("ต้องการ Python 3.8 ขึ้นไป กำลังแนะนำ...", "WARNING")
            return False

        # รายการแพ็กเกจที่ต้องมี
        required_packages = [
            "Flask==2.3.3",
            "Flask-SQLAlchemy==3.1.1",
            "Flask-Login==0.6.3",
            "Flask-Bcrypt==1.0.1",
            "requests==2.31.0",
            "psutil==5.9.6"
        ]

        installed = []
        missing = []

        # ตรวจสอบทีละตัว
        for pkg in required_packages:
            pkg_name = pkg.split("==")[0].replace("-", "_")
            try:
                __import__(pkg_name)
                installed.append(pkg)
                self._log(f"✅ มีแล้ว: {pkg}")
            except ImportError:
                missing.append(pkg)
                self._log(f"❌ ยังไม่มี: {pkg}")

        # ติดตั้งที่ขาด
        if missing:
            self._log(f"กำลังติดตั้ง {len(missing)} แพ็กเกจที่ขาด")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "--upgrade"
                ] + missing, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._log("✅ ติดตั้งแพ็กเกจสำเร็จทั้งหมด")
            except Exception as e:
                self._log(f"❌ ติดตั้งไม่สำเร็จ: {str(e)}", "ERROR")
                return False

        # ดาวน์โหลดเครื่องมือเสริม (ngrok สำหรับเปิดพอร์ต)
        self._download_additional_tools()

        self._log("✅ ส่วนประกอบทั้งหมดพร้อมใช้งาน")
        return True

    def _download_additional_tools(self):
        """ดาวน์โหลดเครื่องมือภายนอกที่จำเป็น"""
        self._log("ตรวจสอบเครื่องมือเสริม")
        
        # ตรวจสอบระบบปฏิบัติการ
        if sys.platform.startswith("win"):
            ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
            ngrok_file = self.tools_dir / "ngrok.exe"
        elif sys.platform.startswith("linux"):
            ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
            ngrok_file = self.tools_dir / "ngrok"
        else:
            self._log("ระบบปฏิบัติการยังไม่รองรับการดาวน์โหลดอัตโนมัติ", "WARNING")
            return

        # ถ้ายังไม่มี ให้ดาวน์โหลด
        if not ngrok_file.exists():
            try:
                self._log("กำลังดาวน์โหลดเครื่องมือเชื่อมต่อ...")
                temp_file = self.tools_dir / "ngrok_temp"
                urllib.request.urlretrieve(ngrok_url, str(temp_file))
                
                # แตกไฟล์
                if ngrok_url.endswith(".zip"):
                    import zipfile
                    with zipfile.ZipFile(str(temp_file), "r") as zf:
                        for file in zf.namelist():
                            if "ngrok" in file:
                                zf.extract(file, str(self.tools_dir))
                                shutil.move(str(self.tools_dir / file), str(ngrok_file))
                elif ngrok_url.endswith(".tgz"):
                    import tarfile
                    with tarfile.open(str(temp_file), "r:gz") as tf:
                        for member in tf.getmembers():
                            if "ngrok" in member.name and member.isfile():
                                tf.extract(member, str(self.tools_dir))
                                shutil.move(str(self.tools_dir / member.name), str(ngrok_file))

                temp_file.unlink(missing_ok=True)
                ngrok_file.chmod(0o755)
                self._log("✅ ดาวน์โหลดเครื่องมือเชื่อมต่อสำเร็จ")

            except Exception as e:
                self._log(f"⚠️ ไม่สามารถดาวน์โหลดเครื่องมือได้: {str(e)}", "WARNING")

    # ────────────────────────────────────────────────
    # 2. เชื่อมต่ออัตโนมัติกับระบบหลัก VIDER
    # ────────────────────────────────────────────────
    def connect_to_vider_core(self):
        """เชื่อมต่อและลงทะเบียนกับระบบหลัก VIDER"""
        self._log("กำลังเชื่อมต่อกับระบบหลัก VIDER")

        # โหลดข้อมูลตัวแทนเดิมถ้ามี
        agent_id = None
        if AGENT_ID_FILE.exists():
            with open(AGENT_ID_FILE, "r", encoding="utf-8") as f:
                agent_id = f.read().strip()

        # สร้างข้อมูลเพื่อลงทะเบียน/เชื่อมต่อ
        system_info = {
            "agent_id": agent_id,
            "hostname": socket.gethostname(),
            "ip_address": self._get_local_ip(),
            "os": sys.platform,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            # ส่งข้อมูลไปยังระบบหลัก
            import requests
            response = requests.post(
                f"{VIDER_CORE_ENDPOINT}/agent/connect",
                json=system_info,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                new_agent_id = data.get("agent_id")
                if new_agent_id and new_agent_id != agent_id:
                    with open(AGENT_ID_FILE, "w", encoding="utf-8") as f:
                        f.write(new_agent_id)
                    agent_id = new_agent_id

                self._log(f"✅ เชื่อมต่อสำเร็จ | รหัสตัวแทน: {agent_id[:8]}...")
                return True, agent_id

            else:
                self._log(f"⚠️ เชื่อมต่อไม่สำเร็จ รหัส: {response.status_code}", "WARNING")
                # ทำงานแบบออฟไลน์ได้ด้วย
                return True, "OFFLINE-" + datetime.now().strftime("%Y%m%d")

        except Exception as e:
            self._log(f"⚠️ ไม่สามารถเชื่อมต่อออนไลน์ได้: {str(e)} | ทำงานแบบอิสระ", "WARNING")
            return True, "STANDALONE-" + datetime.now().strftime("%Y%m%d")

    def _get_local_ip(self):
        """ดึงที่อยู่ IP ภายในเครื่อง"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "127.0.0.1"

    # ────────────────────────────────────────────────
    # 3. จัดการฐานข้อมูลเฉพาะส่วนของ VIDER
    # ────────────────────────────────────────────────
    def setup_local_database(self):
        """เตรียมฐานข้อมูลที่เชื่อมกับระบบ VIDER เท่านั้น"""
        db_path = self.data_dir / "vider_agent_db.db"
        self._log(f"เตรียมฐานข้อมูลที่: {db_path}")

        # สร้างโครงสร้างฐานข้อมูล
        try:
            from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
            from sqlalchemy.ext.declarative import declarative_base
            from sqlalchemy.orm import sessionmaker

            engine = create_engine(f"sqlite:///{db_path}")
            Base = declarative_base()

            # ตารางเก็บคำสั่งและงานที่ได้รับจาก VIDER
            class ViderTask(Base):
                __tablename__ = "vider_tasks"
                id = Column(Integer, primary_key=True)
                task_id = Column(String(100), unique=True)
                description = Column(Text)
                status = Column(String(30), default="pending")
                created_at = Column(DateTime, default=datetime.utcnow)
                completed_at = Column(DateTime, nullable=True)
                result = Column(Text, nullable=True)

            # ตารางเก็บการตั้งค่าเฉพาะ
            class ViderConfig(Base):
                __tablename__ = "vider_config"
                key = Column(String(100), primary_key=True)
                value = Column(Text)
                updated_at = Column(DateTime, default=datetime.utcnow)

            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            self.db_session = Session()

            self._log("✅ ฐานข้อมูลท้องถิ่นพร้อมใช้งาน เชื่อมต่อกับระบบ VIDER เท่านั้น")
            return True

        except Exception as e:
            self._log(f"❌ เตรียมฐานข้อมูลไม่สำเร็จ: {str(e)}", "ERROR")
            return False

    # ────────────────────────────────────────────────
    # 4. รันโหมดทำงานอัตโนมัติ
    # ────────────────────────────────────────────────
    def run_autonomous_mode(self):
        """โหมดทำงานอัตโนมัติเหมือน VIDER เป็นคนใช้คอมเอง"""
        self._log("เริ่มโหมดทำงานอัตโนมัติ")
        
        while True:
            try:
                print("\n" + "="*60)
                print("🤖 VIDER AGENT - ทำงานอัตโนมัติ")
                print("สถานะ: พร้อมรับคำสั่ง | เชื่อมต่อ: " + ("ออนไลน์" if self._check_connection() else "ออฟไลน์"))
                print("="*60)
                print("\nตัวเลือกการทำงาน:")
                print("1. สร้างระบบใหม่ตามเป้าหมาย")
                print("2. แก้ไข/จัดการระบบที่มีอยู่")
                print("3. สถานะการเชื่อมต่อ")
                print("4. ดูบันทึกการทำงาน")
                print("5. ออกจากการทำงาน")

                choice = input("\nเลือกการทำงาน: ").strip()

                if choice == "1":
                    self._create_new_system_workflow()
                elif choice == "2":
                    self._manage_existing_system()
                elif choice == "3":
                    ok, aid = self.connect_to_vider_core()
                    if ok:
                        print(f"✅ เชื่อมต่อสำเร็จ | รหัส: {aid[:12]}...")
                elif choice == "4":
                    self._show_logs()
                elif choice == "5":
                    self._log("ปิดการทำงานตัวแทน")
                    print("👋 ปิดระบบ VIDER Agent")
                    break
                else:
                    print("⚠️ กรุณาเลือก 1-5 เท่านั้น")

            except KeyboardInterrupt:
                self._log("ผู้ใช้สั่งหยุดการทำงาน")
                break
            except Exception as e:
                self._log(f"เกิดข้อผิดพลาด: {str(e)}", "ERROR")
                input("กด Enter เพื่อดำเนินการต่อ...")

    def _check_connection(self):
        """ตรวจสอบว่ายังเชื่อมต่อได้หรือไม่"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except:
            return False

    def _create_new_system_workflow(self):
        """กระบวนการสร้างระบบใหม่"""
        name = input("\n📌 ชื่อระบบ (ห้ามขึ้นต้นด้วย Vider): ").strip()
        if name.lower().startswith("vider"):
            print("❌ ชื่อห้ามขึ้นต้นด้วยคำว่า Vider")
            return

        desc = input("📝 รายละเอียด/เป้าหมายที่ต้องการสร้าง: ").strip()
        if not desc:
            print("❌ ต้องระบุรายละเอียด")
            return

        self._log(f"รับคำขอสร้างระบบ: {name}")
        
        # เรียกใช้ตัวสร้างอัตโนมัติ
        try:
            from vider_auto_builder import ViderAutoBuilder
            builder = ViderAutoBuilder()
            result = builder.create_application(name, desc)
            
            if result["success"]:
                print(f"\n✅ สร้างสำเร็จ!")
                print(f"📂 ที่เก็บ: {result['project_path']}")
                print(f"▶️ รันได้ด้วย: python {result['project_path']}/start.py")
            else:
                print(f"\n❌ ไม่สำเร็จ: {result['message']}")

        except ImportError:
            print("❌ ไม่พบตัวสร้างหลัก (vider_auto_builder.py) กรุณาวางไฟล์ไว้ในที่เดียวกัน")
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")

    def _manage_existing_system(self):
        """จัดการระบบที่มีอยู่"""
        apps_dir = Path("./created_applications")
        if not apps_dir.exists():
            print("❌ ยังไม่มีระบบที่สร้างไว้")
            return

        apps = [d.name for d in apps_dir.iterdir() if d.is_dir()]
        if not apps:
            print("❌ ยังไม่มีระบบที่สร้างไว้")
            return

        print("\n📋 ระบบที่มีอยู่:")
        for i, app in enumerate(apps, 1):
            print(f"{i}. {app}")

        choice = input("\nเลือกเบอร์ระบบที่ต้องการจัดการ: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(apps):
                selected = apps[idx]
                print(f"\n🔧 กำลังจัดการ: {selected}")
                action = input("ต้องการ: [1]รันระบบ | [2]แก้ไข | [3]สำรอง: ").strip()
                if action == "1":
                    from vider_toolkit import ViderToolkit
                    tk = ViderToolkit()
                    tk.run_application(selected)
        except:
            print("❌ เลือกไม่ถูกต้อง")

    def _show_logs(self):
        """แสดงบันทึกล่าสุด"""
        if not self.log_file.exists():
            print("📄 ยังไม่มีบันทึก")
            return

        print("\n📋 บันทึกล่าสุด:")
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[-15:]  # แสดง 15 บรรทัดล่าสุด
            print("".join(lines))

# ────────────────────────────────────────────────
# เริ่มการทำงาน
# ────────────────────────────────────────────────
if __name__ == "__main__":
    agent = ViderComputerAgent()

    # ขั้นตอนอัตโนมัติเมื่อเริ่มครั้งแรก
    print("\n🔄 กำลังเตรียมระบบครั้งแรก...")
    agent.install_all_requirements()
    agent.setup_local_database()
    agent.connect_to_vider_core()

    # เริ่มทำงาน
    agent.run_autonomous_mode()



# ตัวอย่างการเรียกใช้ในตัวสร้าง
from vider_language_analyzer import ViderLanguageAnalyzer

analyzer = ViderLanguageAnalyzer()
analysis = analyzer.analyze_text(คำสั่งของผู้ใช้)
plan = analyzer.generate_action_plan(analysis)

if plan["can_execute"]:
    # สร้างตามแผนที่วางไว้อย่างแม่นยำ
    pass
else:
    # ถามเพิ่มเติมเพื่อความชัดเจน
    pass
