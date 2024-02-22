SELECT title FROM movies JOIN stars,people,ratings WHERE people.name = "Chadwick Boseman"
AND stars.person_id = people.id
AND stars.movie_id = movies.id
AND ratings.movie_id = movies.id
ORDER BY ratings.rating DESC
LIMIT 5;