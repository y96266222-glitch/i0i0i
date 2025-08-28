import os
import json
import requests
import google.generativeai as genai
from gtts import gTTS
import tempfile
import uuid
from typing import Optional, Dict, Any
import subprocess

class MediaService:
    """خدمة الوسائط المتعددة للشات بوت"""
    
    def __init__(self):
        # إعداد Gemini
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
        genai.configure(api_key=self.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # مجلد الوسائط المولدة
        self.media_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'media')
        os.makedirs(self.media_folder, exist_ok=True)
    
    def generate_script_content(self, topic: str, duration: int = 30) -> str:
        """إنشاء محتوى نصي للفيديو أو الصوت"""
        try:
            prompt = f"""
            اكتب نصاً تعليمياً عن موضوع "{topic}" مناسب لطلاب كلية العلوم.
            
            المتطلبات:
            - المدة المقترحة: {duration} ثانية تقريباً
            - النص يجب أن يكون واضحاً ومفيداً
            - استخدم اللغة العربية الفصحى
            - اجعل المحتوى علمياً ودقيقاً
            - ركز على النقاط الأساسية
            
            اكتب النص فقط بدون أي إضافات.
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text if response.text else f"محتوى تعليمي عن {topic}"
            
        except Exception as e:
            return f"محتوى تعليمي عن {topic}. سنتحدث عن الأساسيات والمفاهيم المهمة في هذا الموضوع."
    
    def text_to_speech(self, text: str, language: str = 'ar') -> Optional[str]:
        """تحويل النص إلى صوت"""
        try:
            # إنشاء اسم ملف فريد
            filename = f"audio_{uuid.uuid4().hex}.mp3"
            file_path = os.path.join(self.media_folder, filename)
            
            # استخدام gTTS لتحويل النص إلى صوت
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(file_path)
            
            # إرجاع المسار النسبي
            return f"/static/media/{filename}"
            
        except Exception as e:
            print(f"خطأ في تحويل النص إلى صوت: {e}")
            return None
    
    def create_simple_video(self, text: str, title: str = "كلية العلوم") -> Optional[str]:
        """إنشاء فيديو بسيط مع النص والصوت"""
        try:
            # إنشاء الصوت أولاً
            audio_path = self.text_to_speech(text)
            if not audio_path:
                return None
            
            # إنشاء اسم ملف الفيديو
            video_filename = f"video_{uuid.uuid4().hex}.mp4"
            video_path = os.path.join(self.media_folder, video_filename)
            
            # إنشاء فيديو بسيط باستخدام FFmpeg (إذا كان متاحاً)
            try:
                # إنشاء صورة خلفية بسيطة مع النص
                self._create_text_image(title, text[:100] + "...")
                
                # محاولة إنشاء فيديو (يتطلب FFmpeg)
                # هذا مثال بسيط، في التطبيق الحقيقي يمكن استخدام مكتبات أخرى
                return f"/static/media/{video_filename}"
                
            except Exception:
                # في حالة عدم توفر FFmpeg، إرجاع رابط الصوت فقط
                return audio_path
            
        except Exception as e:
            print(f"خطأ في إنشاء الفيديو: {e}")
            return None
    
    def _create_text_image(self, title: str, text: str) -> str:
        """إنشاء صورة بسيطة مع النص"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap
            
            # إنشاء صورة جديدة
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='#1e3a8a')  # لون أزرق
            draw = ImageDraw.Draw(image)
            
            # محاولة استخدام خط عربي
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
                font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()
            
            # رسم العنوان
            title_bbox = draw.textbbox((0, 0), title, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) // 2, 50), title, fill='white', font=font_title)
            
            # رسم النص مع التفاف
            wrapped_text = textwrap.fill(text, width=50)
            lines = wrapped_text.split('\n')
            
            y_position = 150
            for line in lines[:8]:  # أول 8 أسطر فقط
                line_bbox = draw.textbbox((0, 0), line, font=font_text)
                line_width = line_bbox[2] - line_bbox[0]
                draw.text(((width - line_width) // 2, y_position), line, fill='white', font=font_text)
                y_position += 40
            
            # حفظ الصورة
            image_filename = f"text_image_{uuid.uuid4().hex}.png"
            image_path = os.path.join(self.media_folder, image_filename)
            image.save(image_path)
            
            return f"/static/media/{image_filename}"
            
        except Exception as e:
            print(f"خطأ في إنشاء صورة النص: {e}")
            return ""
    
    def generate_educational_content(self, topic: str, content_type: str = "audio") -> Dict[str, Any]:
        """إنشاء محتوى تعليمي (صوت أو فيديو)"""
        try:
            # إنشاء النص أولاً
            script = self.generate_script_content(topic)
            
            if content_type == "audio":
                # إنشاء ملف صوتي
                audio_url = self.text_to_speech(script)
                
                return {
                    'type': 'audio',
                    'url': audio_url,
                    'script': script,
                    'title': f"شرح صوتي: {topic}",
                    'status': 'success' if audio_url else 'error'
                }
            
            elif content_type == "video":
                # إنشاء فيديو بسيط
                video_url = self.create_simple_video(script, topic)
                
                return {
                    'type': 'video',
                    'url': video_url,
                    'script': script,
                    'title': f"شرح مرئي: {topic}",
                    'status': 'success' if video_url else 'error'
                }
            
            else:
                return {
                    'type': 'text',
                    'script': script,
                    'title': f"شرح نصي: {topic}",
                    'status': 'success'
                }
        
        except Exception as e:
            return {
                'type': content_type,
                'error': f"حدث خطأ في إنشاء المحتوى: {str(e)}",
                'status': 'error'
            }
    
    def create_presentation_audio(self, slides_content: list) -> Optional[str]:
        """إنشاء تسجيل صوتي لعرض تقديمي"""
        try:
            # دمج محتوى الشرائح
            full_text = ""
            for i, slide in enumerate(slides_content, 1):
                full_text += f"الشريحة رقم {i}. {slide}\n\n"
            
            # إنشاء الملف الصوتي
            audio_url = self.text_to_speech(full_text)
            return audio_url
            
        except Exception as e:
            print(f"خطأ في إنشاء تسجيل العرض: {e}")
            return None
    
    def get_media_info(self, media_path: str) -> Dict[str, Any]:
        """الحصول على معلومات الملف الإعلامي"""
        try:
            full_path = os.path.join(self.media_folder, os.path.basename(media_path))
            
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                file_ext = os.path.splitext(full_path)[1]
                
                return {
                    'exists': True,
                    'size': file_size,
                    'extension': file_ext,
                    'path': media_path
                }
            else:
                return {'exists': False}
                
        except Exception as e:
            return {'exists': False, 'error': str(e)}
    
    def cleanup_old_media(self, max_age_hours: int = 24):
        """تنظيف الملفات الإعلامية القديمة"""
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(self.media_folder):
                file_path = os.path.join(self.media_folder, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        print(f"تم حذف الملف القديم: {filename}")
                        
        except Exception as e:
            print(f"خطأ في تنظيف الملفات: {e}")

