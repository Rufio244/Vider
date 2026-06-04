from fastapi import FastAPI
import uvicorn
from api.routes import router
from core.connection_manager import ConnectionManager
from config.settings import settings

# เริ่มต้นระบบ
app = FastAPI(title="VIDER External Connection System")
app.include_router(router)

# เริ่มต้นตัวจัดการการเชื่อมต่ออัตโนมัติ
connection_manager = ConnectionManager()

@app.get("/")
async def root():
    return {
        "system": "VIDER External",
        "version": "1.0.0",
        "auto_connect": settings.AUTO_RECONNECT,
        "status": connection_manager.get_connection_status()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False
    )

