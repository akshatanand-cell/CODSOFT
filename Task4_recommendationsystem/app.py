import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Movie Recommender", page_icon="🎬", layout="centered")

# Movie Dataset
movies = pd.DataFrame({
    'title': [
        'The Dark Knight', 'Inception', 'Interstellar', 'The Matrix',
        'Avengers Endgame', 'Iron Man', 'Thor', 'Black Panther',
        'The Godfather', 'Pulp Fiction', 'Fight Club', 'Goodfellas',
        'Titanic', 'Avatar', 'Forrest Gump', 'The Lion King',
        'Harry Potter', 'Lord of the Rings', 'Star Wars', 'Jurassic Park',
        'The Shawshank Redemption', 'Schindlers List', 'The Silence of the Lambs',
        'Gladiator', 'Braveheart', 'Troy', '300',
        'The Social Network', 'The Wolf of Wall Street', 'Whiplash',
        'La La Land', 'A Beautiful Mind', 'Good Will Hunting',
        'Spider-Man', 'Batman Begins', 'Wonder Woman',
        'Toy Story', 'Finding Nemo', 'The Incredibles', 'Up',
        'Get Out', 'Us', 'A Quiet Place', 'It',
        'Parasite', 'Joker', 'Logan', 'Deadpool'
    ],
    'genre': [
        'action crime drama thriller', 'action sci-fi thriller mystery',
        'sci-fi drama adventure space', 'sci-fi action thriller',
        'action adventure sci-fi superhero', 'action adventure sci-fi superhero',
        'action adventure fantasy superhero', 'action adventure sci-fi superhero',
        'crime drama thriller', 'crime drama thriller',
        'drama thriller mystery', 'crime drama thriller',
        'romance drama history', 'sci-fi action adventure fantasy',
        'drama romance comedy', 'animation adventure drama',
        'fantasy adventure family', 'fantasy adventure action',
        'sci-fi action adventure', 'sci-fi adventure thriller',
        'drama', 'drama history war', 'thriller crime horror',
        'action drama history', 'action drama history war',
        'action drama history', 'action drama history',
        'drama biography', 'biography comedy crime drama',
        'drama music', 'drama romance music', 'drama biography',
        'drama romance', 'action adventure sci-fi superhero',
        'action adventure superhero', 'action adventure superhero',
        'animation comedy adventure family', 'animation adventure comedy family',
        'animation action adventure family', 'animation adventure comedy family',
        'horror thriller mystery', 'horror thriller mystery',
        'horror thriller sci-fi', 'horror thriller',
        'drama thriller', 'crime drama thriller',
        'action sci-fi superhero drama', 'action comedy superhero'
    ],
    'rating': [
        9.0, 8.8, 8.6, 8.7, 8.4, 7.9, 7.9, 7.3,
        9.2, 8.9, 8.8, 8.7, 7.9, 7.9, 8.8, 8.5,
        7.6, 8.9,8.6, 8.1, 9.3, 9.0, 8.6, 8.5,
        8.3, 7.3, 7.7, 7.7, 8.2, 8.5, 8.0, 8.2,
        8.3, 7.4, 8.2, 7.4, 8.3, 8.1, 8.0, 8.2,
        7.7, 6.8, 7.5, 6.9, 8.6, 8.4, 8.1, 8.0
    ],
    'year': [
        2008, 2010, 2014, 1999, 2019, 2008, 2011, 2018,
        1972, 1994, 1999, 1990, 1997, 2009, 1994, 1994,
        2001, 2001, 1977, 1993, 1994, 1993, 1991, 2000,
        1995, 2004, 2006, 2010, 2013, 2014, 2016, 2001,
        1997, 2002, 2005, 2017, 1995, 2003, 2004, 2009,
        2017, 2019, 2018, 2017, 2019, 2019, 2017, 2016
    ]
})

