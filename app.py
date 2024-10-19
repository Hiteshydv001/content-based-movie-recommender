import pickle
import streamlit as st
import requests

# Fetch movie poster and details
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    description = data['overview']
    rating = data['vote_average']
    return poster_path, description, rating

# Recommender system function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    recommended_movie_ratings = []
    
    # Get the top 10 recommendations
    for i in distances[1:11]:  # Change here to get the top 10 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        poster, description, rating = fetch_movie_details(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_descriptions.append(description)
        recommended_movie_ratings.append(rating)
    
    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions, recommended_movie_ratings

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))

# The commented code block you provided is a function that decompresses a pickled object stored in a
# gzip-compressed file. Here's a breakdown of what each part of the code does:
import gzip
import pickle

def decompress_pickle_gzip(file):
    with gzip.open(file, 'rb') as f:
        return pickle.load(f)

similarity = decompress_pickle_gzip('similarity.pkl.gz')


# Set up Streamlit page
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom CSS for modern UI design
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #764BA2, #667EEA);  /* Gradient background */
        padding: 2rem;
        height: 100vh;  /* Full height for gradient */
        color: white;   /* Default text color */
    }
    .movie-card {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .movie-title {
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        color: #1e3c72; /* Dark text color for contrast */
    }
    .movie-desc {
        font-size: 0.9rem;
        text-align: justify;
        margin-bottom: 5px;
    }
    .star-rating {
        text-align: center;
        font-size: 1rem;
        color: gold;
    }
    .header-section {
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .header-section h1 {
        font-size: 3rem;
    }
    .header-section p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: auto;
        opacity: 0.8;
    }
    .recommend-button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header with project explanation
st.markdown("""
    <div class="header-section">
        <h1>🎬 Movie Recommender System</h1>
        <p>
            Welcome to the Movie Recommender System! This project provides personalized movie recommendations 
            based on your favorite films. Powered by the TMDB API, it uses movie metadata to suggest films 
            similar to the one you select. Simply choose a movie and see our recommendations.
        </p>
    </div>
""", unsafe_allow_html=True)

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎥 Type or select a movie to get recommendations",
    movie_list,
    help="Select a movie to get personalized recommendations."
)

# Display recommendations
if st.button('Show Recommendation', key='recommend', help="Click to see similar movies"):
    st.markdown("<h3 style='color: white;'>Recommended Movies:</h3>", unsafe_allow_html=True)
    recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions, recommended_movie_ratings = recommend(selected_movie)
    
    # Create two rows of columns for displaying 10 movies
    cols = st.columns(5, gap="large")
    
    # First row (first 5 movies)
    for idx, col in enumerate(cols):
        with col:
            if idx < 5:  # First 5 movies
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(recommended_movie_posters[idx], width=150, use_column_width="always")
                st.markdown(f'<div class="movie-title">🎥 {recommended_movie_names[idx]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="movie-desc">{recommended_movie_descriptions[idx][:100]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="star-rating">⭐ {recommended_movie_ratings[idx]}/10</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)  # Close movie card div

    # Second row (next 5 movies)
    cols = st.columns(5, gap="large")
    
    for idx, col in enumerate(cols):
        with col:
            if idx + 5 < len(recommended_movie_names):  # Check to avoid index out of range
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(recommended_movie_posters[idx + 5], width=150, use_column_width="always")
                st.markdown(f'<div class="movie-title">🎥 {recommended_movie_names[idx + 5]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="movie-desc">{recommended_movie_descriptions[idx + 5][:100]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="star-rating">⭐ {recommended_movie_ratings[idx + 5]}/10</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)  # Close movie card div

# Footer with GitHub and X.com social icons
st.markdown("""
    <style>
    .footer {
        font-size: 0.85rem;
        margin-top: 3rem;
        text-align: center;
        color: #888;
    }
    .social-icons {
        font-size: 1.5rem;
    }
    .social-icons a {
        margin: 0 10px;
        color: inherit;
        text-decoration: none;
    }
    </style>
    <div class="footer">
        <div class="social-icons">
            <a href="https://github.com/Hiteshydv001" target="_blank">🐱‍💻 GitHub</a>
            <a href="https://x.com/Hitesh_0003" target="_blank">🐦 X.com</a>
        </div>
        Made with 💖 using Streamlit and TMDB API
    </div>
""", unsafe_allow_html=True)
