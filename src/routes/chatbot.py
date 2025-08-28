from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import os
import json
import base64
from io import BytesIO
from PIL import Image
import requests
import openai
import google.generativeai as genai
from werkzeug.utils import secure_filename
from src.services.ai_service import AIService
from src.services.media_service import MediaService

chatbot_bp = Blueprint('chatbot', __name__)

# إعداد مجلد البيانات
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# إنشاء مثيل من خدمة الذكاء الاصطناعي والوسائط
ai_service = AIService()
media_service = MediaService()

def load_data_files():
    """تحميل جميع ملفات البيانات النصية"""
    data_content = ""
    if os.path.exists(DATA_FOLDER):
        for filename in os.listdir(DATA_FOLDER):
            if filename.endswith('.txt'):
                file_path = os.path.join(DATA_FOLDER, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data_content += f"\n\n--- {filename} ---\n"
                        data_content += f.read()
                except Exception as e:
                    print(f"خطأ في قراءة الملف {filename}: {e}")
    return data_content

def search_in_data(question, data_content):
    """البحث في البيانات المحلية"""
    if not data_content:
        return None
    
    # بحث بسيط في النص
    question_words = question.lower().split()
    data_lower = data_content.lower()
    
    # إذا وجدت كلمات من السؤال في البيانات
    found_words = [word for word in question_words if word in data_lower]
    if len(found_words) >= 2:  # إذا وجدت كلمتين على الأقل
        # استخراج الجزء المناسب من البيانات
        lines = data_content.split('\n')
        relevant_lines = []
        for line in lines:
            if any(word in line.lower() for word in question_words):
                relevant_lines.append(line)
        
        if relevant_lines:
            return '\n'.join(relevant_lines[:5])  # أول 5 أسطر مناسبة
    
    return None

def get_deepseek_response(question, image_data=None):
    """الحصول على إجابة من DeepSeek"""
    try:
        messages = [
            {"role": "system", "content": "أنت مساعد ذكي لكلية العلوم. أجب بالعربية بشكل مفيد ومفصل."},
            {"role": "user", "content": question}
        ]
        
        if image_data:
            # إذا كانت هناك صورة، أضف وصفها
            messages[-1]["content"] += "\n\nملاحظة: تم إرفاق صورة مع السؤال."
        
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"عذراً، حدث خطأ في الحصول على الإجابة: {str(e)}"

def is_answer_relevant(answer, data_content):
    """التحقق من صلة الإجابة بمحتوى البيانات"""
    if not data_content:
        return True
    
    # بحث بسيط لمعرفة إذا كانت الإجابة متعلقة بالمحتوى
    answer_words = answer.lower().split()
    data_words = data_content.lower().split()
    
    # حساب نسبة الكلمات المشتركة
    common_words = set(answer_words) & set(data_words)
    if len(common_words) >= 3:  # إذا كان هناك 3 كلمات مشتركة على الأقل
        return True
    
    return False

@chatbot_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """معالجة رسائل الشات"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'السؤال مطلوب'}), 400
        
        # تحميل البيانات المحلية
        data_content = load_data_files()
        
        # البحث الذكي في البيانات المحلية أولاً
        local_answer = ai_service.smart_search_in_data(question, data_content)
        
        if local_answer:
            return jsonify({
                'answer': local_answer,
                'source': 'local_data'
            })
        
        # إذا لم توجد إجابة محلية، استخدم DeepSeek
        deepseek_answer = ai_service.get_enhanced_response(question, context=data_content[:500])
        
        # التحقق من صلة الإجابة بالمحتوى
        if ai_service.check_content_relevance(deepseek_answer, data_content):
            return jsonify({
                'answer': deepseek_answer,
                'source': 'deepseek'
            })
        else:
            return jsonify({
                'answer': 'هذا السؤال غير مقرر في منهج كلية العلوم.',
                'source': 'not_relevant'
            })
    
    except Exception as e:
        return jsonify({'error': f'حدث خطأ: {str(e)}'}), 500

@chatbot_bp.route('/chat/image', methods=['POST'])
@cross_origin()
def chat_with_image():
    """معالجة رسائل الشات مع الصور"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'الصورة مطلوبة'}), 400
        
        image_file = request.files['image']
        question = request.form.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'السؤال مطلوب'}), 400
        
        # حفظ الصورة مؤقتاً
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)
        
        # تحليل الصورة باستخدام Gemini
        image_analysis = ai_service.analyze_image_with_gemini(image_path, question)
        
        # تحميل البيانات المحلية
        data_content = load_data_files()
        
        # الحصول على إجابة محسنة مع تحليل الصورة
        enhanced_answer = ai_service.get_enhanced_response(
            question, 
            context=data_content[:500], 
            image_analysis=image_analysis
        )
        
        # التحقق من صلة الإجابة
        if ai_service.check_content_relevance(enhanced_answer, data_content):
            return jsonify({
                'answer': enhanced_answer,
                'image_analysis': image_analysis,
                'source': 'gemini_with_image'
            })
        else:
            return jsonify({
                'answer': 'هذا السؤال غير مقرر في منهج كلية العلوم.',
                'image_analysis': image_analysis,
                'source': 'not_relevant'
            })
    
    except Exception as e:
        return jsonify({'error': f'حدث خطأ: {str(e)}'}), 500
    finally:
        # حذف الصورة المؤقتة
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)

