import streamlit as st
import pickle
import requests
import time

# Fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.markdown("""
    <style>
    body {
        background-color: #141414;
        color: white;
        font-family: Arial, sans-serif;
    }
    .header {
        font-size:50px;
        color:#E50914;
        text-align:center;
        padding:10px;
        font-weight:bold;
        text-transform:uppercase;
        margin-bottom:50px;
    }
    .stSelectbox, .stButton {
        background-color: #333;
        color: white;
    }
    .stButton > button {
        background-color: #E50914;
        color: white;
        font-size: 16px;
        border-radius: 5px;
        transition: 0.3s;
        padding: 10px;
        width: 100%;
    }

    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header">Movie Recommender System</div>', unsafe_allow_html=True)

# Movie dropdown selection
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Show recommendations with animation
if st.button("Show Recommend"):
    with st.spinner('Fetching movie data...'):
        time.sleep(2)  # simulate a delay for loading
        movie_names, movie_posters = recommend(selectvalue)
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.markdown(f"<div class='fadeIn'>{movie_names[i]}</div>", unsafe_allow_html=True)
                st.image(movie_posters[i])

# Feedback section
st.text_area("How did you like the recommendations?", "")
if st.button("Submit Feedback"):
    st.success("Thank you for your feedback!")

st.markdown("""
    <div class="footer">
        Made with 🧠 by Pradeep Singh Sengar
    </div>
    """, unsafe_allow_html=True)