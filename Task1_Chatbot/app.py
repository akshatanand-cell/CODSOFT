import streamlit as st
import re
import random
from datetime import datetime

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

RULES = {
    r"hello|hi|hey|howdy|hiya": [
        "Hello! How can I help you today? 😊",
        "Hey there! What can I do for you?",
        "Hi! Great to see you! How can I assist?"
    ],
    r"how are you|how r you|how are u": [
        "I'm doing great, thanks for asking! 😊",
        "I'm fantastic! Ready to help you!",
        "Feeling wonderful! How about you?"
    ],
    r"what is your name|who are you|your name": [
        "I'm RuleBot — an AI chatbot built by Akshat Anand! 🤖",
        "My name is RuleBot! Nice to meet you!",
    ],
    r"how old are you|your age": [
        "I'm ageless — I'm an AI! 😄",
        "Age is just a number for AI!"
    ],
    r"who made you|who created you|who built you": [
        "I was built by Akshat Anand — CodSoft AI Intern 2026! 🚀",
        "My creator is Akshat Anand!"
    ],
    r"weather|temperature|rain|sunny": [
        "I can't check real-time weather, but try weather.com! 🌤️",
        "For weather updates, check Google Weather!"
    ],
    r"what time|current time": [
        f"The current time is {datetime.now().strftime('%I:%M %p')}! ⏰",
    ],
    r"what date|today's date|current date": [
        f"Today is {datetime.now().strftime('%B %d, %Y')}! 📅",
    ],
    r"joke|funny|make me laugh|tell me a joke": [
        "Why don't scientists trust atoms? Because they make up everything! 😂",
        "Why did the AI go to school? To improve its neural network! 🤖😄",
        "What do you call a sleeping dinosaur? A dino-snore! 😂",
        "Why did the programmer quit? Because he didn't get arrays! 😄"
    ],
    r"what is ai|artificial intelligence|explain ai": [
        "AI is technology that enables machines to think, learn and solve problems like humans! 🤖",
        "Artificial Intelligence lets computers learn from data and make smart decisions!"
    ],
    r"what is python|tell me about python": [
        "Python is a powerful programming language used for AI, web dev & more! 🐍",
        "Python is great for AI, Data Science & automation! 🐍"
    ],
    r"help|what can you do|capabilities": [
        "I can chat about: greetings, time & date, jokes, AI, Python! 😊",
        "Ask me about AI, tell me jokes, or just have a conversation!"
    ],
    r"thank you|thanks|thank u|thx": [
        "You're welcome! Happy to help! 😊",
        "Anytime! That's what I'm here for!"
    ],
    r"bye|goodbye|see you|see ya": [
        "Goodbye! Have a great day! 👋",
        "See you later! Take care! 😊"
    ],
    r"i love you|love you|i like you": [
        "Aww that's sweet! I like you too! 😊",
        "Thanks! You made my circuits happy! 🤖❤️"
    ],
    r"i am sad|i feel sad|i'm sad|feeling sad": [
        "I'm sorry! Remember every cloud has a silver lining! 🌈",
        "Cheer up! Things will get better! 😊"
    ],
    r"i am happy|i feel happy|i'm happy|great": [
        "That's wonderful! Your happiness makes me happy! 😊🎉",
        "Yay! Keep that positive energy! 🌟"
    ],
    r"coding|programming|developer|software": [
        "Coding is amazing! It's the language of the future! 💻🚀",
        "Programming is a superpower — you can build anything! 💪"
    ],
    r"food|hungry|eat|pizza|burger": [
        "I can't eat but I hear pizza is amazing! 🍕",
        "Food is fuel! Go grab something delicious! 😋"
    ],
}

DEFAULT_RESPONSES = [
    "Interesting! Tell me more about that 🤔",
    "I'm not sure I understand. Could you rephrase that?",
    "That's a great question! I'm still learning though 😊",
    "I'm a rule-based bot — try asking about AI, jokes, or time!"
]

