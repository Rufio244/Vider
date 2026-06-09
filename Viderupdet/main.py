from vider_github_connector import vider_github
from vider_chat import vider_chat
from vider_login import vider_login

def main():
    print("="*50)
    print("  🚀 ระบบ VIDER พร้อมใช้งาน")
    print("  เชื่อมต่อ GitHub: Rufio244/Vider")
    print("="*50)
    print("\nคำสั่งพื้นฐาน:")
    print("1. ตั้งค่า GitHub: vider_github.set_token('โทเค็นของคุณ')")
    print("2. ดึงโค้ด: vider_github.clone_or_pull()")
    print("3. แชท: vider_chat.chat('มะละกอคืออะไร')")
    print("4. สมัคร: vider_login.register('อีเมล', 'รหัสผ่าน')")

if __name__ == "__main__":
    main()
