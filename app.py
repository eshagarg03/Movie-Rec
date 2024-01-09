import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Set page title and favicon
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# Custom CSS for better styling
st.markdown(
    """
    <style>
        .main {
            padding: 20px;
        }
        .header {
            font-size: 30px;
            color: #0066cc;
            text-align: center;
        }
        .button {
            margin-top: 20px;
        }
        .recommendation-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        .recommendation-card {
            text-align: center;
            margin: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .movie-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("<h1 class='header'>Movie Recommender System</h1>", unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation', key="recommendation_button"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names and recommended_movie_posters:
        st.markdown("<h2>Recommended Movies</h2>", unsafe_allow_html=True)
        st.markdown(
            "<div class='recommendation-container'>",
            unsafe_allow_html=True
        )

        for i in range(len(recommended_movie_names)):
            st.markdown(
                f"""
                <div class='recommendation-card'>
                    <p class='movie-title'>{recommended_movie_names[i]}</p>
                    <img src='{recommended_movie_posters[i]}' alt='movie poster' style='width: 150px; height: 200px;'>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("No recommendations available. Please try a different movie.")