@chatbot_bp.route('/generate/video', methods=['POST'])
@cross_origin()
def generate_video():
    """إنشاء فيديو باستخدام خدمة الوسائط"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'error': 'الموضوع مطلوب لإنشاء الفيديو'}), 400
        
        # إنشاء محتوى الفيديو
        result = media_service.generate_educational_content(topic, "video")
        
        if result['status'] == 'success':
            return jsonify({
                'video_url': result['url'],
                'title': result['title'],
                'script': result['script'],
                'type': 'video',
                'status': 'generated'
            })
        else:
            return jsonify({
                'error': result.get('error', 'فشل في إنشاء الفيديو'),
                'status': 'error'
            }), 500
    
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في إنشاء الفيديو: {str(e)}'}), 500

@chatbot_bp.route('/generate/audio', methods=['POST'])
@cross_origin()
def generate_audio():
    """إنشاء صوت باستخدام خدمة الوسائط"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        text = data.get('text', '').strip()
        
        if topic:
            # إنشاء محتوى صوتي تعليمي
            result = media_service.generate_educational_content(topic, "audio")
            
            if result['status'] == 'success':
                return jsonify({
                    'audio_url': result['url'],
                    'title': result['title'],
                    'script': result['script'],
                    'type': 'audio',
                    'status': 'generated'
                })
            else:
                return jsonify({
                    'error': result.get('error', 'فشل في إنشاء الصوت'),
                    'status': 'error'
                }), 500
        
        elif text:
            # تحويل نص محدد إلى صوت
            audio_url = media_service.text_to_speech(text)
            
            if audio_url:
                return jsonify({
                    'audio_url': audio_url,
                    'text': text,
                    'type': 'audio',
                    'status': 'generated'
                })
            else:
                return jsonify({
                    'error': 'فشل في تحويل النص إلى صوت',
                    'status': 'error'
                }), 500
        
        else:
            return jsonify({'error': 'الموضوع أو النص مطلوب'}), 400
    
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في إنشاء الصوت: {str(e)}'}), 500

@chatbot_bp.route('/upload/data', methods=['POST'])
@cross_origin()
def upload_data():
    """رفع ملفات البيانات"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'الملف مطلوب'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        if file and file.filename.endswith('.txt'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(DATA_FOLDER, filename)
            file.save(file_path)
            
            return jsonify({
                'message': 'تم رفع الملف بنجاح',
                'filename': filename
            })
        else:
            return jsonify({'error': 'يجب أن يكون الملف نصي (.txt)'}), 400
    
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في رفع الملف: {str(e)}'}), 500

@chatbot_bp.route('/data/files', methods=['GET'])
@cross_origin()
def list_data_files():
    """عرض قائمة ملفات البيانات"""
    try:
        files = []
        if os.path.exists(DATA_FOLDER):
            for filename in os.listdir(DATA_FOLDER):
                if filename.endswith('.txt'):
                    file_path = os.path.join(DATA_FOLDER, filename)
                    file_size = os.path.getsize(file_path)
                    files.append({
                        'name': filename,
                        'size': file_size
                    })
        
        return jsonify({'files': files})
    
    except Exception as e:
        return jsonify({'error': f'حدث خطأ: {str(e)}'}), 500

