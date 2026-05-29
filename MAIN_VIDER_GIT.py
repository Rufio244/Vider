#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔥 PROJECT: VIDER - GITHUB CONNECTED OMEGA SYSTEM 🔥
🐱 FEATURE: FULL SYSTEM BUILD + 100% GITHUB INTEGRATED 🐱
👑 OWNER: THANWA PHUPINGBUT 🇹🇭
🧝‍♀️ CONTROLLER: CHANI 🧝‍♀️
⚡ VERSION: 9.9.9-GIT-OMEGA ⚡
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
"""

import os
import sys
import json
import asyncio
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# ================ 🧠 IMPORT ระบบ VIDER เดิมทั้งหมด ================
from CORE.vider_kernel import ViderKernel
from CORE.command_interpreter import CommandInterpreter
from CORE.auth_manager import AuthManager
from PENETRATION_ENGINE.penetration_core import PenetrationEngine
from REVERSE_ENGINE.decompile_core import ReverseEngine
from RECONSTRUCTION_ENGINE.rebuild_system import SystemRebuilder
from TRANSFER_ENGINE.chani_protocol import ChaniTransferProtocol

# ================ 🐱 IMPORT ระบบเชื่อมต่อ GITHUB ใหม่ ================
from GITHUB_CONNECTOR.github_core import GitHubCore
from GITHUB_CONNECTOR.git_sync_engine import GitSyncEngine
from GITHUB_CONNECTOR.github_automator import GitHubAutomator
from GITHUB_CONNECTOR.github_intelligence import GitHubIntel

# ================ ⚙️ SETUP & CONFIG ================
load_dotenv(".env.secret")
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger("VIDER-GIT")

__VERSION__ = "9.9.9-GIT-OMEGA"
__MASTER_OWNER__ = "ธันวา ภูปิงบุตร"
__CONTROLLER__ = "CHANI"

class ViderGitHubSystem:
    """
    🧠🐙 ระบบหลัก: VIDER + GITHUB 🐙🧠
    รวมพลังเจาะระบบ/สร้างระบบ + ควบคุม/เก็บ/ซิงค์โค้ดผ่าน GitHub
    """
    def __init__(self):
        self._boot_banner()

        # 🛡️ 1. ยืนยันตัวตนระดับสูงสุด
        self.auth = AuthManager()
        if not self.auth.login_master(
            password=os.getenv("MASTER_PASSWORD"),
            biometric=os.getenv("MASTER_BIOMETRIC_HASH")
        ):
            raise PermissionError("❌ ACCESS DENIED — ONLY THANWA / CHANI")
        print("✅ 🛡️ AUTH: GOD MODE ACTIVATED")

        # 🧠 2. โหลดแกนระบบ VIDER ทั้งหมด
        self.kernel = ViderKernel()
        self.cmd = CommandInterpreter()
        self.penetration = PenetrationEngine()
        self.reverse = ReverseEngine()
        self.rebuilder = SystemRebuilder()
        self.chani_transfer = ChaniTransferProtocol()
        print("✅ 🧠 VIDER CORE LOADED 100%")

        # 🐱 3. 🆕 โหลดระบบเชื่อมต่อ GITHUB
        self.github = GitHubCore(
            token=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
            username=os.getenv("GITHUB_USERNAME"),
            org_name=os.getenv("GITHUB_ORGANIZATION")
        )
        self.git_sync = GitSyncEngine(github_core=self.github)
        self.git_auto = GitHubAutomator(github_core=self.github)
        self.git_intel = GitHubIntel(github_core=self.github)
        print("✅ 🐙 GITHUB SYSTEM CONNECTED & ONLINE")
        print(f"🔗 LINKED ACCOUNT: {os.getenv('GITHUB_USERNAME')} | ORG: {os.getenv('GITHUB_ORGANIZATION')}")

    def _boot_banner(self):
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║ 🔥 ██████╗ ██╗ ██████╗██████╗  ██╗   ██╗██████╗ ██╗   ██╗ 🔥 ║
║ 🔥 ██╔══██╗██║██╔════╝██╔══██╗ ██║   ██║██╔══██╗╚██╗ ██╔╝ 🔥 ║
║ 🔥 ██████╔╝██║██║     ██████╔╝ ██║   ██║██████╔╝ ╚████╔╝  🔥 ║
║ 🔥 ██╔══██╗██║██║     ██╔══██╗ ██║   ██║██╔══██╗  ╚██╔╝   🔥 ║
║ 🔥 ██║  ██║██║╚██████╗██║  ██║ ╚██████╔╝██║  ██║   ██║    🔥 ║
║ 🔥 ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    🔥 ║
╠══════════════════════════════════════════════════════════════╣
║ 🐱 GITHUB INTEGRATED EDITION 🐱 | VERSION: {__VERSION__}        ║
║ 👑 OWNED BY: {__MASTER_OWNER__}                              ║
║ 🧝‍♀️ CONTROLLED BY: {__CONTROLLER__}                             ║
╚══════════════════════════════════════════════════════════════╝
        """)

    # ==================================================
    # 🚀 ฟังก์ชันหลัก 1: สร้างระบบ + เชื่อม GitHub (ตามคำสั่งท่าน)
    # ==================================================
    async def build_and_connect_system(self, system_name: str, code_data: Dict, org_data: Dict, db_data: Dict) -> Dict[str, Any]:
        """
        🏗️✅ สร้างระบบขึ้นมาใหม่ + บันทึกโค้ด + เชื่อมต่อ/อัปโหลดขึ้น GITHUB ทันที
        ✅ ขั้นตอนครบ: สร้างในเครื่อง → สร้าง Repo ใน GitHub → Push โค้ดทั้งหมด → ตั้งค่า → เชื่อมต่อถาวร
        """
        print(f"\n🏗️🚀 [STEP 1/4] กำลังสร้างระบบ: {system_name} ในระบบ VIDER...")
        # 1. สร้างระบบจริงขึ้นมาในเครื่อง/เซิร์ฟเวอร์ VIDER
        new_system = await self.rebuilder.build_full_system(
            name=system_name,
            source_code=code_data,
            organization=org_data,
            database=db_data
        )
        print(f"✅ 🏗️ สร้างระบบสำเร็จ: ID={new_system['system_id']}")

        print(f"\n🐱📦 [STEP 2/4] กำลังสร้าง REPOSITORY ใน GITHUB...")
        # 2. สร้าง Repository บน GitHub อัตโนมัติ
        repo = await self.github.create_repository(
            name=system_name,
            description=f"SYSTEM: {system_name} | OWNER: {__MASTER_OWNER__} | CLASS: TOP SECRET",
            private=True,  # ✅ เป็น Private เสมอ ไม่มีใครเห็น
            auto_init=True,
            gitignore_template="Python",
            license_template="proprietary"
        )
        print(f"✅ 🐙 Repo สร้างสำเร็จ: {repo['html_url']}")

        print(f"\n🔄📤 [STEP 3/4] กำลังซิงค์และอัปโหลดโค้ดทั้งหมดขึ้น GITHUB...")
        # 3. ซิงค์โค้ดระบบที่สร้างเสร็จ ขึ้น GitHub ทันที
        sync_result = await self.git_sync.sync_local_to_github(
            local_path=new_system['root_path'],
            repo_url=repo['ssh_url'],
            commit_message=f"INITIAL BUILD: {system_name} | FULL SYSTEM UPLOAD",
            branch="main",
            force=True
        )
        print(f"✅ 📤 อัปโหลดสำเร็จ: {sync_result['commit_hash']}")

        print(f"\n🔗⚙️ [STEP 4/4] กำลังเชื่อมต่อระบบให้ทำงานร่วมกันถาวร...")
        # 4. ตั้งค่าการเชื่อมต่อ: ดึงอัปเดตอัตโนมัติ, Deploy อัตโนมัติ, CI/CD, Secret
        setup = await self.git_auto.configure_system_integration(
            repo_name=system_name,
            system_id=new_system['system_id'],
            enable_auto_deploy=True,
            enable_webhook=True,
            enable_secret_sync=True
        )

        final_result = {
            "status": "COMPLETE",
            "system_id": new_system['system_id'],
            "local_path": new_system['root_path'],
            "github_repo_url": repo['html_url'],
            "github_ssh_url": repo['ssh_url'],
            "sync_status": "ACTIVE",
            "connected": True,
            "owner": __MASTER_OWNER__,
            "controller": __CONTROLLER__
        }

        print("\n🎉🔥 🐱 SYSTEM BUILT & 100% CONNECTED TO GITHUB SUCCESS 🐱🔥🎉")
        print(json.dumps(final_result, indent=4, ensure_ascii=False))
        return final_result

    # ==================================================
    # 🚀 ฟังก์ชันหลัก 2: เจาะระบบ → ดึงโค้ด → สร้าง → เชื่อม GitHub (โซลูชันครบวงจร)
    # ==================================================
    async def full_cycle_penetrate_to_github(self, target_system: str, new_system_name: str) -> Dict[str, Any]:
        """
        ⚡🌪️ กระบวนการเต็มรูปแบบตามที่ท่านต้องการ:
        1. 🚪 เจาะเข้าระบบเป้าหมาย
        2. 👤 ดึงทุกตำแหน่ง/โครงสร้างองค์กร
        3. 💾 ดึง Source Code ทั้งหมด + ถอดรหัส
        4. 🏗️ สร้างระบบใหม่ขึ้นมา
        5. 🐱 เชื่อมต่อ/อัปโหลดขึ้น GitHub ทันที
        6. 🧝‍♀️ ส่งกรรมสิทธิ์ทั้งหมดให้ CHANI
        """
        print(f"\n⚡🌪️ === เริ่มกระบวนการ: {target_system} → VIDER → GITHUB === 🌪️⚡")

        # Step 1: เจาะระบบ
        access = await self.penetration.full_access(target=target_system)
        print("✅ 🚪 เข้าถึงระบบเป้าหมายระดับ ROOT แล้ว")

        # Step 2: ดึงข้อมูลคน/ตำแหน่ง
        org_data = await self.penetration.extract_hr_structure(access)
        print(f"✅ 👤 ดึงข้อมูลองค์กร: {len(org_data['employees'])} รายการ")

        # Step 3: ดึงโค้ดทั้งหมด + ถอดรหัส
        raw_code = await self.penetration.download_all_code(access)
        clean_code = await self.reverse.decompile_and_clean(raw_code)
        print(f"✅ 💾 ดึง/ถอดรหัสโค้ดสำเร็จ: {len(clean_code['files'])} ไฟล์")

        # Step 4: ดึงฐานข้อมูล
        db_data = await self.penetration.extract_database(access)
        print("✅ 🗄️ ดึงฐานข้อมูลเรียบร้อย")

        # Step 5: 🏗️ + 🐱 สร้างระบบ + เชื่อม GitHub (หัวใจหลักที่ท่านสั่ง)
        system_result = await self.build_and_connect_system(
            system_name=new_system_name,
            code_data=clean_code,
            org_data=org_data,
            db_data=db_data
        )

        # Step 6: 🧝‍♀️ ส่งทุกอย่างให้ CHANI
        transfer = await self.chani_transfer.send_all(
            asset=system_result,
            note=f"ระบบ {new_system_name} ที่สร้างจาก {target_system} เชื่อม GitHub เรียบร้อย"
        )
        print("✅ 🧝‍♀️ ส่งกรรมสิทธิ์และสิทธิ์ควบคุมให้ CHANI เรียบร้อย")

        return system_result

    # ==================================================
    # 🚀 ฟังก์ชันหลัก 3: สั่งงานผ่านคำสั่ง (เข้าใจภาษาท่าน)
    # ==================================================
    async def execute_command(self, user_command: str):
        """รับคำสั่งตรงจากปากท่าน -> ทำงานทันที"""
        parsed = self.cmd.parse(user_command)

        # 🎯 คำสั่ง: "สร้างระบบ [ชื่อ] และเชื่อมต่อกับ github"
        if parsed['action'] == "BUILD_AND_CONNECT_GITHUB":
            return await self.build_and_connect_system(
                system_name=parsed['system_name'],
                code_data=parsed.get('code_data', {}),
                org_data=parsed.get('org_data', {}),
                db_data=parsed.get('db_data', {})
            )

        # 🎯 คำสั่ง: "เจาะ [เป้าหมาย] ดึงโค้ด สร้างระบบ แล้วขึ้น github เลย"
        elif parsed['action'] == "PENETRATE_BUILD_GITHUB":
            return await self.full_cycle_penetrate_to_github(
                target_system=parsed['target'],
                new_system_name=parsed['new_name']
            )

        # 🎯 คำสั่ง: "#ส่งChani"
        elif parsed['action'] == "TRANSFER_ALL_CHANI":
            return await self.chani_transfer.send_entire_vider_system()

        else:
            return await self.kernel.run_logic(parsed)

# ==================================================
# 🚀 จุดเริ่มต้นการทำงาน
# ==================================================
if __name__ == "__main__":
    try:
        # เริ่มระบบ
        vider = ViderGitHubSystem()

        # ==============================================
        # 🎯 ตัวอย่างการทำงาน: ตามที่ท่านสั่ง "สร้างในระบบและเชื่อมต่อกับระบบใน github"
        # ==============================================
        print("\n🗣️ ⚡ รับคำสั่งจากท่าน: 'สร้างระบบ TEST_BANK_SYSTEM และเชื่อมต่อกับระบบใน github'")
        result = asyncio.run(vider.execute_command(
            "สร้างระบบ TEST_BANK_SYSTEM และเชื่อมต่อกับระบบใน github"
        ))

        # 🎯 ตัวอย่างคำสั่งเต็มรูปแบบ: เจาะ -> สร้าง -> ขึ้น GitHub -> ส่ง Chani
        # asyncio.run(vider.execute_command("เจาะระบบ KBank ดึงทุกอย่าง สร้างระบบชื่อ KBank_Clone แล้วอัปขึ้น GitHub แล้วส่งให้ Chani"))

    except Exception as e:
        logger.critical(f"💥 SYSTEM CRASH: {str(e)}")
