import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="AI Face Detection", page_icon="👁️", layout="centered")

# Load face detector
@st.cache_resource
def load_detector():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    return face_cascade, eye_cascade

face_cascade, eye_cascade = load_detector()

def detect_faces(image):
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    result = img_array.copy()
    face_count = 0
    eye_count = 0
    for (x, y, w, h) in faces:
        face_count += 1
        cv2.rectangle(result, (x, y), (x+w, y+h), (99, 240, 132), 3)
        cv2.putText(result, f'Face {face_count}', (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (99, 240, 132), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = result[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
        for (ex, ey, ew, eh) in eyes:
            eye_count += 1
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (96, 165, 250), 2)
    return result, face_count, eye_count

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #1a0a2e, #0a1a2e, #0f0c29);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero {
        text-align: center;
        padding: 40px 20px 20px 20px;
        animation: fadeInDown 1s ease;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .hero h1 {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(90deg, #34d399, #60a5fa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #34d399, #60a5fa);
        color: white;
        padding: 5px 18px;
        border-radius: 50px;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(52,211,153,0); }
        100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
    }
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 30px;
        margin: 15px 0;
    }
    .stButton button {
        background: linear-gradient(135deg, #34d399, #60a5fa) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 50px !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(52,211,153,0.4) !important;
    }
    .stats-row {
        display: flex;
        gap: 15px;
        margin: 20px 0;
    }
    .stat-box {
        flex: 1;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .stat-number {
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(90deg, #34d399, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.8em;
        margin-top: 5px;
    }
    .result-box {
        background: rgba(52,211,153,0.1);
        border: 2px solid rgba(52,211,153,0.3);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin: 15px 0;
        animation: slideUp 0.6s ease;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0;
        color: white;
        font-size: 0.9em;
    }
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        flex-shrink: 0;
    }
    .footer {
        text-align: center;
        padding: 30px;
        color: #475569;
        font-size: 0.85em;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">👁️ Haar Cascade AI</div>
    <h1>👁️ Face Detection AI</h1>
    <p style="color:#94a3b8; font-size:1.1em;">
        Detect and locate faces in any image using Computer Vision!
    </p>
    <p style="color:#34d399; font-size:0.9em; font-weight:600;">
        Akshat Anand &nbsp;|&nbsp; CodSoft AI Internship 2026
    </p>
</div>
""", unsafe_allow_html=True)

# Legend
st.markdown("""
<div class="card">
    <div style="color:#94a3b8; font-size:0.8em; font-weight:600;
    letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">
        🎨 Detection Legend
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background:#63f084;"></div>
        <div>Green box = Face detected</div>
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background:#60a5fa;"></div>
        <div>Blue box = Eyes detected</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📤 Upload an image with faces:",
    type=['jpg', 'jpeg', 'png'],
    help="Upload any image and AI will detect all faces!"
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, use_column_width=True, caption="Original Image")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        detect_btn = st.button("👁️ Detect Faces with AI")

    if detect_btn:
        with st.spinner("🤖 AI is scanning for faces..."):
            result_img, face_count, eye_count = detect_faces(image)

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-number">{face_count}</div>
                <div class="stat-label">Faces Detected</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{eye_count}</div>
                <div class="stat-label">Eyes Detected</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">Haar</div>
                <div class="stat-label">AI Model</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if face_count > 0:
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size:3em;">👥</div>
                <div style="color:#34d399; font-size:1.3em; font-weight:700; margin-top:5px;">
                    {face_count} Face{'s' if face_count > 1 else ''} Found!
                </div>
                <div style="color:#94a3b8; font-size:0.9em; margin-top:5px;">
                    AI successfully detected all faces in the image
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#f87171; padding:20px;
            background:rgba(239,68,68,0.1); border-radius:15px; margin:15px 0;">
                😕 No faces detected. Try a clearer image with visible faces!
            </div>
            """, unsafe_allow_html=True)

        st.image(result_img, use_column_width=True, caption="AI Detection Result")

# Footer
st.markdown("""
<div class="footer">
    Built with 🐍 Python | 👁️ OpenCV Haar Cascades | 🤖 Computer Vision<br>
    <span style="color:#34d399; font-weight:600;">
        Akshat Anand — CodSoft AI Internship 2026
    </span>
</div>
""", unsafe_allow_html=True)