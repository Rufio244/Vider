# vider_value_optimizer.py - โมดูลวิเคราะห์ความคุ้มค่าและเพิ่มประโยชน์
import json
from datetime import datetime
from pathlib import Path

class ViderValueOptimizer:
    def __init__(self):
        self.data_dir = Path("./vider_environment/knowledge/")
        self.data_dir.mkdir(exist_ok=True)
        self.related_features_file = self.data_dir / "related_features.json"
        self.best_practices_file = self.data_dir / "best_practices.json"
        self._load_knowledge()
        print("💡 โมดูลเพิ่มความคุ้มค่าพร้อมทำงาน - ได้มากกว่าที่ขอ")

    def _load_knowledge(self):
        """โหลดฐานข้อมูลสิ่งที่ควรมีเพิ่มและวิธีทำให้ดีขึ้น"""
        # ข้อมูลพื้นฐาน: สิ่งที่มักใช้ร่วมกัน (เหมือนของแถมที่จำเป็น)
        default_related = {
            "user_system": {
                "name": "ระบบสมาชิก/ผู้ใช้งาน",
                "always_add": ["การเข้ารหัสรหัสผ่าน", "ตรวจสอบอีเมล", "ลืมรหัสผ่าน", "บันทึกเวลาเข้าใช้งาน", "สิทธิ์ผู้ใช้"],
                "optional_add": ["รูปโปรไฟล์", "การยืนยันตัวตน 2 ชั้น", "ประวัติการใช้งาน"]
            },
            "web_shop": {
                "name": "ร้านค้าออนไลน์",
                "always_add": ["ตะกร้าสินค้า", "การคำนวณราคารวม", "หน้าแสดงรายละเอียดสินค้า", "การจัดการสต็อก"],
                "optional_add": ["ระบบค้นหา", "จัดเรียงสินค้า", "ส่วนลด", "การแจ้งเตือน"]
            },
            "database": {
                "name": "ระบบจัดเก็บข้อมูล",
                "always_add": ["การสำรองข้อมูล", "การป้องกันข้อมูลซ้ำ", "การค้นหาและเรียงลำดับ", "การตรวจสอบความถูกต้อง"],
                "optional_add": ["การส่งออกข้อมูล", "การนำเข้าข้อมูล", "รายงานสรุป"]
            },
            "web_interface": {
                "name": "หน้าเว็บแสดงผล",
                "always_add": ["รองรับมือถือ", "เมนูนำทาง", "หน้าแสดงผลผิดพลาด", "ความปลอดภัยเบื้องต้น"],
                "optional_add": ["การออกแบบสวยงาม", "การโหลดเร็ว", "รองรับหลายภาษา"]
            }
        }

        # วิธีปฏิบัติที่ดี เพื่อให้ได้งานที่มีคุณภาพสูง
        default_practices = {
            "security": ["เข้ารหัสข้อมูลสำคัญ", "ป้องกันการเข้าถึงโดยไม่ได้รับอนุญาต", "ตรวจสอบข้อมูลที่รับเข้ามา"],
            "performance": ["จัดระเบียบโค้ดให้อ่านง่าย", "ใช้ทรัพยากรอย่างมีประสิทธิภาพ", "เตรียมรองรับการขยายงานในอนาคต"],
            "usability": ["ใช้งานง่าย ไม่ซับซ้อนเกินไป", "มีข้อความแจ้งเตือนชัดเจน", "ทำงานได้เสถียร"]
        }

        # โหลดหรือสร้างใหม่
        if self.related_features_file.exists():
            with open(self.related_features_file, "r", encoding="utf-8") as f:
                self.related_features = json.load(f)
        else:
            self.related_features = default_related
            self._save_related()

        if self.best_practices_file.exists():
            with open(self.best_practices_file, "r", encoding="utf-8") as f:
                self.practices = json.load(f)
        else:
            self.practices = default_practices
            self._save_practices()

    def _save_related(self):
        with open(self.related_features_file, "w", encoding="utf-8") as f:
            json.dump(self.related_features, f, ensure_ascii=False, indent=2)

    def _save_practices(self):
        with open(self.best_practices_file, "w", encoding="utf-8") as f:
            json.dump(self.practices, f, ensure_ascii=False, indent=2)

    # ────────────────────────────────────────────────
    # วิเคราะห์และเพิ่มสิ่งที่มีประโยชน์เพิ่มเติม
    # ────────────────────────────────────────────────
    def analyze_and_enrich(self, analysis_result):
        """รับผลวิเคราะห์คำสั่ง แล้วเพิ่มสิ่งที่ควรมีเพิ่มเติมให้คุ้มค่าที่สุด"""
        if not analysis_result or "error" in analysis_result:
            return analysis_result, {}

        original_needs = analysis_result.get("requirements", [])
        target = analysis_result.get("target", "").lower()
        added_features = {"must_add": [], "good_to_add": [], "practices": []}

        # ตรวจสอบว่าคำสั่งเกี่ยวข้องกับหมวดหมู่ไหนบ้าง
        matched_categories = []
        for cat_key, cat_info in self.related_features.items():
            keywords = cat_info["name"].lower().split()
            if any(kw in target for kw in keywords):
                matched_categories.append(cat_info)

        # เพิ่มสิ่งที่จำเป็นแต่มักถูกลืม (เหมือนของแถมที่ต้องมี)
        for cat in matched_categories:
            for feature in cat["always_add"]:
                if feature not in original_needs and feature not in added_features["must_add"]:
                    added_features["must_add"].append(feature)

        # เพิ่มสิ่งที่น่าสนใจเพิ่มเติม (เหมือนของแถมเสริม)
        for cat in matched_categories:
            for feature in cat["optional_add"]:
                if feature not in original_needs and feature not in added_features["good_to_add"]:
                    added_features["good_to_add"].append(feature)

        # เพิ่มวิธีปฏิบัติที่ดีเพื่อให้งานมีคุณภาพ
        for practice_group, items in self.practices.items():
            for item in items:
                added_features["practices"].append(item)

        # รวมทุกอย่างกลับเข้าไปในผลวิเคราะห์
        enriched = analysis_result.copy()
        enriched["requirements"].extend(added_features["must_add"])
        enriched["added_value"] = added_features
        enriched["summary_added"] = f"เพิ่มสิ่งที่จำเป็น {len(added_features['must_add'])} อย่าง และสิ่งที่น่าสนใจอีก {len(added_features['good_to_add'])} อย่าง"

        return enriched, added_features

    # ────────────────────────────────────────────────
    # สร้างรายงานความคุ้มค่าให้ผู้ใช้เห็น
    # ────────────────────────────────────────────────
    def get_value_report(self, added_features):
        """สร้างข้อความอธิบายสิ่งที่ได้เพิ่มเติมให้เข้าใจง่าย"""
        report = "\n🎁 **สิ่งที่ได้รับเพิ่มเติมโดยไม่ต้องสั่งเพิ่ม:**\n"
        
        if added_features["must_add"]:
            report += "\n✅ **สิ่งที่จำเป็นต้องมีเพื่อให้ทำงานได้สมบูรณ์:**\n"
            for idx, item in enumerate(added_features["must_add"], 1):
                report += f"  {idx}. {item}\n"

        if added_features["good_to_add"]:
            report += "\n✨ **สิ่งเสริมเพิ่มความสะดวกและคุ้มค่า:**\n"
            for idx, item in enumerate(added_features["good_to_add"], 1):
                report += f"  {idx}. {item}\n"

        if added_features["practices"]:
            report += "\n🛡️ **มาตรฐานความปลอดภัยและคุณภาพที่เพิ่มให้:**\n"
            report += "  → เข้ารหัสข้อมูล, ป้องกันข้อผิดพลาด, รองรับการใช้งานในอนาคต\n"

        report += "\n💡 **สรุป:** ได้งานที่สมบูรณ์ ใช้งานได้จริง และมีมาตรฐานครบถ้วนมากกว่าที่ขอครับ"
        return report

    # ────────────────────────────────────────────────
    # เพิ่มความรู้ใหม่ให้ระบบได้ตลอด
    # ────────────────────────────────────────────────
    def add_knowledge(self, category_name, must_have=None, optional=None):
        """เพิ่มหมวดหมู่ใหม่หรือสิ่งที่ควรมีเพิ่มเติม"""
        cat_key = category_name.lower().replace(" ", "_")
        if cat_key not in self.related_features:
            self.related_features[cat_key] = {
                "name": category_name,
                "always_add": must_have or [],
                "optional_add": optional or []
            }
        else:
            if must_have:
                self.related_features[cat_key]["always_add"].extend(must_have)
            if optional:
                self.related_features[cat_key]["optional_add"].extend(optional)
        
        self._save_related()
        return True
