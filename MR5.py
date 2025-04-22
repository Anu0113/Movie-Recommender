import streamlit as st
import pickle
import pandas as pd
import requests
import time

def set_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_url}) no-repeat center center fixed;
            background-size: cover;
        }}
        .center-text {{
            text-align: center;
            color: white;
        }}
        .highlight-box {{
            background-color: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
        }}
        .back-arrow {{
            font-size: 25px;
            cursor: pointer;
        }}
        .white-text {{
            color: white;
        }}
        .spinner-text {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "welcome"

def go_to_recommender():
    st.session_state.page = "recommender"

def go_to_welcome():
    st.session_state.page = "welcome"

# ---------- WELCOME PAGE ----------
if st.session_state.page == "welcome":
    set_bg_image("https://genotipia.com/wp-content/uploads/2020/04/Netflix-Background-prueba-1.jpg")

    st.markdown(
        '<div class="highlight-box"><h1 class="center-text" style="color: white;">🎬 Welcome to the Movie Recommender System! 🍿</h1></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="center-text">Discover your next favorite movie with our AI-powered recommendation engine.</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎥 Click Here to Get Started 🎥"):
            go_to_recommender()
            st.rerun()

    st.stop()

# ---------- RECOMMENDER PAGE ----------
set_bg_image("https://www.itl.cat/pngfile/big/46-465731_streaming-movies.jpg")

# Load movie data
movie_list_dict = pickle.load(open('movie_list_dict.pkl', 'rb'))
movie_list = pd.DataFrame(movie_list_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        )
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500?text=No+Image+Available"
    except Exception as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500?text=Error+Loading+Image"

def recommend(movie):
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[index]
    movie_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list1:
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

if st.button("⬅️ Back to Home Page"):
    go_to_welcome()
    st.rerun()

st.markdown('<h1 class="center-text" style="color: white;">Movie Recommender System</h1>', unsafe_allow_html=True)

st.markdown('<p style="color: white;">INTERESTING MOVIES ?</p>', unsafe_allow_html=True)
selected_movie_name = st.selectbox(
    '',
    movie_list['title'].values
)

if st.button('Recommend'):
    with st.spinner("Fetching recommendations..."):
        time.sleep(2)
        names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    for col, name, poster in zip([col1, col2, col3, col4, col5], names, posters):
        with col:
            st.markdown(f'<p class="white-text">{name}</p>', unsafe_allow_html=True)
            st.image(poster)