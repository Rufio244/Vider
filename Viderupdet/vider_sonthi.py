# vider_sonthi.py - ระบบตรวจสอบและสร้างความสัมพันธ์ข้อมูล
import json
import math
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class ViderSonthi:
    def __init__(self):
        self.data_dir = Path("./vider_environment/sonthi_data/")
        self.data_dir.mkdir(exist_ok=True)
        self.relations_file = self.data_dir / "known_relations.json"
        self.patterns_file = self.data_dir / "relation_patterns.json"
        self.history_file = self.data_dir / "discovery_history.json"
        
        self._load_knowledge()
        print("🔗 VIDER SONTHI พร้อมทำงาน - วิเคราะห์และสร้างความสัมพันธ์ข้อมูล")

    def _load_knowledge(self):
        """โหลดฐานความรู้ความสัมพันธ์ที่มีอยู่"""
        # ความสัมพันธ์ที่ทราบแน่นอน
        if self.relations_file.exists():
            with open(self.relations_file, "r", encoding="utf-8") as f:
                self.known_relations = json.load(f)
        else:
            self.known_relations = {"exact": {}, "statistical": {}, "semantic": {}}
            self._save_relations()

        # รูปแบบความสัมพันธ์ทั่วไป
        if self.patterns_file.exists():
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                self.patterns = json.load(f)
        else:
            self.patterns = {
                "common_types": {
                    "owner_of": ["เจ้าของ", "เป็นของ", "ผู้ดูแล"],
                    "related_to": ["เกี่ยวข้องกับ", "เชื่อมโยงกับ", "สัมพันธ์กับ"],
                    "part_of": ["เป็นส่วนหนึ่งของ", "ประกอบด้วย", "ส่วนประกอบ"],
                    "causes": ["ทำให้เกิด", "ส่งผลให้", "เป็นสาเหตุของ"],
                    "belongs_to": ["อยู่ภายใต้", "สังกัด", "จัดอยู่ในกลุ่ม"],
                    "depends_on": ["อาศัย", "ต้องใช้", "ขึ้นอยู่กับ"]
                },
                "weight_factors": {
                    "same_source": 0.8,
                    "same_time": 0.7,
                    "same_group": 0.6,
                    "keyword_overlap": 0.5,
                    "common_pattern": 0.4
                }
            }
            self._save_patterns()

        # ประวัติการค้นพบ
        if self.history_file.exists():
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        else:
            self.history = {"discoveries": [], "stats": {"total_found": 0, "confirmed": 0}}
            self._save_history()

    def _save_relations(self):
        with open(self.relations_file, "w", encoding="utf-8") as f:
            json.dump(self.known_relations, f, ensure_ascii=False, indent=2)

    def _save_patterns(self):
        with open(self.patterns_file, "w", encoding="utf-8") as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)

    def _save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    # ────────────────────────────────────────────────
    # 1. ตรวจสอบความสัมพันธ์จากแหล่งข้อมูลที่มี
    # ────────────────────────────────────────────────
    def analyze_existing_data(self, data_sources: list) -> dict:
        """วิเคราะห์ความสัมพันธ์จากข้อมูลที่มีอยู่แล้ว"""
        result = {
            "found_relations": [],
            "possible_links": [],
            "summary": "",
            "confidence": 0.0
        }

        if not data_sources:
            result["summary"] = "ไม่มีแหล่งข้อมูลให้วิเคราะห์"
            return result

        # ดึงข้อมูลสำคัญ
        entities = self._extract_entities(data_sources)
        direct_relations = self._find_direct_relations(data_sources)
        indirect_relations = self._find_indirect_relations(entities)

        result["found_relations"] = direct_relations
        result["possible_links"] = indirect_relations
        result["summary"] = f"พบความสัมพันธ์ที่ชัดเจน {len(direct_relations)} รายการ และความเป็นไปได้เพิ่มเติม {len(indirect_relations)} รายการ"
        result["confidence"] = self._calculate_overall_confidence(direct_relations, indirect_relations)

        # บันทึกความสัมพันธ์ที่พบ
        self._add_to_known_relations(direct_relations)
        return result

    def _extract_entities(self, data_sources: list) -> dict:
        """สกัดหน่วยข้อมูลสำคัญจากแหล่งต่างๆ"""
        entities = defaultdict(list)
        for idx, source in enumerate(data_sources):
            if isinstance(source, dict):
                for key, value in source.items():
                    entities[key.lower()].append({
                        "value": value,
                        "source_id": idx,
                        "type": self._guess_type(key, value)
                    })
        return entities

    def _guess_type(self, key: str, value) -> str:
        """ประเภทของข้อมูลเพื่อช่วยวิเคราะห์"""
        key_lower = key.lower()
        if "ชื่อ" in key_lower or "name" in key_lower:
            return "name"
        elif "รหัส" in key_lower or "id" in key_lower:
            return "identifier"
        elif "วันที่" in key_lower or "date" in key_lower:
            return "time"
        elif "จำนวน" in key_lower or "ราคา" in key_lower:
            return "quantity"
        elif "หมวด" in key_lower or "กลุ่ม" in key_lower:
            return "category"
        return "general"

    def _find_direct_relations(self, data_sources: list) -> list:
        """ค้นหาความสัมพันธ์ที่ระบุไว้ชัดเจน"""
        relations = []
        source_count = len(data_sources)

        # ตรวจสอบรหัสเดียวกันข้ามแหล่ง
        if source_count >= 2:
            identifiers = defaultdict(list)
            for s_idx, source in enumerate(data_sources):
                for k, v in source.items():
                    if self._guess_type(k, v) == "identifier":
                        identifiers[str(v)].append({
                            "source": s_idx,
                            "field": k
                        })
            
            for val, matches in identifiers.items():
                if len(matches) >= 2:
                    relations.append({
                        "type": "direct_link",
                        "description": f"เชื่อมโยงด้วยรหัส/ค่าเดียวกัน: {val}",
                        "sources": [m["source"] for m in matches],
                        "confidence": 0.95,
                        "evidence": "มีค่าเหมือนกันในหลายแหล่ง"
                    })

        # ตรวจสอบคำสำคัญที่บ่งบอกความสัมพันธ์
        relation_keywords = sum(self.patterns["common_types"].values(), [])
        for source in data_sources:
            text_content = str(source).lower()
            for rel_type, keywords in self.patterns["common_types"].items():
                for kw in keywords:
                    if kw in text_content:
                        relations.append({
                            "type": rel_type,
                            "description": f"ระบุความสัมพันธ์: {kw}",
                            "sources": [data_sources.index(source)],
                            "confidence": 0.8,
                            "evidence": f"มีคำบ่งชี้: {kw}"
                        })
                        break

        return relations

    def _find_indirect_relations(self, entities: dict) -> list:
        """ค้นหาความสัมพันธ์ทางอ้อม/เป็นไปได้"""
        possible = []
        entity_list = list(entities.items())

        for i in range(len(entity_list)):
            for j in range(i+1, len(entity_list)):
                key1, items1 = entity_list[i]
                key2, items2 = entity_list[j]

                # คำนวณค่าความเป็นไปได้
                similarity_score = self._calculate_similarity(items1, items2)
                if similarity_score >= 0.4:  # เกณฑ์ยอมรับ
                    possible.append({
                        "type": "possible_association",
                        "entities": [key1, key2],
                        "similarity_score": round(similarity_score, 3),
                        "confidence": round(similarity_score, 2),
                        "reason": self._explain_similarity(items1, items2)
                    })

        return sorted(possible, key=lambda x: x["confidence"], reverse=True)

    def _calculate_similarity(self, items1: list, items2: list) -> float:
        """คำนวณระดับความคล้ายคลึงกัน"""
        score = 0.0
        factors = self.patterns["weight_factors"]

        # แหล่งเดียวกัน
        sources1 = {x["source_id"] for x in items1}
        sources2 = {x["source_id"] for x in items2}
        if sources1 & sources2:
            score += factors["same_source"]

        # ชนิดข้อมูลเดียวกัน
        types1 = {x["type"] for x in items1}
        types2 = {x["type"] for x in items2}
        if types1 & types2:
            score += factors["same_group"]

        # คำที่คล้ายกัน
        values1 = str([x["value"] for x in items1]).lower()
        values2 = str([x["value"] for x in items2]).lower()
        common_words = set(values1.split()) & set(values2.split())
        if common_words:
            score += min(factors["keyword_overlap"], len(common_words) * 0.1)

        # ค่าที่มีรูปแบบเดียวกัน
        if len(str(items1[0]["value"])) == len(str(items2[0]["value"])):
            score += factors["common_pattern"] * 0.5

        return min(score / sum(factors.values().values()), 1.0)

    def _explain_similarity(self, items1: list, items2: list) -> str:
        """อธิบายสาเหตุที่คิดว่ามีความสัมพันธ์"""
        reasons = []
        if {x["source_id"] for x in items1} & {x["source_id"] for x in items2}:
            reasons.append("อยู่ในแหล่งข้อมูลเดียวกัน")
        if {x["type"] for x in items1} & {x["type"] for x in items2}:
            reasons.append("เป็นข้อมูลประเภทเดียวกัน")
        common = set(str(items1[0]["value"]).split()) & set(str(items2[0]["value"]).split())
        if common:
            reasons.append(f"มีคำร่วมกัน: {', '.join(list(common)[:3])}")
        
        return " และ ".join(reasons) if reasons else "รูปแบบข้อมูลสอดคล้องกัน"

    # ────────────────────────────────────────────────
    # 2. สร้างความสัมพันธ์ใหม่ตามความเป็นไปได้
    # ────────────────────────────────────────────────
    def discover_new_relations(self, data_analysis: dict, min_confidence: float = 0.5) -> dict:
        """สร้างความสัมพันธ์ใหม่จากความเป็นไปได้ที่ตรวจพบ"""
        result = {
            "created_relations": [],
            "logic_used": [],
            "recommendations": [],
            "timestamp": datetime.utcnow().isoformat()
        }

        possible_links = data_analysis.get("possible_links", [])
        for link in possible_links:
            conf = link.get("confidence", 0)
            if conf >= min_confidence:
                # สร้างความสัมพันธ์ใหม่
                new_rel = {
                    "id": f"rel_{len(self.history['discoveries']) + 1}",
                    "type": "discovered",
                    "entities": link["entities"],
                    "confidence": conf,
                    "description": f"คาดว่า {link['entities'][0]} มีความสัมพันธ์กับ {link['entities'][1]}",
                    "reason": link["reason"],
                    "status": "proposed"
                }
                result["created_relations"].append(new_rel)
                result["logic_used"].append(f"ใช้เกณฑ์ความคล้ายคลึง {conf*100}%")

        # เพิ่มคำแนะนำ
        if result["created_relations"]:
            result["recommendations"] = [
                "ตรวจสอบความถูกต้องด้วยข้อมูลเพิ่มเติม",
                "สามารถนำไปใช้วิเคราะห์เชื่อมโยงต่อได้",
                "หากยืนยันแล้วจะเพิ่มน้ำหนักในการวิเคราะห์ครั้งต่อไป"
            ]
        else:
            result["recommendations"] = [
                "ความเป็นไปได้ต่ำเกินไป ลดเกณฑ์ความเชื่อมั่นหรือเพิ่มข้อมูล"
            ]

        # บันทึกการค้นพบ
        self._add_to_history(result)
        return result

    def confirm_relation(self, relation_id: str, is_correct: bool = True):
        """ยืนยันความสัมพันธ์เพื่อเรียนรู้ต่อไป"""
        for entry in self.history["discoveries"]:
            for rel in entry.get("created_relations", []):
                if rel.get("id") == relation_id:
                    rel["status"] = "confirmed" if is_correct else "rejected"
                    self.history["stats"]["confirmed"] += 1 if is_correct else 0
                    
                    if is_correct:
                        # เพิ่มเข้าฐานความรู้ที่แน่นอน
                        self.known_relations["statistical"][relation_id] = rel
                        self._save_relations()
                    
                    self._save_history()
                    return True
        return False

    # ────────────────────────────────────────────────
    # 3. รายงานผลสรุป
    # ────────────────────────────────────────────────
    def generate_report(self, analysis_result: dict, discovery_result: dict = None) -> str:
        """สร้างรายงานผลวิเคราะห์เข้าใจง่าย"""
        report = "\n📊 รายงาน VIDER SONTHI - ความสัมพันธ์ข้อมูล\n" + "="*50

        if analysis_result.get("found_relations"):
            report += "\n✅ **ความสัมพันธ์ที่ตรวจพบแน่นอน:**\n"
            for idx, rel in enumerate(analysis_result["found_relations"], 1):
                report += f"  {idx}. {rel['description']} (ความมั่นใจ: {rel['confidence']*100:.0f}%)\n"

        if discovery_result and discovery_result.get("created_relations"):
            report += "\n🔍 **ความสัมพันธ์ที่ค้นพบใหม่:**\n"
            for idx, rel in enumerate(discovery_result["created_relations"], 1):
                report += f"  {idx}. {rel['description']}\n"
                report += f"     เหตุผล: {rel['reason']}\n"
                report += f"     ความเป็นไปได้: {rel['confidence']*100:.0f}% | รหัสอ้างอิง: {rel['id']}\n"

        report += f"\n📈 **สรุป:** {analysis_result.get('summary', '')}\n"
        report += f"💡 **การใช้งาน:** สามารถยืนยันความถูกต้องด้วยคำสั่ง `confirm_relation('รหัส', True/False)`"
        return report

    def _add_to_known_relations(self, relations: list):
        """บันทึกความสัมพันธ์ที่ชัดเจน"""
        for rel in relations:
            key = f"{rel['type']}_{hash(str(rel['sources']))}"
            self.known_relations["exact"][key] = rel
        self._save_relations()

    def _add_to_history(self, discovery: dict):
        """บันทึกประวัติการค้นพบ"""
        discovery["timestamp"] = datetime.utcnow().isoformat()
        self.history["discoveries"].append(discovery)
        self.history["stats"]["total_found"] += len(discovery.get("created_relations", []))
        self._save_history()

    def _calculate_overall_confidence(self, direct: list, indirect: list) -> float:
        """คำนวณค่าความเชื่อมั่นโดยรวม"""
        if not direct and not indirect:
            return 0.0
        direct_score = sum(r.get("confidence", 0) for r in direct) / max(len(direct), 1) if direct else 0
        indirect_score = sum(r.get("confidence", 0) for r in indirect) / max(len(indirect), 1) if indirect else 0
        return round((direct_score * 0.7) + (indirect_score * 0.3), 2)
