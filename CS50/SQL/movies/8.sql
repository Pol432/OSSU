SELECT name FROM people JOIN movies, stars WHERE movies.title LIKE "%Toy Story%"
AND stars.movie_id = movies.id AND person_id = people.id;