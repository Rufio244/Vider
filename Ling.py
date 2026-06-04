-- =============================================
-- ฐานข้อมูลระบบ Vider - ฐานข้อมูลภายนอก
-- สถานะ: โครงสร้างสมบูรณ์ | ความปลอดภัย: มาตรฐานสากล
-- =============================================

CREATE DATABASE IF NOT EXISTS vider_external_db;
USE vider_external_db;

-- =============================================
-- 1. ตารางจัดเก็บข้อมูลบัญชีและรหัส (เข้ารหัสทั้งหมด)
-- =============================================
CREATE TABLE IF NOT EXISTS account_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ref_code VARCHAR(64) NOT NULL UNIQUE COMMENT 'รหัสอ้างอิงเฉพาะ',
    service_name VARCHAR(100) NOT NULL COMMENT 'ชื่อบริการ/แอปพลิเคชัน',
    service_type VARCHAR(50) NOT NULL COMMENT 'ประเภทบริการ',
    username VARCHAR(255) COMMENT 'ชื่อผู้ใช้/อีเมล',
    encrypted_password TEXT NOT NULL COMMENT 'รหัสผ่านที่เข้ารหัส (AES-256)',
    encrypted_otp TEXT COMMENT 'รหัส OTP ชั่วคราวที่เข้ารหัส',
    otp_expiry DATETIME COMMENT 'วันหมดอายุ OTP',
    notes TEXT COMMENT 'หมายเหตุทั่วไป',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'blocked') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ตารางจัดเก็บข้อมูลบัญชี';

-- =============================================
-- 2. ตารางระบบการเงินและบัญชี
-- =============================================
CREATE TABLE IF NOT EXISTS accounting_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE NOT NULL COMMENT 'วันที่ทำรายการ',
    reference_no VARCHAR(50) COMMENT 'เลขที่อ้างอิง',
    description TEXT NOT NULL COMMENT 'รายละเอียด',
    account_type VARCHAR(50) NOT NULL COMMENT 'ประเภทบัญชี',
    category VARCHAR(100) NOT NULL COMMENT 'หมวดหมู่',
    amount DECIMAL(15,2) NOT NULL COMMENT 'จำนวนเงิน',
    debit_credit ENUM('DEBIT', 'CREDIT') NOT NULL COMMENT 'เดบิต/เครดิต',
    balance DECIMAL(15,2) NOT NULL COMMENT 'ยอดคงเหลือ',
    recorded_by VARCHAR(100) COMMENT 'ผู้บันทึก',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ตารางบันทึกรายการบัญชี';

-- =============================================
-- 3. ตารางระบบจัดการการเชื่อมต่อและสิทธิ์
-- =============================================
CREATE TABLE IF NOT EXISTS connection_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    access_key VARCHAR(255) NOT NULL COMMENT 'รหัสคีย์เข้าถึง',
    action VARCHAR(100) NOT NULL COMMENT 'การกระทำ',
    ip_address VARCHAR(45) COMMENT 'ที่อยู่ IP',
    status ENUM('success', 'failed', 'denied') NOT NULL COMMENT 'สถานะ',
    request_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT COMMENT 'รายละเอียดเพิ่มเติม'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ตารางบันทึกการเชื่อมต่อ';

-- =============================================
-- 4. ตารางข้อมูลอ้างอิงระบบ
-- =============================================
CREATE TABLE IF NOT EXISTS system_settings (
    setting_key VARCHAR(100) PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description VARCHAR(255),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ตารางตั้งค่าระบบ';

-- เพิ่มค่าตั้งค่าเริ่มต้น
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('encryption_standard', 'AES-256', 'มาตรฐานการเข้ารหัสข้อมูล'),
('session_timeout', '300', 'เวลาหมดอายุการใช้งาน (วินาที)'),
('max_login_attempts', '5', 'จำนวนครั้งที่พยายามเข้าถึงผิดพลาดสูงสุด'),
('data_retention_days', '730', 'ระยะเวลาเก็บรักษาข้อมูล (วัน)');

-- =============================================
-- ดัชนีเพื่อประสิทธิภาพการทำงาน
-- =============================================
CREATE INDEX idx_ref_code ON account_data(ref_code);
CREATE INDEX idx_service_type ON account_data(service_type);
CREATE INDEX idx_transaction_date ON accounting_transactions(transaction_date);
CREATE INDEX idx_account_type ON accounting_transactions(account_type);
CREATE INDEX idx_log_time ON connection_logs(request_time);
