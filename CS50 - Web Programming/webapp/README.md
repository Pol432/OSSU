# Skillmatch
SkillMatch is an web app that aims to develop creativity, the desire of creation in students and help them choose their future career through experimentation. The method that the app applies is the recommendation of projects to students, projects that will be recommended according to their abiities and likes, and will be created by teachers and evaluated by the staff from the web app.


## Quick Start Guide
Run `pip install -r requirements.txt` in your terminal and then `python manage.py runserver` in order to get the link for the Django server.
After signing up, tn order to navigate through the app, the user can use the navbar in the top. Clicking the name of the app will take the user to the index (where the projects are), and clicking on the username will take it to the user page.
The rest of the web app features are self explanatory.


## Features
### Index
The index of the web app has the list of all the projects, if the user has done the test then the projects will be sorted from the ones that are recommended the most, to the ones the user would enjoy the least based on the test results. If the user hasn't done the test then the order of the projects will be randomized.

### User page
The main two divisions of the user page will be the pie chart which will show the user test results with the five interest areas. This page will also show the projects that the user has saved. And if the user is a teacher, it will have the option to see the projects that they have created, as well as the option to create a project.

### Test
The test is divided in two main parts, the first one is based on the Kuder Vocational Test and the second part from the Holland Vocational Test. The second part has two main divisions too.


## File Explanations
### Main Files
Includes the folder **images** for the images files for the ImageField from the projects model. The other files are self explanatory (db, README, requirements, etc.)
### skillmatch-static
All the css and js files for the project.
### skillmatch-templates
Has all the .html files for SkillMatch.
### skillmatch
- The forms.py file has the forms to create/edit a project, as well as the login and signup forms.
- The rest of the files are self explanatory.


## Distinctiveness and Complexity
This project has a real life application and, if developed well, it has the capability of helping students and teachers. One of the most common mistakes of students at the moment of choosing a careers is the fact that they don't know what they are going to do and what they can do. By having a greater understanding of their abilities and the things they like, as well as what they can create with their current capabilities, already gives them a greater comprehension of the paths that they can choose when they grow up. Plus, giving them a sense of creation since a young age can also help them become productive members of society who ñpve what they do.

In order to make the app as viable as possible with its current uses, it was necessary to make a deep research on the methods that can be applied to accomplish its objectives. For example, when making the test that measures the user likes and abilities, it was necessary to apply the Kuder and Holland vocational tests and adapt it to the apps needs (By choosing only the questions that were related of the interest areas of the app, and the activities that were already adapted to our days).

SkillMatch makes use of the main advantajes that Django and React have to offer. By using not only the materials that were teached during CS50W course, but also some other features. As well as the use of other libraries that help the front-end of the web app look appealing to the user, and some other functionalities in the backend, such as Numpy library which helps to make use of the Dot Product algorithm to recommend projects to the student.