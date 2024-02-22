SELECT name FROM people JOIN stars,movies ON stars.movie_id = movies.id AND stars.person_id = people.id
WHERE stars.movie_id IN (SELECT stars.movie_id FROM people JOIN stars,movies
ON stars.movie_id = movies.id AND stars.person_id = people.id
WHERE people.name = "Kevin Bacon")
AND people.name != "Kevin Bacon";