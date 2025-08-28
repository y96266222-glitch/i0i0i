# دليل النشر - شات بوت كلية العلوم 🚀

هذا الدليل يوضح كيفية نشر شات بوت كلية العلوم على خوادم مختلفة ومنصات الاستضافة.

## المحتويات
- [النشر على خادم Linux](#النشر-على-خادم-linux)
- [النشر باستخدام Docker](#النشر-باستخدام-docker)
- [النشر على خدمات السحابة](#النشر-على-خدمات-السحابة)
- [إعداد النطاق والـ SSL](#إعداد-النطاق-والـ-ssl)
- [المراقبة والصيانة](#المراقبة-والصيانة)

## النشر على خادم Linux 🐧

### المتطلبات الأساسية
- خادم Ubuntu 20.04+ أو CentOS 8+
- صلاحيات sudo
- اتصال بالإنترنت
- 2GB RAM على الأقل
- 10GB مساحة تخزين

### 1. إعداد الخادم

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python والأدوات الأساسية
sudo apt install python3 python3-pip python3-venv nginx git -y

# تثبيت أدوات إضافية
sudo apt install htop curl wget unzip -y
```

### 2. إنشاء مستخدم للتطبيق

```bash
# إنشاء مستخدم جديد
sudo adduser chatbot
sudo usermod -aG sudo chatbot

# التبديل للمستخدم الجديد
sudo su - chatbot
```

### 3. رفع ملفات التطبيق

```bash
# إنشاء مجلد التطبيق
mkdir -p /home/chatbot/apps/
cd /home/chatbot/apps/

# رفع الملفات (استخدم إحدى الطرق التالية)

# الطريقة 1: استخدام Git
git clone <your-repository-url> college-sciences-chatbot

# الطريقة 2: استخدام SCP من جهازك المحلي
# scp -r college-sciences-chatbot/ chatbot@your-server-ip:/home/chatbot/apps/

# الطريقة 3: استخدام rsync
# rsync -avz college-sciences-chatbot/ chatbot@your-server-ip:/home/chatbot/apps/college-sciences-chatbot/

cd college-sciences-chatbot
```

### 4. إعداد البيئة الافتراضية

```bash
# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية
source venv/bin/activate

# ترقية pip
pip install --upgrade pip

# تثبيت المكتبات
pip install -r requirements.txt

# تثبيت Gunicorn للإنتاج
pip install gunicorn
```

### 5. إعداد متغيرات البيئة

```bash
# إنشاء ملف .env
cp .env.example .env

# تعديل ملف .env
nano .env

# أضف مفاتيح API الصحيحة:
# DEEPSEEK_API_KEY=your-actual-deepseek-key
# GEMINI_API_KEY=your-actual-gemini-key
```

### 6. اختبار التطبيق

```bash
# تشغيل التطبيق للاختبار
python src/main.py

# في terminal آخر، اختبر الاتصال
curl http://localhost:5000

# إيقاف التطبيق (Ctrl+C)
```

### 7. إعداد Gunicorn

```bash
# إنشاء ملف إعداد Gunicorn
nano gunicorn.conf.py
```

أضف المحتوى التالي:

```python
# gunicorn.conf.py
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
reload = False
daemon = False
user = "chatbot"
group = "chatbot"
tmp_upload_dir = None
logfile = "/home/chatbot/apps/college-sciences-chatbot/logs/gunicorn.log"
loglevel = "info"
access_logfile = "/home/chatbot/apps/college-sciences-chatbot/logs/access.log"
error_logfile = "/home/chatbot/apps/college-sciences-chatbot/logs/error.log"
```

```bash
# إنشاء مجلد السجلات
mkdir -p logs

# اختبار Gunicorn
gunicorn -c gunicorn.conf.py src.main:app
```

### 8. إعداد Systemd Service

```bash
# إنشاء ملف الخدمة
sudo nano /etc/systemd/system/chatbot.service
```

أضف المحتوى التالي:

```ini
[Unit]
Description=College Sciences Chatbot
After=network.target

[Service]
Type=exec
User=chatbot
Group=chatbot
WorkingDirectory=/home/chatbot/apps/college-sciences-chatbot
Environment=PATH=/home/chatbot/apps/college-sciences-chatbot/venv/bin
ExecStart=/home/chatbot/apps/college-sciences-chatbot/venv/bin/gunicorn -c gunicorn.conf.py src.main:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل وتشغيل الخدمة
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot

# التحقق من حالة الخدمة
sudo systemctl status chatbot
```

### 9. إعداد Nginx

```bash
# إنشاء ملف إعداد Nginx
sudo nano /etc/nginx/sites-available/chatbot
```

أضف المحتوى التالي:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    client_max_body_size 16M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static/ {
        alias /home/chatbot/apps/college-sciences-chatbot/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/

# اختبار إعداد Nginx
sudo nginx -t

# إعادة تشغيل Nginx
sudo systemctl restart nginx
```

## النشر باستخدام Docker 🐳

### 1. إنشاء Dockerfile

```dockerfile
FROM python:3.11-slim

# تثبيت الأدوات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات التطبيق
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p src/data src/uploads src/static/media src/database

# إعداد المستخدم
RUN useradd -m -u 1000 chatbot && chown -R chatbot:chatbot /app
USER chatbot

# فتح المنفذ
EXPOSE 5000

# أمر التشغيل
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

### 2. إنشاء docker-compose.yml

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
      - FLASK_ENV=production
    volumes:
      - ./src/data:/app/src/data
      - ./src/static/media:/app/src/static/media
      - ./src/database:/app/src/database
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - chatbot
    restart: unless-stopped
```

### 3. إعداد Nginx للـ Docker

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream chatbot {
        server chatbot:5000;
    }
    
    server {
        listen 80;
        server_name your-domain.com;
        
        client_max_body_size 16M;
        
        location / {
            proxy_pass http://chatbot;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 4. تشغيل مع Docker

```bash
# بناء وتشغيل الحاويات
docker-compose up -d

# مراقبة السجلات
docker-compose logs -f

# إيقاف الحاويات
docker-compose down

# إعادة البناء
docker-compose up -d --build
```

## النشر على خدمات السحابة ☁️

### 1. Heroku

```bash
# تثبيت Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# تسجيل الدخول
heroku login

# إنشاء تطبيق جديد
heroku create your-chatbot-name

# إعداد متغيرات البيئة
heroku config:set DEEPSEEK_API_KEY=your-key
heroku config:set GEMINI_API_KEY=your-key
heroku config:set FLASK_ENV=production

# إنشاء Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT src.main:app" > Procfile

# رفع التطبيق
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# فتح التطبيق
heroku open
```

### 2. DigitalOcean App Platform

```yaml
# .do/app.yaml
name: college-sciences-chatbot
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: gunicorn -w 4 -b 0.0.0.0:8080 src.main:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DEEPSEEK_API_KEY
    value: your-key
    type: SECRET
  - key: GEMINI_API_KEY
    value: your-key
    type: SECRET
  http_port: 8080
```

### 3. Railway

```bash
# تثبيت Railway CLI
npm install -g @railway/cli

# تسجيل الدخول
railway login

# إنشاء مشروع جديد
railway new

# ربط المستودع
railway link

# إعداد متغيرات البيئة
railway variables set DEEPSEEK_API_KEY=your-key
railway variables set GEMINI_API_KEY=your-key

# النشر
railway up
```

### 4. Google Cloud Run

```bash
# تثبيت Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# تسجيل الدخول
gcloud auth login

# إعداد المشروع
gcloud config set project your-project-id

# بناء ورفع الصورة
gcloud builds submit --tag gcr.io/your-project-id/chatbot

# النشر
gcloud run deploy chatbot \
  --image gcr.io/your-project-id/chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DEEPSEEK_API_KEY=your-key,GEMINI_API_KEY=your-key
```

## إعداد النطاق والـ SSL 🔒

### 1. ربط النطاق

```bash
# تحديث DNS records
# A record: your-domain.com -> server-ip
# CNAME record: www.your-domain.com -> your-domain.com
```

### 2. تثبيت SSL مع Let's Encrypt

```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# اختبار التجديد التلقائي
sudo certbot renew --dry-run

# إعداد التجديد التلقائي
sudo crontab -e
# أضف السطر التالي:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. إعداد Nginx مع SSL

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    client_max_body_size 16M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /home/chatbot/apps/college-sciences-chatbot/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## المراقبة والصيانة 📊

### 1. مراقبة السجلات

```bash
# سجلات التطبيق
sudo journalctl -u chatbot -f

# سجلات Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# سجلات Gunicorn
tail -f /home/chatbot/apps/college-sciences-chatbot/logs/gunicorn.log
```

### 2. مراقبة الأداء

```bash
# استخدام الذاكرة والمعالج
htop

# مساحة القرص
df -h

# حالة الخدمات
sudo systemctl status chatbot
sudo systemctl status nginx
```

### 3. النسخ الاحتياطي

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/chatbot/backups"
APP_DIR="/home/chatbot/apps/college-sciences-chatbot"

mkdir -p $BACKUP_DIR

# نسخ احتياطي للتطبيق
tar -czf $BACKUP_DIR/app_$DATE.tar.gz -C $APP_DIR .

# نسخ احتياطي لقاعدة البيانات
cp $APP_DIR/src/database/app.db $BACKUP_DIR/database_$DATE.db

# نسخ احتياطي للبيانات المرفوعة
tar -czf $BACKUP_DIR/data_$DATE.tar.gz -C $APP_DIR/src/data .

# حذف النسخ القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# جعل السكريبت قابل للتنفيذ
chmod +x backup.sh

# إضافة للـ cron للتشغيل اليومي
crontab -e
# أضف السطر التالي:
# 0 2 * * * /home/chatbot/backup.sh
```

### 4. التحديثات

```bash
#!/bin/bash
# update.sh

cd /home/chatbot/apps/college-sciences-chatbot

# تفعيل البيئة الافتراضية
source venv/bin/activate

# سحب آخر التحديثات
git pull origin main

# تحديث المكتبات
pip install -r requirements.txt

# إعادة تشغيل التطبيق
sudo systemctl restart chatbot

echo "Update completed"
```

### 5. مراقبة الأخطاء

```bash
# إنشاء سكريبت مراقبة
#!/bin/bash
# monitor.sh

# التحقق من حالة التطبيق
if ! systemctl is-active --quiet chatbot; then
    echo "Chatbot service is down, restarting..."
    sudo systemctl restart chatbot
    # إرسال تنبيه (اختياري)
    # curl -X POST "https://api.telegram.org/bot<token>/sendMessage" \
    #      -d "chat_id=<chat_id>&text=Chatbot service restarted"
fi

# التحقق من استخدام الذاكرة
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
if (( $(echo "$MEMORY_USAGE > 90" | bc -l) )); then
    echo "High memory usage: $MEMORY_USAGE%"
    # إجراءات التنظيف أو التنبيه
fi

# التحقق من مساحة القرص
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "High disk usage: $DISK_USAGE%"
    # تنظيف الملفات المؤقتة
    find /tmp -type f -atime +7 -delete
fi
```

## استكشاف أخطاء النشر 🔧

### مشاكل شائعة وحلولها

#### 1. خطأ في الاتصال بـ API
```
Error: Invalid API key
```
**الحل**: تحقق من مفاتيح API في ملف .env

#### 2. خطأ في الصلاحيات
```
Permission denied
```
**الحل**: 
```bash
sudo chown -R chatbot:chatbot /home/chatbot/apps/college-sciences-chatbot
chmod +x setup.py
```

#### 3. خطأ في قاعدة البيانات
```
sqlite3.OperationalError: database is locked
```
**الحل**: 
```bash
sudo systemctl stop chatbot
rm src/database/app.db
sudo systemctl start chatbot
```

#### 4. خطأ في Nginx
```
502 Bad Gateway
```
**الحل**: 
```bash
sudo systemctl status chatbot
sudo systemctl restart chatbot
sudo systemctl restart nginx
```

---

**تم إنشاء هذا الدليل لضمان نشر ناجح وآمن للتطبيق** 🚀

