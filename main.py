import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    api_key = '2cc84e4a5af059b119684c68da5936cd'
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id,api_key)
    response = requests.get(url)
    data = response.json()
    # st.text(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    recommended_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies_names = []
    recommended_movies_posters = []

    for i in recommended_list:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies_names.append(movies_list.iloc[i[0]].title)
        # fetch movie posters from TMDB API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies_names, recommended_movies_posters

movies_dataframe = pickle.load(open('movies_dict.pkl','rb'))
movies_list = pd.DataFrame(movies_dataframe)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'How would you like to be contacted?',
    movies_list['title'].values)

st.write('You have selected:', selected_movie)

if st.button('Recommend'):
    recommended_names, recommended_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_names[0])
        st.image(recommended_posters[0])

    with col2:
        st.text(recommended_names[1])
        st.image(recommended_posters[1])

    with col3:
        st.text(recommended_names[2])
        st.image(recommended_posters[2])

    with col4:
        st.text(recommended_names[3])
        st.image(recommended_posters[3])

    with col5:
        st.text(recommended_names[4])
        st.image(recommended_posters[4])

