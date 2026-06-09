# vider_api_manager.py - โมดูลจัดการ API: ดึงข้อมูล, วิเคราะห์, และนำมาใช้งาน
import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ViderAPIManager:
    def __init__(self):
        self.data_dir = Path("./vider_environment/api_data/")
        self.data_dir.mkdir(exist_ok=True)
        self.config_file = self.data_dir / "api_configs.json"
        self._load_api_configs()
        print("🌐 โมดูลจัดการ API พร้อมทำงาน - ดึงข้อมูลได้จริงและนำมาใช้")

    def _load_api_configs(self):
        """โหลดการตั้งค่า API ที่เคยใช้ไว้ (จดจำได้ครั้งหน้า)"""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.api_configs = json.load(f)
        else:
            self.api_configs = {
                "saved_configs": [],  # เก็บการตั้งค่า API ที่เคยใช้
                "last_used": None     # API ที่ใช้ล่าสุด
            }
            self._save_api_configs()

    def _save_api_configs(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.api_configs, f, ensure_ascii=False, indent=2)

    # ────────────────────────────────────────────────
    # 1. ดึงข้อมูลจาก API ได้จริง
    # ────────────────────────────────────────────────
    def fetch_from_api(
        self,
        api_url: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        save_config: bool = True
    ) -> Dict:
        """
        ดึงข้อมูลจาก API ด้วยวิธี GET/POST
        :return: ผลลัพธ์รวม: สถานะ, ข้อมูล, ข้อผิดพลาด (ถ้ามี)
        """
        result = {
            "success": False,
            "data": None,
            "error": None,
            "timestamp": datetime.utcnow().isoformat(),
            "api_url": api_url
        }

        # ตั้งค่าพื้นฐาน
        headers = headers or {}
        params = params or {}
        data = data or {}

        try:
            # ส่งคำขอไปยัง API
            if method.upper() == "GET":
                response = requests.get(api_url, headers=headers, params=params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(api_url, headers=headers, json=data, timeout=10)
            else:
                result["error"] = "วิธีดึงข้อมูลไม่รองรับ (เฉพาะ GET/POST)"
                return result

            # ตรวจสอบสถานะการตอบกลับ
            response.raise_for_status()  # โยนข้อผิดพลาดถ้าสถานะไม่ใช่ 200-299

            # อ่านข้อมูลตามรูปแบบ
            try:
                api_data = response.json()
            except json.JSONDecodeError:
                api_data = response.text  # ถ้าไม่ใช่ JSON ให้อ่านเป็นข้อความธรรมดา

            result["success"] = True
            result["data"] = api_data
            result["status_code"] = response.status_code

            # บันทึกการตั้งค่า API เพื่อใช้ครั้งหน้า
            if save_config:
                self._save_api_config(api_url, method, headers, params, data)

            return result

        except requests.exceptions.RequestException as e:
            result["error"] = f"ไม่สามารถเชื่อมต่อ API ได้: {str(e)}"
            return result

    # ────────────────────────────────────────────────
    # 2. บันทึกการตั้งค่า API เพื่อใช้ครั้งหน้า
    # ────────────────────────────────────────────────
    def _save_api_config(
        self,
        api_url: str,
        method: str,
        headers: Dict,
        params: Dict,
        data: Dict
    ):
        """บันทึกการตั้งค่า API ที่ใช้แล้ว เพื่อไม่ต้องใส่ใหม่ครั้งหน้า"""
        config = {
            "api_name": api_url.split("/")[-2] if "/" in api_url else api_url,
            "api_url": api_url,
            "method": method,
            "headers": headers,
            "params": params,
            "data": data,
            "last_used": datetime.utcnow().isoformat()
        }

        # ตรวจสอบว่ามีอยู่แล้วหรือไม่
        existing = [c for c in self.api_configs["saved_configs"] if c["api_url"] == api_url]
        if existing:
            self.api_configs["saved_configs"].remove(existing[0])
        
        self.api_configs["saved_configs"].append(config)
        self.api_configs["last_used"] = api_url
        self._save_api_configs()

    # ────────────────────────────────────────────────
    # 3. วิเคราะห์และจัดระเบียบข้อมูลจาก API
    # ────────────────────────────────────────────────
    def analyze_api_data(self, api_data: any) -> Dict:
        """วิเคราะห์โครงสร้างข้อมูลจาก API เพื่อเข้าใจเนื้อหา"""
        analysis = {
            "is_json": isinstance(api_data, (dict, list)),
            "structure": None,
            "fields": [],
            "item_count": None,
            "summary": None
        }

        if not analysis["is_json"]:
            analysis["summary"] = "ข้อมูลไม่ใช่รูปแบบ JSON"
            return analysis

        # วิเคราะห์โครงสร้าง
        if isinstance(api_data, dict):
            analysis["structure"] = "object"
            analysis["fields"] = list(api_data.keys())
            analysis["item_count"] = len(api_data)
            analysis["summary"] = f"ข้อมูลเป็นวัตถุ มี {len(api_data)} ฟิลด์"
        elif isinstance(api_data, list):
            analysis["structure"] = "list"
            analysis["item_count"] = len(api_data)
            if len(api_data) > 0 and isinstance(api_data[0], dict):
                analysis["fields"] = list(api_data[0].keys())
                analysis["summary"] = f"ข้อมูลเป็นรายการ มี {len(api_data)} รายการ แต่ละรายการมี {len(api_data[0])} ฟิลด์"
            else:
                analysis["summary"] = f"ข้อมูลเป็นรายการ มี {len(api_data)} รายการ"

        return analysis

    # ────────────────────────────────────────────────
    # 4. นำข้อมูลจาก API ไปบันทึกในฐานข้อมูล VIDER
    # ────────────────────────────────────────────────
    def save_api_data_to_db(self, api_data: any, db_session, table_name: str = "api_data") -> bool:
        """บันทึกข้อมูลจาก API เข้าฐานข้อมูลของ VIDER"""
        try:
            # สร้างตารางถ้ายังไม่มี (ตามโครงสร้างข้อมูล)
            from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData

            metadata = MetaData()
            fields = [
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("raw_data", Text),
                Column("saved_at", DateTime, default=datetime.utcnow)
            ]

            # เพิ่มฟิลด์จากข้อมูล API ถ้าเป็น JSON
            if isinstance(api_data, (dict, list)):
                if isinstance(api_data, list) and len(api_data) > 0 and isinstance(api_data[0], dict):
                    sample = api_data[0]
                elif isinstance(api_data, dict):
                    sample = api_data
                else:
                    sample = {}

                for key in sample.keys():
                    fields.append(Column(f"field_{key}", String(255), nullable=True))

            # สร้างตาราง
            api_table = Table(table_name, metadata, *fields)
            metadata.create_all(db_session.bind)

            # บันทึกข้อมูล
            raw_data = json.dumps(api_data, ensure_ascii=False)
            data_to_save = {"raw_data": raw_data}

            # เพิ่มข้อมูลลงในฟิลด์แยก
            if isinstance(api_data, dict):
                for key, value in api_data.items():
                    data_to_save[f"field_{key}"] = str(value)[:255]
                db_session.execute(api_table.insert().values(data_to_save))
            elif isinstance(api_data, list):
                for item in api_data:
                    if isinstance(item, dict):
                        item_data = {"raw_data": raw_data}
                        for key, value in item.items():
                            item_data[f"field_{key}"] = str(value)[:255]
                        db_session.execute(api_table.insert().values(item_data))

            db_session.commit()
            return True

        except Exception as e:
            db_session.rollback()
            self._log(f"ผิดพลาดในการบันทึกข้อมูล API: {str(e)}", "ERROR")
            return False

    # ────────────────────────────────────────────────
    # 5. ดึง API ที่เคยใช้ไว้
    # ────────────────────────────────────────────────
    def get_saved_apis(self) -> List[Dict]:
        """แสดงรายการ API ที่เคยใช้ไว้"""
        return self.api_configs["saved_configs"]

    def _log(self, message: str, level: str = "INFO"):
        """บันทึกเหตุการณ์การทำงาน API"""
        log_file = self.data_dir / "api_logs.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())

# ────────────────────────────────────────────────
# ตัวอย่างการใช้งานจริง
# ────────────────────────────────────────────────
if __name__ == "__main__":
    api_manager = ViderAPIManager()

    # ทดสอบดึงข้อมูลจาก API ตัวอย่าง (jsonplaceholder.typicode.com)
    print("\n=== ทดสอบดึงข้อมูลจาก API ===")
    test_api = "https://jsonplaceholder.typicode.com/posts/1"
    fetch_result = api_manager.fetch_from_api(test_api)

    if fetch_result["success"]:
        print("✅ ดึงข้อมูลสำเร็จ")
        print("ข้อมูลที่ได้:", json.dumps(fetch_result["data"], indent=2, ensure_ascii=False))

        # ทดสอบวิเคราะห์ข้อมูล
        print("\n=== ทดสอบวิเคราะห์ข้อมูล ===")
        analyze_result = api_manager.analyze_api_data(fetch_result["data"])
        print("ผลวิเคราะห์:", json.dumps(analyze_result, indent=2, ensure_ascii=False))

        # ทดสอบบันทึกข้อมูล (ต้องมีฐานข้อมูลของ VIDER พร้อม)
        print("\n=== ทดสอบบันทึกข้อมูล ===")
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            engine = create_engine("sqlite:///vider_environment/data/vider_agent_db.db")
            Session = sessionmaker(bind=engine)
            db_session = Session()
            save_ok = api_manager.save_api_data_to_db(fetch_result["data"], db_session)
            print("✅ บันทึกข้อมูลสำเร็จ" if save_ok else "❌ บันทึกไม่สำเร็จ")
        except Exception as e:
            print(f"❌ ไม่สามารถเชื่อมต่อฐานข้อมูล: {str(e)}")
else:
    print("❌ ดึงข้อมูลไม่สำเร็จ: " + fetch_result["error"])
0
