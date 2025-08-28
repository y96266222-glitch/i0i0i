# شات بوت كلية العلوم 🎓

شات بوت ذكي متطور مصمم خصيصاً لكلية العلوم، يستخدم تقنيات الذكاء الاصطناعي المتقدمة لتقديم إجابات دقيقة ومفيدة للطلاب والأساتذة.

## المميزات الرئيسية ✨

### 🤖 ذكاء اصطناعي متطور
- **البحث الذكي**: يبحث في ملفات البيانات المحلية أولاً
- **DeepSeek AI**: يستخدم نموذج DeepSeek للإجابات المتقدمة
- **Gemini Vision**: تحليل الصور والمخططات العلمية
- **فلترة المحتوى**: يتأكد من صلة الإجابات بالمنهج الدراسي

### 📱 واجهة مستخدم متقدمة
- **تصميم عربي**: واجهة باللغة العربية مع دعم RTL
- **تصميم متجاوب**: يعمل على جميع الأجهزة (جوال، تابلت، كمبيوتر)
- **تفاعل سلس**: أنيميشن وتأثيرات بصرية جميلة
- **سهولة الاستخدام**: واجهة بديهية وبسيطة

### 🎯 وظائف متنوعة
- **أسئلة نصية**: اكتب سؤالك واحصل على إجابة فورية
- **تحليل الصور**: ارفع صورة واطرح سؤالاً عنها
- **إنشاء الصوت**: تحويل النصوص إلى ملفات صوتية
- **إنشاء الفيديو**: إنتاج محتوى مرئي تعليمي
- **إدارة البيانات**: رفع وإدارة ملفات المناهج

## متطلبات النظام 🖥️

- Python 3.11 أو أحدث
- 4 جيجابايت رام على الأقل
- 2 جيجابايت مساحة تخزين فارغة
- اتصال بالإنترنت

## التثبيت والإعداد 🚀

### 1. تحميل المشروع
```bash
# استنساخ المشروع أو تحميل الملفات
cd /path/to/your/directory
```

### 2. إعداد البيئة الافتراضية
```bash
# إنشاء البيئة الافتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# في Linux/Mac:
source venv/bin/activate
# في Windows:
venv\Scripts\activate
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة
أنشئ ملف `.env` في المجلد الرئيسي وأضف:

```env
# مفاتيح API (مطلوبة)
DEEPSEEK_API_KEY=your-deepseek-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# إعدادات اختيارية
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. تشغيل التطبيق
```bash
python src/main.py
```

سيعمل التطبيق على: `http://localhost:5000`

## الحصول على مفاتيح API 🔑

