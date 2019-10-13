### Backend Server Set Up

Now that you have the application on your local machine it is time to start configuring the backend server.

In order for all the application logic to work smoothly there needs to be quite a few seed questions in the database already. Enter the following commands into your command line or terminal application.

'''
cd backend
dropdb trivia
createdb triva
psql trivia < trivia.psql
'''

set up flask app

from the directory titled backend enter the following commands into your command line or terminal application

```
export FLASK_APP=flaskr
export FLASK_ENV-development
export FLASK_DEBUG=true
```

For running tests it is generally reccomended that you use a fresh database instance.
To make this process easier feel free to enter the following into your command to perform testing.

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```