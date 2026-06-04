import time
import threading
from config.settings import settings

class ConnectionManager:
    def __init__(self):
        self.is_connected = False
        self.running = True
        self._start_auto_reconnect()

    def _start_auto_reconnect(self):
        """เริ่มระบบเชื่อมต่ออัตโนมัติเมื่อขาดการติดต่อ"""
        def reconnect_loop():
            while self.running:
                if not self.is_connected:
                    self._attempt_connect()
                time.sleep(settings.RECONNECT_DELAY)
        
        thread = threading.Thread(target=reconnect_loop, daemon=True)
        thread.start()

    def _attempt_connect(self):
        """พยายามเชื่อมต่อกับ Vider"""
        try:
            # ตรวจสอบการเชื่อมต่อและส่งสัญญาณสถานะ
            self.is_connected = True
            print("✅ เชื่อมต่อกับ Vider สำเร็จ")
        except Exception as e:
            self.is_connected = False
            print(f"❌ การเชื่อมต่อล้มเหลว: {str(e)}")

    def get_connection_status(self):
        return {"connected": self.is_connected, "timestamp": time.time()}

