# دليل الحصول على مفاتيح API 🔑

هذا الدليل يوضح كيفية الحصول على مفاتيح API المطلوبة لتشغيل شات بوت كلية العلوم.

## المحتويات
- [DeepSeek API](#deepseek-api)
- [Google Gemini API](#google-gemini-api)
- [إعداد المفاتيح في التطبيق](#إعداد-المفاتيح-في-التطبيق)
- [اختبار المفاتيح](#اختبار-المفاتيح)
- [أمان المفاتيح](#أمان-المفاتيح)

## DeepSeek API 🧠

DeepSeek هو نموذج ذكاء اصطناعي متطور يُستخدم للإجابة على الأسئلة النصية.

### خطوات الحصول على المفتاح:

#### 1. إنشاء حساب
- اذهب إلى [DeepSeek Platform](https://platform.deepseek.com)
- اضغط على "Sign Up" أو "إنشاء حساب"
- أدخل بياناتك:
  - البريد الإلكتروني
  - كلمة المرور
  - رقم الهاتف (للتحقق)

#### 2. تأكيد الحساب
- تحقق من بريدك الإلكتروني
- اضغط على رابط التأكيد
- أكمل عملية التحقق من رقم الهاتف

#### 3. الوصول إلى لوحة التحكم
- سجل الدخول إلى حسابك
- ستجد لوحة التحكم الرئيسية

#### 4. إنشاء مفتاح API
- اذهب إلى قسم "API Keys" أو "مفاتيح API"
- اضغط على "Create New Key" أو "إنشاء مفتاح جديد"
- أدخل اسماً للمفتاح (مثل: "College Chatbot")
- اختر الصلاحيات المطلوبة:
  - ✅ Chat Completion
  - ✅ Text Generation
- اضغط على "Create" أو "إنشاء"

#### 5. نسخ المفتاح
- انسخ المفتاح فوراً (لن تتمكن من رؤيته مرة أخرى)
- احفظه في مكان آمن

### معلومات مهمة عن DeepSeek:
- **النموذج المستخدم**: `deepseek-chat`
- **الحد الأقصى للرموز**: 4,000 رمز لكل طلب
- **التسعير**: يبدأ من $0.14 لكل مليون رمز
- **الحدود**: 60 طلب في الدقيقة للحسابات المجانية

### مثال على الاستخدام:
```python
import openai

openai.api_base = "https://api.deepseek.com"
openai.api_key = "your-deepseek-api-key"

response = openai.ChatCompletion.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "ما هو التمثيل الضوئي؟"}]
)
```

## Google Gemini API 🌟

Gemini هو نموذج الذكاء الاصطناعي من Google، يدعم النصوص والصور.

### خطوات الحصول على المفتاح:

#### 1. الوصول إلى Google AI Studio
- اذهب إلى [Google AI Studio](https://makersuite.google.com)
- سجل الدخول بحساب Google الخاص بك

#### 2. إنشاء مشروع جديد (إذا لزم الأمر)
- اضغط على "Create Project" إذا لم يكن لديك مشروع
- أدخل اسم المشروع
- اختر المنطقة الجغرافية

#### 3. تفعيل Gemini API
- اذهب إلى قسم "API Keys"
- اضغط على "Create API Key"
- اختر المشروع المناسب

#### 4. إنشاء مفتاح API
- اضغط على "Create API Key in new project" أو اختر مشروع موجود
- انتظر حتى يتم إنشاء المفتاح
- انسخ المفتاح واحفظه

#### 5. تفعيل الخدمات المطلوبة
- تأكد من تفعيل:
  - ✅ Generative Language API
  - ✅ AI Platform API

### معلومات مهمة عن Gemini:
- **النماذج المتاحة**: 
  - `gemini-pro` (للنصوص)
  - `gemini-pro-vision` (للنصوص والصور)
- **الحد الأقصى للرموز**: 30,720 رمز
- **التسعير**: يبدأ من $0.50 لكل مليون رمز
- **الحدود**: 60 طلب في الدقيقة

### مثال على الاستخدام:
```python
import google.generativeai as genai

genai.configure(api_key="your-gemini-api-key")
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("اشرح لي الخلية النباتية")
print(response.text)
```

## إعداد المفاتيح في التطبيق ⚙️

### 1. إنشاء ملف .env
```bash
# في مجلد المشروع
cp .env.example .env
```

### 2. تعديل ملف .env
```bash
nano .env
```

### 3. إضافة المفاتيح
```env
# مفاتيح API المطلوبة
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# إعدادات Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. حفظ الملف
- احفظ الملف (Ctrl+S في nano، ثم Ctrl+X للخروج)
- تأكد من عدم مشاركة هذا الملف مع أحد

## اختبار المفاتيح 🧪

### 1. اختبار DeepSeek API
```python
# test_deepseek.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_base = "https://api.deepseek.com"
openai.api_key = os.getenv('DEEPSEEK_API_KEY')

try:
    response = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "مرحبا"}],
        max_tokens=50
    )
    print("✅ DeepSeek API يعمل بشكل صحيح")
    print(f"الرد: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ خطأ في DeepSeek API: {e}")
```

### 2. اختبار Gemini API
```python
# test_gemini.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("مرحبا")
    print("✅ Gemini API يعمل بشكل صحيح")
    print(f"الرد: {response.text}")
except Exception as e:
    print(f"❌ خطأ في Gemini API: {e}")
```

### 3. تشغيل الاختبارات
```bash
# تفعيل البيئة الافتراضية
source venv/bin/activate

# تثبيت python-dotenv إذا لم يكن مثبتاً
pip install python-dotenv

# تشغيل الاختبارات
python test_deepseek.py
python test_gemini.py
```

## أمان المفاتيح 🔒

### أفضل الممارسات:

#### 1. لا تشارك المفاتيح
- ❌ لا تضع المفاتيح في الكود مباشرة
- ❌ لا ترفع ملف .env إلى Git
- ❌ لا تشارك المفاتيح في الرسائل أو البريد الإلكتروني

#### 2. استخدم متغيرات البيئة
```python
# ✅ صحيح
api_key = os.getenv('DEEPSEEK_API_KEY')

# ❌ خطأ
api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#### 3. أضف .env إلى .gitignore
```gitignore
# .gitignore
.env
*.env
.env.local
.env.production
```

#### 4. استخدم مفاتيح منفصلة للبيئات المختلفة
- مفتاح للتطوير (Development)
- مفتاح للاختبار (Testing)  
- مفتاح للإنتاج (Production)

#### 5. راقب استخدام المفاتيح
- تحقق من لوحة التحكم بانتظام
- راقب الاستخدام والتكاليف
- فعل التنبيهات للاستخدام المرتفع

#### 6. دور المفاتيح بانتظام
- غير المفاتيح كل 3-6 أشهر
- غيرها فوراً إذا شككت في تسريبها
- احتفظ بنسخة احتياطية آمنة

### في حالة تسريب المفتاح:

#### 1. إلغاء المفتاح فوراً
- اذهب إلى لوحة التحكم
- احذف المفتاح المسرب
- أنشئ مفتاحاً جديداً

#### 2. تحديث التطبيق
- حدث ملف .env بالمفتاح الجديد
- أعد تشغيل التطبيق
- اختبر أن كل شيء يعمل

#### 3. راجع السجلات
- تحقق من سجلات الاستخدام
- ابحث عن أي نشاط مشبوه
- غير كلمات المرور إذا لزم الأمر

## حل المشاكل الشائعة 🔧

### 1. "Invalid API Key"
```
Error: The API key provided is invalid
```
**الحلول:**
- تحقق من نسخ المفتاح بشكل صحيح
- تأكد من عدم وجود مسافات إضافية
- تحقق من انتهاء صلاحية المفتاح
- أنشئ مفتاحاً جديداً

### 2. "Quota Exceeded"
```
Error: You have exceeded your quota
```
**الحلول:**
- تحقق من حدود الاستخدام في لوحة التحكم
- انتظر حتى إعادة تعيين الحدود
- ارفع حدود الاستخدام إذا أمكن
- استخدم مفتاحاً آخر مؤقتاً

### 3. "Rate Limit Exceeded"
```
Error: Too many requests
```
**الحلول:**
- قلل عدد الطلبات في الدقيقة
- أضف تأخير بين الطلبات
- استخدم نظام queue للطلبات
- ارفع حدود المعدل إذا أمكن

### 4. "Service Unavailable"
```
Error: Service temporarily unavailable
```
**الحلول:**
- انتظر وأعد المحاولة
- تحقق من حالة الخدمة
- استخدم آلية إعادة المحاولة
- تواصل مع الدعم الفني

## معلومات إضافية 📋

### روابط مفيدة:
- [DeepSeek Documentation](https://platform.deepseek.com/api-docs)
- [Google Gemini Documentation](https://ai.google.dev/docs)
- [OpenAI Python Library](https://github.com/openai/openai-python)

### أدوات مساعدة:
- [Postman](https://www.postman.com) - لاختبار API
- [curl](https://curl.se) - لاختبار الطلبات من Terminal
- [Insomnia](https://insomnia.rest) - بديل لـ Postman

### مجتمعات الدعم:
- [DeepSeek Discord](https://discord.gg/deepseek)
- [Google AI Community](https://developers.googleblog.com/2023/12/gemini-api-developers.html)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/api)

---

**احرص على حماية مفاتيح API الخاصة بك وتعامل معها كما تتعامل مع كلمات المرور!** 🔐

