#!/usr/bin/env python3
"""
سكريبت إعداد وتثبيت شات بوت كلية العلوم
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """طباعة شعار التطبيق"""
    banner = """
    ╔══════════════════════════════════════╗
    ║        شات بوت كلية العلوم          ║
    ║     College Sciences Chatbot        ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """التحقق من إصدار Python"""
    print("🔍 التحقق من إصدار Python...")
    
    if sys.version_info < (3, 8):
        print("❌ خطأ: يتطلب Python 3.8 أو أحدث")
        print(f"الإصدار الحالي: {sys.version}")
        sys.exit(1)
    
    print(f"✅ إصدار Python مناسب: {sys.version.split()[0]}")

def create_virtual_environment():
    """إنشاء البيئة الافتراضية"""
    print("\n🔧 إنشاء البيئة الافتراضية...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  البيئة الافتراضية موجودة بالفعل")
        response = input("هل تريد إعادة إنشائها؟ (y/N): ")
        if response.lower() == 'y':
            print("🗑️  حذف البيئة الافتراضية القديمة...")
            shutil.rmtree(venv_path)
        else:
            print("⏭️  تخطي إنشاء البيئة الافتراضية")
            return
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ تم إنشاء البيئة الافتراضية بنجاح")
    except subprocess.CalledProcessError:
        print("❌ فشل في إنشاء البيئة الافتراضية")
        sys.exit(1)

def get_pip_command():
    """الحصول على أمر pip المناسب"""
    if os.name == 'nt':  # Windows
        return os.path.join("venv", "Scripts", "pip")
    else:  # Linux/Mac
        return os.path.join("venv", "bin", "pip")

def install_requirements():
    """تثبيت المكتبات المطلوبة"""
    print("\n📦 تثبيت المكتبات المطلوبة...")
    
    pip_cmd = get_pip_command()
    
    try:
        # ترقية pip أولاً
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # تثبيت المكتبات
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ تم تثبيت جميع المكتبات بنجاح")
    except subprocess.CalledProcessError:
        print("❌ فشل في تثبيت المكتبات")
        print("💡 جرب تشغيل الأمر يدوياً:")
        print(f"   {pip_cmd} install -r requirements.txt")
        sys.exit(1)

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    print("\n📁 إنشاء المجلدات المطلوبة...")
    
    directories = [
        "src/data",
        "src/uploads", 
        "src/static/media",
        "src/database"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ تم إنشاء مجلد: {directory}")

def create_env_file():
    """إنشاء ملف .env"""
    print("\n🔑 إعداد ملف متغيرات البيئة...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  ملف .env موجود بالفعل")
        return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ تم إنشاء ملف .env من المثال")
        print("⚠️  يرجى تعديل ملف .env وإضافة مفاتيح API الصحيحة")
    else:
        # إنشاء ملف .env أساسي
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("# مفاتيح API المطلوبة\n")
            f.write("DEEPSEEK_API_KEY=your-deepseek-api-key-here\n")
            f.write("GEMINI_API_KEY=your-gemini-api-key-here\n")
            f.write("\n# إعدادات Flask\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=True\n")
        
        print("✅ تم إنشاء ملف .env أساسي")
        print("⚠️  يرجى تعديل ملف .env وإضافة مفاتيح API الصحيحة")

def test_installation():
    """اختبار التثبيت"""
    print("\n🧪 اختبار التثبيت...")
    
    try:
        # اختبار استيراد المكتبات الأساسية
        python_cmd = get_python_command()
        test_script = """
import flask
import openai
import google.generativeai as genai
from PIL import Image
import requests
from gtts import gTTS
print("✅ جميع المكتبات تعمل بشكل صحيح")
"""
        
        result = subprocess.run([python_cmd, "-c", test_script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ اختبار التثبيت نجح")
        else:
            print("❌ فشل اختبار التثبيت:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ خطأ في اختبار التثبيت: {e}")

def get_python_command():
    """الحصول على أمر Python المناسب"""
    if os.name == 'nt':  # Windows
        return os.path.join("venv", "Scripts", "python")
    else:  # Linux/Mac
        return os.path.join("venv", "bin", "python")

def print_next_steps():
    """طباعة الخطوات التالية"""
    python_cmd = get_python_command()
    
    if os.name == 'nt':  # Windows
        activate_cmd = r"venv\Scripts\activate"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate"
    
    print("\n🎉 تم الإعداد بنجاح!")
    print("\n📋 الخطوات التالية:")
    print("1. تفعيل البيئة الافتراضية:")
    print(f"   {activate_cmd}")
    print("\n2. تعديل ملف .env وإضافة مفاتيح API:")
    print("   - DEEPSEEK_API_KEY")
    print("   - GEMINI_API_KEY")
    print("\n3. تشغيل التطبيق:")
    print(f"   {python_cmd} src/main.py")
    print("\n4. فتح المتصفح على:")
    print("   http://localhost:5000")
    print("\n📖 للمزيد من المعلومات، راجع ملف README.md")

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    try:
        check_python_version()
        create_virtual_environment()
        install_requirements()
        create_directories()
        create_env_file()
        test_installation()
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  تم إلغاء الإعداد بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