# Build recommendation engine
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genre'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, n=5):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx][:n]
    movie_indices = [s[0] for s in sim_scores]
    scores = [s[1] for s in sim_scores]
    result = movies.iloc[movie_indices][['title', 'genre', 'rating', 'year']].copy()
    result['match'] = [round(s * 100, 1) for s in scores]
    return result

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(-45deg, #1a0533, #0d1b4b, #1a0a2e, #0a1a1a);
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
        background: linear-gradient(90deg, #f472b6, #fbbf24, #34d399);
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
        background: linear-gradient(135deg, #f472b6, #fbbf24);
        color: white;
        padding: 5px 18px;
        border-radius: 50px;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244,114,182,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(244,114,182,0); }
        100% { box-shadow: 0 0 0 0 rgba(244,114,182,0); }
    }
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
    }
    .movie-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        animation: slideUp 0.5s ease;
        transition: all 0.3s ease;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .movie-title {
        color: white;
        font-size: 1.1em;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .movie-meta {
        color: #94a3b8;
        font-size: 0.85em;
        margin: 3px 0;
    }
    .match-bar-container {
        background: rgba(255,255,255,0.1);
        border-radius: 50px;
        height: 8px;
        margin-top: 10px;
        overflow: hidden;
    }
    .match-bar {
        height: 100%;
        border-radius: 50px;
        background: linear-gradient(90deg, #f472b6, #fbbf24);
        transition: width 1s ease;
    }
    .stButton button {
        background: linear-gradient(135deg, #f472b6, #fbbf24) !important;
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
        box-shadow: 0 15px 35px rgba(244,114,182,0.4) !important;
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
        background: linear-gradient(90deg, #f472b6, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.8em;
        margin-top: 5px;
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
    .stSelectbox label { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">🤖 Content-Based Filtering AI</div>
    <h1>🎬 Movie Recommender</h1>
    <p style="color:#94a3b8; font-size:1.1em;">
        AI that recommends movies based on your taste!
    </p>
    <p style="color:#f472b6; font-size:0.9em; font-weight:600;">
        Akshat Anand &nbsp;|&nbsp; CodSoft AI Internship 2026
    </p>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-number">{len(movies)}</div>
        <div class="stat-label">Movies</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">TF-IDF</div>
        <div class="stat-label">AI Algorithm</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">∞</div>
        <div class="stat-label">Recommendations</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input
st.markdown('<div class="card">', unsafe_allow_html=True)
selected_movie = st.selectbox(
    "🎬 Select a movie you like:",
    sorted(movies['title'].tolist())
)
num_recommendations = st.slider("📊 Number of recommendations:", 3, 10, 5)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    recommend_btn = st.button("🎯 Get AI Recommendations")

if recommend_btn:
    recommendations = get_recommendations(selected_movie, num_recommendations)

    st.markdown(f"""
    <div style="text-align:center; color:#34d399; padding:15px;
    background:rgba(52,211,153,0.1); border-radius:15px; margin:15px 0;
    font-weight:600; font-size:1.1em;">
        ✅ Found {len(recommendations)} movies similar to "{selected_movie}"!
    </div>
    """, unsafe_allow_html=True)

    for i, (_, row) in enumerate(recommendations.iterrows()):
        genres = row['genre'].replace(' ', ' • ')
        st.markdown(f"""
        <div class="movie-card">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div>
                    <div class="movie-title">
                        #{i+1} &nbsp; 🎬 {row['title']}
                    </div>
                    <div class="movie-meta">⭐ Rating: {row['rating']}/10</div>
                    <div class="movie-meta">📅 Year: {row['year']}</div>
                    <div class="movie-meta">🎭 {genres}</div>
                </div>
                <div style="text-align:right; min-width:80px;">
                    <div style="color:#f472b6; font-size:1.4em; font-weight:800;">
                        {row['match']}%
                    </div>
                    <div style="color:#94a3b8; font-size:0.75em;">Match</div>
                </div>
            </div>
            <div class="match-bar-container">
                <div class="match-bar" style="width:{row['match']}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Built with 🐍 Python | 🤖 TF-IDF & Cosine Similarity AI<br>
    <span style="color:#f472b6; font-weight:600;">
        Akshat Anand — CodSoft AI Internship 2026
    </span>
</div>
""", unsafe_allow_html=True)