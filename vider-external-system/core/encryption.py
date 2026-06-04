from cryptography.fernet import Fernet
from config.settings import settings
import base64

class EncryptionManager:
    def __init__(self):
        key = base64.urlsafe_b64encode(settings.ENCRYPTION_KEY.ljust(32)[:32].encode())
        self.cipher = Fernet(key)

    def encrypt_data(self, data: str) -> str:
        """เข้ารหัสข้อมูลก่อนจัดเก็บ"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """ถอดรหัสข้อมูลเมื่อต้องการใช้งาน"""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return ""

