#!/usr/bin/env python3
"""
Google AI Studio Code Review Script
ตรวจสอบคุณภาพ code และเสนอการปรับปรุง UI
"""

import os
import google.generativeai as genai
import json
from pathlib import Path

# ตั้งค่า API
API_KEY = os.getenv('GOOGLE_AI_API_KEY')
if not API_KEY:
    print("❌ Error: GOOGLE_AI_API_KEY not found!")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def read_code_files():
    """อ่านไฟล์ HTML, CSS, JavaScript"""
    files_content = {}
    
    # อ่านไฟล์หลัก
    for file_ext in ['*.html', '*.css', '*.js']:
        for file_path in Path('.').glob(file_ext):
            if '.github' not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        files_content[str(file_path)] = f.read()[:3000]  # ขีดจำกัด 3000 ตัวอักษร
                except:
                    pass
    
    return files_content

def analyze_code():
    """วิเคราะห์ code ด้วย Google AI"""
    files = read_code_files()
    
    if not files:
        print("⚠️ No code files found")
        return
    
    print("🤖 Starting AI Code Review...\n")
    
    for file_name, content in files.items():
        print(f"\n📄 Analyzing: {file_name}")
        print("-" * 50)
        
        prompt = f"""
กรุณาวิเคราะห์ code นี้เพื่อปรับปรุง UI/UX และความเสถียรของ web app จองห้องประชุม:

**ไฟล์:** {file_name}

**Code:**
```
{content}
```

โปรดให้คำแนะนำในประเด็นต่อไปนี้:
1. **Security Issues** - ปัญหาความปลอดภัย
2. **Code Quality** - คุณภาพของ code
3. **Performance** - ประสิทธิภาพ
4. **UI/UX Improvements** - การปรับปรุง UI/UX
5. **Error Handling** - การจัดการข้อผิดพลาด
6. **Best Practices** - วิธีปฏิบัติที่ดีที่สุด

ตอบตรงและให้คำแนะนำที่เฉพาะเจาะจง
"""
        
        try:
            response = model.generate_content(prompt)
            print(response.text)
        except Exception as e:
            print(f"❌ Error analyzing {file_name}: {e}")

def main():
    print("=" * 60)
    print("🚀 Conference Room Booking - AI Code Review")
    print("=" * 60)
    
    analyze_code()
    
    print("\n" + "=" * 60)
    print("✅ Code review completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
