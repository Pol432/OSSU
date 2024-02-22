SELECT title FROM movies JOIN people,stars ON movies.id = stars.movie_id AND stars.person_id = people.id
WHERE people.name = "Johnny Depp"
AND stars.movie_id IN (SELECT movies.id FROM movies JOIN stars,people ON stars.movie_id = movies.id
AND stars.person_id = people.id
WHERE people.name = "Helena Bonham Carter");