### DeepSeek API
1. اذهب إلى [DeepSeek Platform](https://platform.deepseek.com)
2. أنشئ حساب جديد أو سجل الدخول
3. اذهب إلى قسم API Keys
4. أنشئ مفتاح API جديد
5. انسخ المفتاح وضعه في ملف `.env`

### Gemini API
1. اذهب إلى [Google AI Studio](https://makersuite.google.com)
2. سجل الدخول بحساب Google
3. أنشئ مفتاح API جديد
4. انسخ المفتاح وضعه في ملف `.env`

## كيفية الاستخدام 📖

### 1. الأسئلة النصية
- اكتب سؤالك في مربع النص
- اضغط إرسال أو Enter
- ستحصل على إجابة فورية

### 2. الأسئلة مع الصور
- اضغط على أيقونة الصورة 📷
- اختر صورة من جهازك
- اكتب سؤالك عن الصورة
- اضغط إرسال

### 3. إنشاء المحتوى الصوتي
- اضغط على أيقونة الفيديو 🎥
- اختر "إنشاء شرح صوتي"
- اكتب الموضوع المطلوب
- اضغط إرسال

### 4. إنشاء المحتوى المرئي
- اضغط على أيقونة الفيديو 🎥
- اختر "إنشاء شرح مرئي"
- اكتب الموضوع المطلوب
- اضغط إرسال

### 5. إدارة البيانات
- اضغط على "إدارة البيانات"
- ارفع ملفات نصية (.txt) تحتوي على المناهج
- ستظهر قائمة بالملفات المرفوعة

## بنية المشروع 📁

```
college-sciences-chatbot/
├── src/
│   ├── main.py                 # الملف الرئيسي
│   ├── routes/
│   │   ├── user.py            # مسارات المستخدمين
│   │   └── chatbot.py         # مسارات الشات بوت
│   ├── services/
│   │   ├── ai_service.py      # خدمة الذكاء الاصطناعي
│   │   └── media_service.py   # خدمة الوسائط المتعددة
│   ├── models/
│   │   └── user.py            # نماذج قاعدة البيانات
│   ├── static/
│   │   ├── index.html         # الواجهة الرئيسية
│   │   ├── styles.css         # ملف التصميم
│   │   ├── script.js          # ملف JavaScript
│   │   └── media/             # الملفات المولدة
│   ├── data/                  # ملفات البيانات المرفوعة
│   ├── uploads/               # الصور المؤقتة
│   └── database/
│       └── app.db             # قاعدة البيانات
├── venv/                      # البيئة الافتراضية
├── requirements.txt           # المكتبات المطلوبة
├── .env                       # متغيرات البيئة
└── README.md                  # هذا الملف
```

## API Endpoints 🔗

### الشات العادي
```
POST /api/chat
Content-Type: application/json

{
    "question": "ما هو التمثيل الضوئي؟"
}
```

### الشات مع الصور
```
POST /api/chat/image
Content-Type: multipart/form-data

question: "ما هذا المركب الكيميائي؟"
image: [ملف الصورة]
```

### إنشاء الصوت
```
POST /api/generate/audio
Content-Type: application/json

{
    "topic": "الخلية النباتية"
}
```

### إنشاء الفيديو
```
POST /api/generate/video
Content-Type: application/json

{
    "topic": "الدورة الدموية"
}
```

### رفع البيانات
```
POST /api/upload/data
Content-Type: multipart/form-data

file: [ملف نصي .txt]
```

### قائمة الملفات
```
GET /api/data/files
```

## النشر على الخادم 🌐

### 1. النشر على خادم Linux

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و pip
sudo apt install python3 python3-pip python3-venv -y

# رفع الملفات إلى الخادم
scp -r college-sciences-chatbot/ user@server:/path/to/deployment/

# الدخول للخادم
ssh user@server

# الانتقال لمجلد المشروع
cd /path/to/deployment/college-sciences-chatbot/

# إعداد البيئة الافتراضية
python3 -m venv venv
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt

# إعداد متغيرات البيئة
nano .env
# أضف مفاتيح API

# تشغيل التطبيق مع Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### 2. النشر مع Docker

أنشئ ملف `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

أنشئ ملف `docker-compose.yml`:

```yaml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./src/data:/app/src/data
      - ./src/static/media:/app/src/static/media
```

تشغيل مع Docker:
```bash
docker-compose up -d
```

### 3. النشر على خدمات السحابة

#### Heroku
```bash
# تثبيت Heroku CLI
# إنشاء تطبيق جديد
heroku create your-chatbot-name

# إعداد متغيرات البيئة
heroku config:set DEEPSEEK_API_KEY=your-key
heroku config:set GEMINI_API_KEY=your-key

# رفع التطبيق
git push heroku main
```

#### Railway
1. اربط مستودع GitHub بـ Railway
2. أضف متغيرات البيئة في لوحة التحكم
3. سيتم النشر تلقائياً

## استكشاف الأخطاء 🔧

### مشاكل شائعة وحلولها

#### 1. خطأ في مفاتيح API
```
Error: Invalid API key
```
**الحل**: تأكد من صحة مفاتيح API في ملف `.env`

#### 2. خطأ في تثبيت المكتبات
```
ERROR: Could not install packages
```
**الحل**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

#### 3. خطأ في الاتصال بقاعدة البيانات
```
sqlite3.OperationalError: database is locked
```
**الحل**: أعد تشغيل التطبيق أو احذف ملف `app.db`

#### 4. مشاكل في رفع الملفات
```
413 Request Entity Too Large
```
**الحل**: قلل حجم الملف أو زد الحد الأقصى في إعدادات Flask

### سجلات الأخطاء
تحقق من سجلات التطبيق:
```bash
# في وضع التطوير
python src/main.py

# مع Gunicorn
gunicorn --log-level debug src.main:app
```

## التطوير والمساهمة 👨‍💻

### إعداد بيئة التطوير
```bash
# استنساخ المشروع
git clone <repository-url>
cd college-sciences-chatbot

# إعداد البيئة الافتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows

# تثبيت المكتبات
pip install -r requirements.txt

# تشغيل في وضع التطوير
export FLASK_ENV=development
export FLASK_DEBUG=True
python src/main.py
```

### إضافة ميزات جديدة
1. أنشئ فرع جديد: `git checkout -b feature/new-feature`
2. اكتب الكود واختبره
3. أضف التوثيق المناسب
4. أرسل Pull Request

### اختبار التطبيق
```bash
# تشغيل الاختبارات (إذا توفرت)
python -m pytest tests/

# اختبار API endpoints
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "ما هو الماء؟"}'
```

## الأمان والخصوصية 🔒

### حماية مفاتيح API
- لا تشارك مفاتيح API مع أحد
- استخدم متغيرات البيئة دائماً
- غير المفاتيح دورياً

### حماية البيانات
- ملفات البيانات المرفوعة محلية فقط
- الصور المؤقتة تُحذف تلقائياً
- لا يتم حفظ المحادثات

### أفضل الممارسات
- استخدم HTTPS في الإنتاج
- فعل جدار الحماية
- راقب استخدام API
- احتفظ بنسخ احتياطية

## الدعم والمساعدة 💬

### الحصول على المساعدة
- اقرأ هذا الدليل كاملاً
- تحقق من قسم استكشاف الأخطاء
- ابحث في المشاكل المعروفة

### الإبلاغ عن المشاكل
عند الإبلاغ عن مشكلة، أرفق:
- وصف المشكلة
- رسالة الخطأ كاملة
- خطوات إعادة إنتاج المشكلة
- معلومات النظام (OS, Python version)

## الترخيص 📄

هذا المشروع مرخص تحت رخصة MIT. راجع ملف LICENSE للتفاصيل.

## الشكر والتقدير 🙏

شكر خاص لـ:
- فريق DeepSeek على نموذج الذكاء الاصطناعي المتطور
- Google على Gemini AI
- مجتمع Python ومطوري Flask
- جميع المساهمين في المكتبات مفتوحة المصدر

---

**تم تطوير هذا المشروع بـ ❤️ لخدمة التعليم العلمي**

للمزيد من المعلومات أو الدعم الفني، لا تتردد في التواصل معنا.

