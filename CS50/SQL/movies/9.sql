SELECT name FROM people JOIN movies,stars WHERE movies.year = 2004 AND stars.person_id = people.id
AND stars.movie_id = movies.id
ORDER BY people.birth;