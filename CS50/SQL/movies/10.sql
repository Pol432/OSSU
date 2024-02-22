SELECT name FROM people JOIN directors,movies,ratings WHERE ratings.rating >= 9.0
AND people.id = directors.person_id
AND movies.id = ratings.movie_id
AND directors.movie_id = movies.id;