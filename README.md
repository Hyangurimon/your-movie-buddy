# YOUR MOVIE BUDDY
#### Video Demo: https://youtu.be/uDneBaCc8q4
#### Description:
Your Movie Buddy is a web-based application made using JavaScript, Python, and SQL.
It is an application where you can register/log in and log the movies that you have watched so far like a movie diary.
The reason behind making this application was that I tend to forget which movies I watched or haven't watched.
I thought it would be nice to have a movie diary where I could keep a record of all the movies that I have watched so far and which date I watched it on.

In order to use the application, you need to be logged in, therefore you need to first register.
If you have already registered, you may use your username and password to log in.
The register page and login page are displayed using the register.html and login.html files.
When you log in, you will be shown a list of all the movies that you have already added.
If you haven't logged any movies yet, or if you have just registered as a new user, you will be shown an empty list, followed by the total number of movies watched, which in this case would be 0.
This page is implemented using the index.html file.

When you click on 'Add Movie', you will be redirected to an 'Add Movie' page.
This page is displayed by the add.html file.
In this page, you can literally add a movie that you have watched.
You have the option of keying in the following information when making a record:
- date you watched the movie,
- title of movie,
- director,
- co-director (if any),
- release year of movie,
- your own personal rating out of 5
The date and title are required fields, i.e. an error message will flash if no input is given.
The rest are optional, i.e. they can be left blank.

When you click on 'Delete Movie', you will be redirected to a 'Delete Movie' page.
This page is displayed using the delete.html, deleted.html, and deleteSearch.html files.
In this page, you can search for a movie that corresponds with the movie details that you wish to delete.
You can select which category it is that you wish to search in, either Movie Title, Directors, or Release Year, and type in the search bar which word/number it is that you wish to look up.
Alternatively, you can just click on 'List All Movies' to view all the movies.
When you get back the result of your search, you can check on the checkboxes of the movies that you wish to delete from you log.

You can also click on your nickname on the upper far right corner to make changes to your nickname or your password.
To edit your nickname, you can click on the 'Edit Nickname' button, and to edit your password, you can click on the 'Edit Password' button.
These tasks are implemented using the edit.html, edited.html, editNickname.html, editPassword.html files.
Finally, you can click on 'Log Out' to log out from the application altogether.