def get_response(user_input):
    user_input = user_input.lower().strip()
    for pattern, responses in RULES.items():
        if re.search(pattern, user_input):
            return random.choice(responses)
    return random.choice(DEFAULT_RESPONSES)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
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
        padding: 30px 20px 10px 20px;
        animation: fadeInDown 1s ease;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .hero h1 {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(90deg, #f472b6, #a78bfa, #60a5fa);
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
        background: linear-gradient(135deg, #f472b6, #a78bfa);
        color: white;
        padding: 5px 18px;
        border-radius: 50px;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 15px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244,114,182,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(244,114,182,0); }
        100% { box-shadow: 0 0 0 0 rgba(244,114,182,0); }
    }
    .chat-message-user {
        background: linear-gradient(135deg, #a78bfa, #60a5fa);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 8px 0;
        margin-left: 25%;
        font-size: 0.95em;
        line-height: 1.6;
        animation: fadeIn 0.3s ease;
    }
    .chat-message-bot {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 8px 0;
        margin-right: 25%;
        font-size: 0.95em;
        line-height: 1.6;
        animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-label-user {
        text-align: right;
        color: #a78bfa;
        font-size: 0.75em;
        font-weight: 600;
        margin-bottom: 3px;
    }
    .chat-label-bot {
        color: #60a5fa;
        font-size: 0.75em;
        font-weight: 600;
        margin-bottom: 3px;
    }
    .stButton button {
        background: linear-gradient(135deg, #f472b6, #a78bfa) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 50px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(167,139,250,0.4) !important;
    }
    .topics-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    .topic-tag {
        display: inline-block;
        background: rgba(167,139,250,0.2);
        border: 1px solid rgba(167,139,250,0.3);
        color: #a78bfa;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8em;
        margin: 4px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #475569;
        font-size: 0.85em;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTextInput input {
        background: rgba(255,255,255,0.07) !important;
        border: 2px solid rgba(167,139,250,0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 15px 25px !important;
    }
    .stTextInput input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 20px rgba(167,139,250,0.3) !important;
    }
    .stTextInput label { color: #94a3b8 !important; }
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="badge">🤖 Rule-Based AI</div>
    <h1>🤖 RuleBot</h1>
    <p style="color:#94a3b8; font-size:1em;">A smart chatbot powered by pattern matching & rules</p>
    <p style="color:#f472b6; font-size:0.85em; font-weight:600;">
        Akshat Anand &nbsp;|&nbsp; CodSoft AI Internship 2026
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topics-card">
    <div style="color:#94a3b8; font-size:0.8em; font-weight:600;
    letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">
        💬 I can talk about:
    </div>
    <span class="topic-tag">👋 Greetings</span>
    <span class="topic-tag">😄 Jokes</span>
    <span class="topic-tag">⏰ Time & Date</span>
    <span class="topic-tag">🤖 About AI</span>
    <span class="topic-tag">🐍 Python</span>
    <span class="topic-tag">😊 Feelings</span>
    <span class="topic-tag">🌤️ Weather</span>
    <span class="topic-tag">👨‍💻 Coding</span>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "bot",
        "content": "Hello! I'm RuleBot 🤖 Ask me anything! Type 'help' to see what I can do!"
    }]

for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"""
        <div class="chat-label-user">You 👤</div>
        <div class="chat-message-user">{chat["content"]}</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-label-bot">🤖 RuleBot</div>
        <div class="chat-message-bot">{chat["content"]}</div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your message:", 
        placeholder="Say hello, ask a joke, or ask about AI...")
    send_btn = st.form_submit_button("🚀 Send Message")

col4, col5, col6 = st.columns([1,2,1])
with col5:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [{
            "role": "bot",
            "content": "Hello! I'm RuleBot 🤖 Ask me anything!"
        }]
        st.rerun()

if send_btn and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    response = get_response(user_input)
    st.session_state.chat_history.append({"role": "bot", "content": response})
    st.rerun()

st.markdown("""
<div class="footer">
    Built with 🐍 Python & Rule-Based AI<br>
    <span style="color:#f472b6; font-weight:600;">
        Akshat Anand — CodSoft AI Internship 2026
    </span>
</div>
""", unsafe_allow_html=True)