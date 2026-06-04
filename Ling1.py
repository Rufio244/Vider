{
  "database_name": "vider_external_db",
  "version": "1.0.0",
  "security_standard": "AES-256 Encryption",
  "tables": {
    "account_data": {
      "description": "จัดเก็บข้อมูลบัญชีและรหัสที่เข้ารหัส",
      "fields": ["id", "ref_code", "service_name", "username", "encrypted_password", "created_at"]
    },
    "accounting_transactions": {
      "description": "บันทึกรายการการเงินและบัญชี",
      "fields": ["transaction_id", "transaction_date", "description", "amount", "debit_credit"]
    }
  }
}
