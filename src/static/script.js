// متغيرات عامة
let selectedImage = null;
let isImageUploadVisible = false;
let isMediaOptionsVisible = false;

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    loadDataFiles();
    autoResizeTextarea();
});

// إدارة تغيير حجم textarea
function autoResizeTextarea() {
    const textarea = document.getElementById('messageInput');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

// معالجة الضغط على المفاتيح
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// إرسال رسالة
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message && !selectedImage) {
        return;
    }
    
    // إضافة رسالة المستخدم
    addMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // إخفاء خيارات الرفع
    hideUploadOptions();
    
    // إظهار مؤشر التحميل
    showLoading('جاري معالجة سؤالك...');
    
    try {
        let response;
        
        if (selectedImage) {
            // إرسال مع صورة
            response = await sendMessageWithImage(message, selectedImage);
            selectedImage = null;
            document.getElementById('imagePreview').innerHTML = '';
        } else {
            // إرسال نص فقط
            response = await sendTextMessage(message);
        }
        
        // إضافة رد البوت
        addMessage(response.answer, 'bot', response.source);
        
        // إضافة تحليل الصورة إن وجد
        if (response.image_analysis) {
            addMessage(`تحليل الصورة: ${response.image_analysis}`, 'bot', 'image_analysis');
        }
        
    } catch (error) {
        addMessage('عذراً، حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.', 'bot', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// إرسال رسالة نصية
async function sendTextMessage(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message })
    });
    
    if (!response.ok) {
        throw new Error('فشل في إرسال الرسالة');
    }
    
    return await response.json();
}

// إرسال رسالة مع صورة
async function sendMessageWithImage(message, imageFile) {
    const formData = new FormData();
    formData.append('question', message);
    formData.append('image', imageFile);
    
    const response = await fetch('/api/chat/image', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error('فشل في إرسال الرسالة مع الصورة');
    }
    
    return await response.json();
}

// إضافة رسالة للشات
function addMessage(content, sender, source = '') {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = sender === 'user' ? 'user-avatar' : 'bot-avatar-small';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = formatMessage(content);
    
    // إضافة مصدر الإجابة
    if (source && sender === 'bot') {
        const sourceDiv = document.createElement('div');
        sourceDiv.className = 'message-source';
        sourceDiv.innerHTML = getSourceLabel(source);
        bubble.appendChild(sourceDiv);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// تنسيق الرسالة
function formatMessage(content) {
    // تحويل الروابط إلى روابط قابلة للنقر
    content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // تحويل النص إلى فقرات
    content = content.replace(/\n/g, '<br>');
    
    return content;
}

// الحصول على تسمية المصدر
function getSourceLabel(source) {
    const labels = {
        'local_data': '<i class="fas fa-database"></i> من البيانات المحلية',
        'deepseek': '<i class="fas fa-brain"></i> من الذكاء الاصطناعي',
        'gemini_with_image': '<i class="fas fa-image"></i> تحليل الصورة',
        'not_relevant': '<i class="fas fa-exclamation-triangle"></i> خارج المنهج',
        'error': '<i class="fas fa-exclamation-circle"></i> خطأ'
    };
    
    return `<small style="opacity: 0.7; margin-top: 0.5rem; display: block;">${labels[source] || source}</small>`;
}

// تبديل عرض رفع الصور
function toggleImageUpload() {
    const uploadArea = document.getElementById('imageUploadArea');
    const mediaOptions = document.getElementById('mediaOptions');
    
    isImageUploadVisible = !isImageUploadVisible;
    uploadArea.style.display = isImageUploadVisible ? 'block' : 'none';
    
    if (isImageUploadVisible) {
        mediaOptions.style.display = 'none';
        isMediaOptionsVisible = false;
    }
}

// تبديل عرض خيارات الوسائط
function toggleMediaGeneration() {
    const mediaOptions = document.getElementById('mediaOptions');
    const uploadArea = document.getElementById('imageUploadArea');
    
    isMediaOptionsVisible = !isMediaOptionsVisible;
    mediaOptions.style.display = isMediaOptionsVisible ? 'flex' : 'none';
    
    if (isMediaOptionsVisible) {
        uploadArea.style.display = 'none';
        isImageUploadVisible = false;
    }
}

// إخفاء خيارات الرفع
function hideUploadOptions() {
    document.getElementById('imageUploadArea').style.display = 'none';
    document.getElementById('mediaOptions').style.display = 'none';
    isImageUploadVisible = false;
    isMediaOptionsVisible = false;
}

// معالجة اختيار الصورة
function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file) {
        selectedImage = file;
        
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            preview.innerHTML = `
                <img src="${e.target.result}" alt="معاينة الصورة">
                <p>تم اختيار: ${file.name}</p>
            `;
        };
        reader.readAsDataURL(file);
    }
}

