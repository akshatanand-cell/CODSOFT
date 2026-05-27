from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import streamlit as st
import torch

st.set_page_config(page_title="AI Image Captioning", page_icon="🖼️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(-45deg, #0a0a2e, #1a0a3e, #0d1b4b, #0a0a2e);
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
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
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
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        color: white;
        padding: 5px 18px;
        border-radius: 50px;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(96,165,250,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(96,165,250,0); }
        100% { box-shadow: 0 0 0 0 rgba(96,165,250,0); }
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
        background: linear-gradient(135deg, #60a5fa, #a78bfa) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 50px !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        letter-spacing: 1px !important;
    }
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(96,165,250,0.4) !important;
    }
    .caption-box {
        background: rgba(96,165,250,0.1);
        border: 2px solid rgba(96,165,250,0.4);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
    }
    .caption-text {
        color: white;
        font-size: 1.3em;
        font-weight: 600;
        line-height: 1.6;
        margin-top: 10px;
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
        font-size: 1.8em;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.8em;
        margin-top: 5px;
    }
    .how-it-works {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: white;
        font-size: 0.9em;
    }
    .step-number {
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85em;
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
    <div class="badge">🤖 Powered by BLIP AI</div>
    <h1>🖼️ AI Image Captioning</h1>
    <p style="color:#94a3b8; font-size:1.1em;">
        Computer Vision + NLP — AI that sees and describes images!
    </p>
    <p style="color:#60a5fa; font-size:0.9em; font-weight:600;">
        Akshat Anand &nbsp;|&nbsp; CodSoft AI Internship 2026
    </p>
</div>
""", unsafe_allow_html=True)

# How it works
st.markdown("""
<div class="how-it-works">
    <div style="color:#60a5fa; font-size:0.85em; font-weight:600;
    letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">
        🧠 How It Works
    </div>
    <div class="step-item">
        <div class="step-number">1</div>
        <div>Upload any image (JPG, PNG, WEBP)</div>
    </div>
    <div class="step-item">
        <div class="step-number">2</div>
        <div>BLIP AI analyzes pixels using Computer Vision</div>
    </div>
    <div class="step-item">
        <div class="step-number">3</div>
        <div>NLP model generates natural language caption</div>
    </div>
    <div class="step-item">
        <div class="step-number">4</div>
        <div>Caption displayed with confidence stats</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

with st.spinner("⏳ Loading BLIP AI model..."):
    processor, model = load_model()

st.markdown("""
<div style="text-align:center; color:#34d399; padding:10px; 
background:rgba(52,211,153,0.1); border-radius:10px; margin:10px 0;">
    ✅ AI Model Loaded Successfully!
</div>
""", unsafe_allow_html=True)

# Upload
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📤 Upload any image:",
    type=['jpg', 'jpeg', 'png', 'webp'],
    help="Upload any image and AI will generate a caption!"
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, use_column_width=True, caption="Your uploaded image")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("✨ Generate Caption with AI")

    if generate_btn:
        with st.spinner("🤖 AI is analyzing your image..."):
            inputs = processor(image, return_tensors="pt")
            with torch.no_grad():
                output = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(output[0], skip_special_tokens=True)

            words = len(caption.split())
            chars = len(caption)

            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-number">{words}</div>
                    <div class="stat-label">Words Generated</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{chars}</div>
                    <div class="stat-label">Characters</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">BLIP</div>
                    <div class="stat-label">AI Model</div>
                </div>
            </div>
            <div class="caption-box">
                <div style="color:#60a5fa; font-size:0.85em; font-weight:600;
                letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">
                    🤖 AI Generated Caption
                </div>
                <div class="caption-text">"{caption}"</div>
            </div>
            """, unsafe_allow_html=True)

            st.text_area("📋 Copy Caption:", value=caption, height=80)

# Footer
st.markdown("""
<div class="footer">
    Built with 🐍 Python | 🤖 BLIP Computer Vision | 📝 NLP<br>
    <span style="color:#60a5fa; font-weight:600;">
        Akshat Anand — CodSoft AI Internship 2026
    </span>
</div>
""", unsafe_allow_html=True)