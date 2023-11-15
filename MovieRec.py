import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# data files
movies = pd.read_csv('movies.csv')

# user input
user_liked_movie = input("Enter a movie you previously liked: ")
user_genre = input("Enter a genre you like: ")
user_keyword = input("Enter a keyword associated with the movie you are looking for: ")

# convert inputs to lowercase
user_liked_movie = user_liked_movie.lower()
user_genre = user_genre.lower()
user_keyword = user_keyword.lower()
movies['title'] = movies['title'].str.lower()

# TF-IDF Vectorization on movie genres and keywords
movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)
movies['genres_keywords'] = movies['genres'] + " " + movies['title']
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['genres_keywords'])

# cosine similarity between movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# find index of the movie that matches user's liked movie
movie_index = movies[movies['title'].str.contains(user_liked_movie)].index

if len(movie_index) == 0:
    print("Movie not found. Please check the spelling or try another movie.")
    exit()

# similarity scores
similarity_scores = list(enumerate(cosine_sim[movie_index[0]]))

# sort movies based on similarity scores
similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

# top 5 similar movies
top_similar_movies_indices = [score[0] for score in similarity_scores[1:6]]  # Exclude the first movie (itself)
recommended_movies = movies.iloc[top_similar_movies_indices]['title']

print("Top 5 recommended movies:")
print(recommended_movies)