// إنشاء صوت
async function generateAudio() {
    const messageInput = document.getElementById('messageInput');
    const topic = messageInput.value.trim();
    
    if (!topic) {
        alert('يرجى كتابة الموضوع المراد إنشاء شرح صوتي له');
        return;
    }
    
    showLoading('جاري إنشاء الشرح الصوتي...');
    
    try {
        const response = await fetch('/api/generate/audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });
        
        if (!response.ok) {
            throw new Error('فشل في إنشاء الصوت');
        }
        
        const result = await response.json();
        
        if (result.status === 'generated') {
            addAudioMessage(result);
            messageInput.value = '';
            hideUploadOptions();
        } else {
            throw new Error(result.error || 'فشل في إنشاء الصوت');
        }
        
    } catch (error) {
        addMessage('عذراً، حدث خطأ في إنشاء الشرح الصوتي.', 'bot', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// إنشاء فيديو
async function generateVideo() {
    const messageInput = document.getElementById('messageInput');
    const topic = messageInput.value.trim();
    
    if (!topic) {
        alert('يرجى كتابة الموضوع المراد إنشاء شرح مرئي له');
        return;
    }
    
    showLoading('جاري إنشاء الشرح المرئي...');
    
    try {
        const response = await fetch('/api/generate/video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });
        
        if (!response.ok) {
            throw new Error('فشل في إنشاء الفيديو');
        }
        
        const result = await response.json();
        
        if (result.status === 'generated') {
            addVideoMessage(result);
            messageInput.value = '';
            hideUploadOptions();
        } else {
            throw new Error(result.error || 'فشل في إنشاء الفيديو');
        }
        
    } catch (error) {
        addMessage('عذراً، حدث خطأ في إنشاء الشرح المرئي.', 'bot', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// إضافة رسالة صوتية
function addAudioMessage(result) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const avatar = document.createElement('div');
    avatar.className = 'bot-avatar-small';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = `
        <h4>${result.title}</h4>
        <div class="media-content">
            <audio controls>
                <source src="${result.audio_url}" type="audio/mpeg">
                متصفحك لا يدعم تشغيل الصوت.
            </audio>
        </div>
        <p><strong>النص:</strong></p>
        <p>${result.script}</p>
        <small style="opacity: 0.7; margin-top: 0.5rem; display: block;">
            <i class="fas fa-microphone"></i> تم إنشاؤه تلقائياً
        </small>
    `;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// إضافة رسالة فيديو
function addVideoMessage(result) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const avatar = document.createElement('div');
    avatar.className = 'bot-avatar-small';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    // التحقق من نوع الوسائط المُنشأة
    if (result.video_url && result.video_url.includes('.mp4')) {
        bubble.innerHTML = `
            <h4>${result.title}</h4>
            <div class="media-content">
                <video controls>
                    <source src="${result.video_url}" type="video/mp4">
                    متصفحك لا يدعم تشغيل الفيديو.
                </video>
            </div>
            <p><strong>النص:</strong></p>
            <p>${result.script}</p>
            <small style="opacity: 0.7; margin-top: 0.5rem; display: block;">
                <i class="fas fa-video"></i> تم إنشاؤه تلقائياً
            </small>
        `;
    } else {
        // في حالة عدم توفر الفيديو، عرض الصوت
        bubble.innerHTML = `
            <h4>${result.title}</h4>
            <div class="media-content">
                <audio controls>
                    <source src="${result.video_url}" type="audio/mpeg">
                    متصفحك لا يدعم تشغيل الصوت.
                </audio>
            </div>
            <p><strong>النص:</strong></p>
            <p>${result.script}</p>
            <small style="opacity: 0.7; margin-top: 0.5rem; display: block;">
                <i class="fas fa-microphone"></i> تم إنشاء شرح صوتي (الفيديو غير متاح حالياً)
            </small>
        `;
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// إظهار مؤشر التحميل
function showLoading(text = 'جاري المعالجة...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    loadingText.textContent = text;
    overlay.style.display = 'flex';
}

// إخفاء مؤشر التحميل
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// عرض مدير البيانات
function showDataManager() {
    document.getElementById('dataManagerModal').style.display = 'flex';
    loadDataFiles();
}

// عرض المساعدة
function showHelp() {
    document.getElementById('helpModal').style.display = 'flex';
}

// إغلاق النافذة المنبثقة
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// رفع ملف بيانات
async function uploadDataFile() {
    const fileInput = document.getElementById('dataFileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        return;
    }
    
    if (!file.name.endsWith('.txt')) {
        alert('يرجى اختيار ملف نصي (.txt) فقط');
        return;
    }
    
    showLoading('جاري رفع الملف...');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/upload/data', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('فشل في رفع الملف');
        }
        
        const result = await response.json();
        alert('تم رفع الملف بنجاح!');
        
        // إعادة تحميل قائمة الملفات
        loadDataFiles();
        
        // مسح اختيار الملف
        fileInput.value = '';
        
    } catch (error) {
        alert('حدث خطأ في رفع الملف: ' + error.message);
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// تحميل قائمة ملفات البيانات
async function loadDataFiles() {
    try {
        const response = await fetch('/api/data/files');
        if (!response.ok) {
            throw new Error('فشل في تحميل قائمة الملفات');
        }
        
        const result = await response.json();
        const filesList = document.getElementById('dataFilesList');
        
        if (result.files && result.files.length > 0) {
            filesList.innerHTML = result.files.map(file => `
                <div class="file-item">
                    <div class="file-info">
                        <i class="fas fa-file-text"></i>
                        <span>${file.name}</span>
                    </div>
                    <span class="file-size">${formatFileSize(file.size)}</span>
                </div>
            `).join('');
        } else {
            filesList.innerHTML = '<p style="color: #6b7280; text-align: center;">لا توجد ملفات مرفوعة</p>';
        }
        
    } catch (error) {
        console.error('Error loading files:', error);
        const filesList = document.getElementById('dataFilesList');
        filesList.innerHTML = '<p style="color: #ef4444; text-align: center;">خطأ في تحميل الملفات</p>';
    }
}

// تنسيق حجم الملف
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// إغلاق النوافذ المنبثقة عند النقر خارجها
document.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (event.target === loadingOverlay) {
        // لا نغلق overlay التحميل عند النقر عليه
    }
});

