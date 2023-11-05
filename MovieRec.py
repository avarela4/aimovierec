import pandas as pd

# read in data files
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')
tags = pd.read_csv('tags.csv')

# get user input
user_liked_movie = input("Enter a movie you previously liked: ")
user_genre = input("Enter a genre you like: ")
user_keyword = input("Enter a keyword associated with the movie you are looking for: ")

# need to make the data all lowercase to compare 
user_liked_movie = user_liked_movie.lower()
user_genre = user_genre.lower()
user_keyword = user_keyword.lower()
movies['title'] = movies['title'].str.lower()

# combine the data of movies and ratings
ratings_mean = ratings.groupby('movieId')['rating'].mean()
movies = pd.merge(movies, ratings_mean, on='movieId')

# filter 
movies['genres'] = movies['genres'].str.replace('|', ' ')
movies['title'] = movies['title'].str.strip()  
movies['title'] = movies['title'].str.replace(r'\(\d{4}\)', '')  

# get the movies that have something in common with what the user inputed 
matched_movies = movies[movies['title'].str.contains(user_liked_movie)]

if matched_movies.empty:
    print("Movie not found. Please check the spelling or try another movie.")
    exit()

# scoring based on the inputed genre and keyword
movies['genre_match'] = movies['genres'].apply(lambda x: user_genre in x)
movies['keyword_match'] = movies['title'].apply(lambda x: user_keyword in x)
movies['score'] = movies['genre_match'].astype(int) + movies['keyword_match'].astype(int) + movies['rating']

# get the top 5 and display
recommended_movies = movies[movies['title'].isin(matched_movies['title']) == False].nlargest(5, 'score')['title']
print("Top 5 recommended movies:")
print(recommended_movies)