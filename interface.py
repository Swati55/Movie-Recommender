import streamlit as st
import pickle
import pandas as pd
import requests

#loading movies and similarity
movie_dict =pickle.load(open('movie_dict.pkl','rb'))
movie = pd.DataFrame(movie_dict)

similarity= pickle.load(open('similarity.pkl','rb'))

#function for posters        404d90dd7bc3d8ef5e096dc224226e8d
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=404d90dd7bc3d8ef5e096dc224226e8d&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path ="https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


#recommend function
def recommend(m):
    movie_index = movie[movie['title'] == m].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse =True, key =lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters =[]
    for i in movie_list:
        movie_id = movie.iloc[i[0]].movie_id
        #fetching poster using api
        recommended_movies.append(movie.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

#title
st.title('Movie Recommender System')

#dropbox
selected_movie_name = st.selectbox(' ', movie['title'].values)

#button
if st.button('Recommend'):
    names, posters =recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
