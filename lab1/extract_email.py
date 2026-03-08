import re
from collections import defaultdict
import os

# 1. กำหนดค่าคงที่และ Regular Expression
FILENAME = "sample_text.txt"
# Regex Pattern สำหรับ email ตามที่แนะนำ: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
# ใช้ r'' สำหรับ Raw string และกำหนด flag re.IGNORECASE เพื่อให้ค้นหาได้ทั้งตัวพิมพ์เล็กและใหญ่
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_emails_from_file(filename):
    """
    ค้นหาและสกัด email address จากไฟล์ข้อความโดยใช้ Regular Expression
    """
    print(f"กำลังค้นหา email จากไฟล์: {filename}")
    print("=" * 60)
    
    # ตัวแปรสำหรับเก็บผลลัพธ์
    found_emails = []  # เก็บ tuple (line_number, email_address) ทั้งหมด
    
    try:
        # เปิดและอ่านไฟล์
        with open(filename, 'r', encoding='utf-8') as file:
            # ใช้ enumerate เพื่อติดตามหมายเลขบรรทัด (เริ่มต้นที่ 1)
            for line_number, line in enumerate(file, 1):
                # ใช้ findall เพื่อค้นหา email ทั้งหมดในบรรทัด
                # EMAIL_REGEX.findall(line) จะคืนค่า list ของ string ที่ตรงกับ pattern
                emails_in_line = EMAIL_REGEX.findall(line)
                
                # ถ้าพบคู่ email ในบรรทัด
                for email in emails_in_line:
                    found_emails.append((line_number, email))
                    
    except FileNotFoundError:
        print(f"*** ERROR: ไม่พบไฟล์ '{filename}' กรุณาตรวจสอบว่ามีไฟล์อยู่ในไดเรกทอรีเดียวกันหรือไม่ ***")
        return

    # 2. ส่วนแสดงผลลัพธ์
    
    # 2.1 แสดงรายการ email ที่พบทั้งหมด
    print(f"\nพบ email ทั้งหมด {len(found_emails)} รายการ:\n")
    if found_emails:
        for line_num, email in found_emails:
            print(f"✓ บรรทัดที่ {line_num:3}: {email}")
    else:
        print("  (ไม่พบ email ที่ตรงตามรูปแบบ)")
        
    print("=" * 60)
    
    # 2.2 แสดง Email ที่ไม่ซ้ำกัน
    # ใช้ set เพื่อเก็บ email ที่ไม่ซ้ำกัน (เฉพาะ string email)
    unique_emails = sorted({email for line_num, email in found_emails})
    
    print(f"Email ที่ไม่ซ้ำกัน ({len(unique_emails)} รายการ):")
    for email in unique_emails:
        print(f"  - {email}")

    print("=" * 60)
    
    # 2.3 สถิติ Domain
    domain_counts = defaultdict(int)
    for email in unique_emails:
        # สกัดส่วน Domain: ค้นหาสัญลักษณ์ @ และนำข้อความที่อยู่หลัง @ มา
        domain = email.split('@')[-1]
        domain_counts[domain] += 1
        
    # จัดเรียง domain ตามชื่อ
    sorted_domains = sorted(domain_counts.items())

    print("สถิติ Domain:")
    for domain, count in sorted_domains:
        print(f"  - {domain}: {count} email(s)")
        
    print("=" * 60)
    
# ตรวจสอบว่ามีไฟล์ตัวอย่างหรือไม่ และทำการสร้างไฟล์หากยังไม่มี
if not os.path.exists(FILENAME):
    print(f"*** คำเตือน: ไฟล์ '{FILENAME}' ไม่พบ จะทำการสร้างไฟล์ตัวอย่างให้ ***")
    sample_content = """สวัสดีครับ ผมชื่อสมชาย
Email: somchai.test@example.com
โทร: 081-234-5678

ติดต่อทีมงานได้ที่:
- ฝ่ายขาย: sales@company.co.th
- ฝ่ายสนับสนุน: support@company.co.th
- CEO: ceo.admin@company.com

สำหรับข้อมูลเพิ่มเติมติดต่อ:
john.doe123@gmail.com หรือ jane_smith@university.ac.th

Email ที่ไม่ถูกต้อง: invalid@, @invalid.com, test@.com"""
    with open(FILENAME, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    print(f"*** สร้างไฟล์ '{FILENAME}' เรียบร้อยแล้ว ***\n")
    
# เรียกใช้ฟังก์ชันหลัก                                                             
extract_emails_from_file(FILENAME)