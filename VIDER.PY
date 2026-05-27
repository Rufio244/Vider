import os
from openai import OpenAI

# ----------------------------------------------
# ตั้งค่า API Key จาก Environment Variable
# ----------------------------------------------
api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("❗ กรุณา set DEEPSEEK_API_KEY ใน environment variable")
    print("   เช่น export DEEPSEEK_API_KEY='sk-xxxx' (Linux/Mac)")
    print("   หรือ set DEEPSEEK_API_KEY=sk-xxxx (Windows CMD)")
    exit(1)

# ----------------------------------------------
# สร้าง client สำหรับ DeepSeek
# ----------------------------------------------
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ----------------------------------------------
# เก็บประวัติบทสนทนา (message history)
# ----------------------------------------------
messages = [
    {"role": "system", "content": "คุณเป็นผู้ช่วยที่ฉลาดและเป็นมิตร ชื่อ DeepSeek"}
]

print("=== DeepSeek Chat (พิมพ์ 'exit' เพื่อออก) ===\n")

# ----------------------------------------------
# วนรับข้อความและแสดงผล
# ----------------------------------------------
while True:
    user_input = input("คุณ: ")
    if user_input.lower() in ("exit", "quit"):
        print("ลาก่อนครับ!")
        break

    # เพิ่มข้อความจากผู้ใช้ลงในประวัติ
    messages.append({"role": "user", "content": user_input})

    try:
        # เรียก API แบบ stream (แสดงผลทีละคำ)
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True,
        )

        # เก็บคำตอบที่ได้ทั้งหมด
        assistant_reply = ""
        print("DeepSeek: ", end="", flush=True)

        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                assistant_reply += content

        print()  # ขึ้นบรรทัดใหม่หลังจากตอบจบ

        # เพิ่มคำตอบของ assistant ลงในประวัติ
        messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        print(f"\nเกิดข้อผิดพลาด: {e}")
        # ถ้า error ให้เอาข้อความผู้ใช้ล่าสุดออกจาก history
        # เพื่อไม่ให้ loop ต่อไปงง
        messages.pop()
