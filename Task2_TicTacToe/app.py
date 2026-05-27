import streamlit as st

st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="♟️", layout="centered")

# Minimax Algorithm
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "O": return 1
    if winner == "X": return -1
    if " " not in board: return 0

    if is_maximizing:
        best = -1000
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                best = max(best, minimax(board, depth+1, False))
                board[i] = " "
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                best = min(best, minimax(board, depth+1, True))
                board[i] = " "
        return best

def best_move(board):
    best_val = -1000
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            move_val = minimax(board, 0, False)
            board[i] = " "
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None

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
        background: linear-gradient(90deg, #34d399, #60a5fa, #a78bfa);
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
        margin-bottom: 15px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(52,211,153,0); }
        100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
    }
    .game-status {
        text-align: center;
        padding: 15px 25px;
        border-radius: 15px;
        margin: 15px 0;
        font-size: 1.2em;
        font-weight: 700;
        animation: fadeIn 0.5s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .status-playing {
        background: rgba(96,165,250,0.1);
        border: 1px solid rgba(96,165,250,0.3);
        color: #60a5fa;
    }
    .status-win {
        background: rgba(52,211,153,0.1);
        border: 2px solid rgba(52,211,153,0.5);
        color: #34d399;
    }
    .status-lose {
        background: rgba(239,68,68,0.1);
        border: 2px solid rgba(239,68,68,0.5);
        color: #f87171;
    }
    .status-draw {
        background: rgba(251,191,36,0.1);
        border: 2px solid rgba(251,191,36,0.5);
        color: #fbbf24;
    }
    .score-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .score-number {
        font-size: 2.5em;
        font-weight: 800;
    }
    .score-label {
        color: #94a3b8;
        font-size: 0.8em;
        margin-top: 5px;
    }
    div[data-testid="stButton"] button {
        border-radius: 15px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
    }
    div[data-testid="stButton"] button:hover {
        transform: scale(1.05) !important;
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
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">🤖 Minimax AI</div>
    <h1>♟️ Tic-Tac-Toe AI</h1>
    <p style="color:#94a3b8; font-size:1em;">Play against an unbeatable AI powered by Minimax algorithm!</p>
    <p style="color:#34d399; font-size:0.85em; font-weight:600;">
        Akshat Anand &nbsp;|&nbsp; CodSoft AI Internship 2026
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize state
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status" not in st.session_state:
    st.session_state.status = "your_turn"
if "scores" not in st.session_state:
    st.session_state.scores = {"player": 0, "ai": 0, "draws": 0}

board = st.session_state.board

# Scores
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="score-card">
        <div class="score-number" style="color:#60a5fa;">
            {st.session_state.scores['player']}
        </div>
        <div class="score-label">👤 You (X)</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="score-card">
        <div class="score-number" style="color:#fbbf24;">
            {st.session_state.scores['draws']}
        </div>
        <div class="score-label">🤝 Draws</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="score-card">
        <div class="score-number" style="color:#f87171;">
            {st.session_state.scores['ai']}
        </div>
        <div class="score-label">🤖 AI (O)</div>
    </div>
    """, unsafe_allow_html=True)

# Status
winner = check_winner(board)
if winner == "X":
    st.session_state.scores["player"] += 1
    st.session_state.game_over = True
    st.markdown('<div class="game-status status-win">🎉 You Win! Amazing!</div>', unsafe_allow_html=True)
elif winner == "O":
    st.session_state.scores["ai"] += 1
    st.session_state.game_over = True
    st.markdown('<div class="game-status status-lose">🤖 AI Wins! Try again!</div>', unsafe_allow_html=True)
elif " " not in board:
    st.session_state.scores["draws"] += 1
    st.session_state.game_over = True
    st.markdown('<div class="game-status status-draw">🤝 It\'s a Draw!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="game-status status-playing">👤 Your turn! You are X</div>', unsafe_allow_html=True)

# Board
st.markdown("<br>", unsafe_allow_html=True)
for row in range(3):
    cols = st.columns([1,3,3,3,1])
    for col_idx, col in enumerate([1, 2, 3]):
        idx = row * 3 + (col - 1)
        with cols[col]:
            cell = board[idx]
            if cell == " " and not st.session_state.game_over:
                if st.button("　", key=f"cell_{idx}", use_container_width=True):
                    board[idx] = "X"
                    if not check_winner(board) and " " in board:
                        ai_idx = best_move(board)
                        board[ai_idx] = "O"
                    st.rerun()
            else:
                color = "#60a5fa" if cell == "X" else "#f87171" if cell == "O" else "#475569"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); border:2px solid rgba(255,255,255,0.1);
                border-radius:15px; padding:20px; text-align:center; font-size:2em; 
                font-weight:800; color:{color}; min-height:80px; display:flex; 
                align-items:center; justify-content:center;">
                    {cell if cell != " " else ""}
                </div>
                """, unsafe_allow_html=True)

# New Game button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔄 New Game", use_container_width=True):
        st.session_state.board = [" "] * 9
        st.session_state.game_over = False
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    Built with 🐍 Python & 🤖 Minimax Algorithm<br>
    <span style="color:#34d399; font-weight:600;">
        Akshat Anand — CodSoft AI Internship 2026
    </span>
</div>
""", unsafe_allow_html=True)