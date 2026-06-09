import hashlib
import secrets
from datetime import datetime
from typing import Dict

class VIDERChat:
    def __init__(self):
        self.name = "VIDER Chat"
        self.level = "10% พื้นฐาน"
        self.enc_key = secrets.token_hex(16)
        self.sessions: Dict[str, list] = []
        self.knowledge = {
            "มะละกอ": {
                "ชื่ออื่น": "ลูกทอง, ลูกน้ำเต้า",
                "ถิ่นกำเนิด": "อเมริกากลาง",
                "ลักษณะ": "ต้นล้มลุก ลำต้นกลวง ใบใหญ่รูปฝ่ามือ",
                "การปลูก": "ชอบแดดจัด ดินระบายน้ำดี ขยายพันธุ์เมล็ด",
                "ประโยชน์": "กินผลสุก ต้มแกง ทำน้ำ ใบช่วยย่อย",
                "คุณค่า": "วิตามิน A, C, ไฟเบอร์, แคลเซียม",
                "ศัตรู": "โรคเน่าเลี้ยง, แมลงหวี่ขาว",
                "วัฒนธรรม": "ถือเป็นไม้มงคลในบางพื้นที่"
            }
        }

    def _encrypt(self, text: str) -> str:
        return hashlib.sha256(f"{text}{self.enc_key}".encode()).hexdigest()

    def chat(self, message: str, session_id: str = None) -> Dict:
        message = message.strip()
        if not session_id:
            session_id = f"CHAT_{secrets.token_hex(8)}"

        resp = self._get_response(message.lower())
        self.sessions.append({
            "time": datetime.now().isoformat(),
            "user": self._encrypt(message),
            "bot": self._encrypt(resp)
        })
        return {"success": True, "session_id": session_id, "response": resp}

    def _get_response(self, msg: str) -> str:
        if "มะละกอ" in msg:
            d = self.knowledge["มะละกอ"]
            return f"""🍈 ข้อมูลมะละกอ (ครบ 8 ด้าน)
• ชื่ออื่น: {d['ชื่ออื่น']}
• ถิ่นกำเนิด: {d['ถิ่นกำเนิด']}
• ลักษณะ: {d['ลักษณะ']}
• การปลูก: {d['การปลูก']}
• ประโยชน์: {d['ประโยชน์']}
• คุณค่าอาหาร: {d['คุณค่า']}
• ศัตรูพืช: {d['ศัตรู']}
• วัฒนธรรม: {d['วัฒนธรรม']}"""

        if "โค้ด" in msg or "python" in msg:
            return """ตัวอย่างโค้ดพื้นฐาน:
```python
name = input("ชื่อ: ")
print("สวัสดี", name)
