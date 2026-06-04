from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from core.auth import verify_access_key
from core.encryption import EncryptionManager
from database.db_handler import DatabaseHandler

router = APIRouter(prefix="/api/v1")
encryption = EncryptionManager()
db = DatabaseHandler()

class AccountRequest(BaseModel):
    ref_code: str
    access_key: str

@router.get("/status")
async def get_status():
    """ตรวจสอบสถานะการเชื่อมต่อ"""
    return {"status": "online", "service": "VIDER External System"}

@router.post("/get-account")
async def get_account_data(request: AccountRequest):
    """ดึงข้อมูลบัญชี (ถอดรหัสชั่วคราวเท่านั้น)"""
    if not verify_access_key(request.access_key):
        raise HTTPException(status_code=403, detail="สิทธิ์การเข้าถึงไม่ถูกต้อง")
    
    account = db.get_account_by_ref(request.ref_code)
    if not account:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูล")
    
    # ถอดรหัสเฉพาะตอนส่งกลับ และไม่เก็บไว้ในระบบอื่น
    decrypted_data = {
        "service_name": account.service_name,
        "username": account.username,
        "password": encryption.decrypt_data(account.encrypted_password),
        "otp": encryption.decrypt_data(account.encrypted_otp) if account.encrypted_otp else None,
        "expires_at": account.otp_expiry
    }
    
    return decrypted_data

