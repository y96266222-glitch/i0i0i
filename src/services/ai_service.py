import os
import json
import base64
import requests
import openai
import google.generativeai as genai
from PIL import Image
import io
import re
from typing import Optional, Dict, Any

class AIService:
    """خدمة الذكاء الاصطناعي للشات بوت"""
    
    def __init__(self):
        # إعداد DeepSeek
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', 'your-deepseek-api-key-here')
        openai.api_base = "https://api.deepseek.com"
        openai.api_key = self.deepseek_api_key
        
        # إعداد Gemini
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
        genai.configure(api_key=self.gemini_api_key)
        
        # إعداد نموذج Gemini للنص والصور
        self.gemini_model = genai.GenerativeModel('gemini-pro-vision')
        self.gemini_text_model = genai.GenerativeModel('gemini-pro')
    
    def analyze_image_with_gemini(self, image_path: str, question: str) -> str:
        """تحليل الصورة باستخدام Gemini"""
        try:
            # قراءة الصورة
            image = Image.open(image_path)
            
            # تحضير النص للتحليل
            prompt = f"""
            أنت مساعد ذكي لكلية العلوم. حلل هذه الصورة وأجب على السؤال التالي:
            
            السؤال: {question}
            
            يرجى تقديم إجابة مفصلة ومفيدة بالعربية.
            """
            
            # إرسال الطلب لـ Gemini
            response = self.gemini_model.generate_content([prompt, image])
            
            return response.text if response.text else "لم أتمكن من تحليل الصورة."
            
        except Exception as e:
            return f"حدث خطأ في تحليل الصورة: {str(e)}"
    
    def get_enhanced_response(self, question: str, context: str = "", image_analysis: str = "") -> str:
        """الحصول على إجابة محسنة من DeepSeek"""
        try:
            # تحضير النص للطلب
            system_prompt = """
            أنت مساعد ذكي متخصص في كلية العلوم. مهمتك هي:
            1. تقديم إجابات دقيقة ومفيدة باللغة العربية
            2. استخدام المعلومات المتاحة من السياق
            3. التركيز على المواضيع العلمية والأكاديمية
            4. تقديم إجابات واضحة ومنظمة
            """
            
            user_message = f"السؤال: {question}"
            
            if context:
                user_message += f"\n\nالسياق المتاح: {context}"
            
            if image_analysis:
                user_message += f"\n\nتحليل الصورة: {image_analysis}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=messages,
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"حدث خطأ في الحصول على الإجابة: {str(e)}"
    
    def check_content_relevance(self, answer: str, data_content: str) -> bool:
        """فحص صلة المحتوى بالبيانات المحلية بطريقة متقدمة"""
        if not data_content:
            return True
        
        try:
            # استخدام Gemini للتحقق من الصلة
            prompt = f"""
            قم بتحليل ما إذا كانت الإجابة التالية متعلقة بالمحتوى المقرر:
            
            الإجابة: {answer[:500]}...
            
            المحتوى المقرر: {data_content[:1000]}...
            
            أجب بـ "نعم" إذا كانت الإجابة متعلقة بالمحتوى المقرر، أو "لا" إذا لم تكن متعلقة.
            """
            
            response = self.gemini_text_model.generate_content(prompt)
            result = response.text.strip().lower()
            
            return "نعم" in result or "yes" in result
            
        except Exception:
            # في حالة الخطأ، استخدم الطريقة البسيطة
            answer_words = set(answer.lower().split())
            data_words = set(data_content.lower().split())
            common_words = answer_words & data_words
            return len(common_words) >= 5
    
    def extract_keywords(self, text: str) -> list:
        """استخراج الكلمات المفتاحية من النص"""
        try:
            prompt = f"""
            استخرج الكلمات المفتاحية الأساسية من النص التالي:
            
            {text}
            
            اكتب الكلمات المفتاحية مفصولة بفواصل.
            """
            
            response = self.gemini_text_model.generate_content(prompt)
            keywords = [keyword.strip() for keyword in response.text.split(',')]
            return keywords[:10]  # أول 10 كلمات مفتاحية
            
        except Exception:
            # طريقة بسيطة في حالة الخطأ
            words = re.findall(r'\b\w+\b', text.lower())
            return list(set(words))[:10]
    
    def smart_search_in_data(self, question: str, data_content: str) -> Optional[str]:
        """بحث ذكي في البيانات باستخدام الذكاء الاصطناعي"""
        if not data_content:
            return None
        
        try:
            # استخراج الكلمات المفتاحية من السؤال
            question_keywords = self.extract_keywords(question)
            
            # تقسيم البيانات إلى أجزاء
            data_chunks = data_content.split('\n\n')
            relevant_chunks = []
            
            # البحث عن الأجزاء المناسبة
            for chunk in data_chunks:
                chunk_lower = chunk.lower()
                if any(keyword.lower() in chunk_lower for keyword in question_keywords):
                    relevant_chunks.append(chunk)
            
            if relevant_chunks:
                # دمج الأجزاء المناسبة
                combined_content = '\n\n'.join(relevant_chunks[:3])  # أول 3 أجزاء
                
                # استخدام Gemini لتحسين الإجابة
                prompt = f"""
                بناءً على المعلومات التالية، أجب على السؤال:
                
                السؤال: {question}
                
                المعلومات المتاحة:
                {combined_content}
                
                قدم إجابة مفصلة ومفيدة بالعربية.
                """
                
                response = self.gemini_text_model.generate_content(prompt)
                return response.text
            
            return None
            
        except Exception as e:
            # في حالة الخطأ، استخدم البحث البسيط
            question_words = question.lower().split()
            data_lower = data_content.lower()
            
            found_words = [word for word in question_words if word in data_lower]
            if len(found_words) >= 2:
                lines = data_content.split('\n')
                relevant_lines = []
                for line in lines:
                    if any(word in line.lower() for word in question_words):
                        relevant_lines.append(line)
                
                if relevant_lines:
                    return '\n'.join(relevant_lines[:5])
            
            return None
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """إنشاء ملخص للنص"""
        try:
            prompt = f"""
            اكتب ملخصاً موجزاً للنص التالي في حدود {max_length} كلمة:
            
            {text}
            
            الملخص يجب أن يكون باللغة العربية ويحتوي على النقاط الأساسية.
            """
            
            response = self.gemini_text_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"حدث خطأ في إنشاء الملخص: {str(e)}"
    
    def translate_text(self, text: str, target_language: str = "ar") -> str:
        """ترجمة النص"""
        try:
            prompt = f"""
            ترجم النص التالي إلى {'العربية' if target_language == 'ar' else 'الإنجليزية'}:
            
            {text}
            """
            
            response = self.gemini_text_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"حدث خطأ في الترجمة: {str(e)}"

