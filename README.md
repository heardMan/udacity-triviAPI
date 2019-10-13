# udacity-triviAPI

## Introduction

Welcome to trivia API!

I completed this project as part of the Udacity Full Stack Developer Nanodegree.

This Project taught me alot about using Python3 and flask to create backend logic for web applications.

As a full stack application this project has 2 main directories: the fronend and the backend.

The front end portion of this application is written in ReactJS.

The back end portion of this applicattion is written with Python3, flask, and a postgreSQL database.

The follow sectionsgive details on how to set up and start a development server for the project.

## Initial Set Up and Configuration

The first step to starting development on Trivia API will require one to clone the initial files.

Please Fork or clone the directory-- cloning instructions are provided below.

Cloning Instructions:

Step 1: Open your command Line or Terminal Application

Step 2: Navigate to the directory you would like to clone the Trivia API to.

Step 3: Now that the files are on your local machine navigate to the root directory of the project

Step 4: Set up your virtual Python3 environment and install the necessary requirements

```
cd Desktop
git clone https://github.com/heardMan/udacity-triviAPI.git
cd udacity-triviaAPI
python3 -m venv your_environment_name
source your_environment_name/bin/activate
pip install -r requirements.txt
```

### Backend Server Set Up

If you do not already have it please download and install python3 with pip3 <a href="https://www.python.org/downloads/">here</a> prior to setting up this application.

Now that you have the application on your local machine it is time to start configuring the backend server.

In order for all the application logic to work smoothly there needs to be quite a few seed questions in the database already. From the root directory of the project enter the following commands into your command line or terminal application.

##### Set Up the PostgreSQL Database

'''
cd backend
dropdb trivia
createdb triva
psql trivia < trivia.psql
'''

##### Set Up the Flask App

from the directory titled backend enter the following commands into your command line or terminal application

```
export FLASK_APP=flaskr
export FLASK_ENV-development
export FLASK_DEBUG=true
flask run --reload
```

For running tests it is generally reccomended that you use a fresh database instance.
To make this process easier feel free to enter the following into your command to perform testing.

##### Set Up the test PostgreSQL Database

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Frontend Server Set Up

If you do not already have it please download and install nodeJS <a href="https://nodejs.org/en/download/">here</a> prior to setting up this application.

As a react application setting up the server for Trivia API is very easy.

From your root directory simply enter the following commands on your command line:

##### Download and Install Node Dependencies

```
cd frontend
npm i
npm start
```

Viola!

Trivia API should be up and running!

## API DOCUMENTATION

### GET categories

##### Relative Route:
<strong>/categories</strong>

##### Route Method: 
<strong>GET</strong> 

##### Parameters: 
None

##### Sample Request Object: 
None

##### Sample cURL Request:

```
curl http://localhost:3000/categories
```

##### Sample Success Response:

```
{
    "categories":[
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "success": true
}
```

### GET paginated questions

##### Relative Route:
<strong>/questions/page/{page_number}</strong>

##### Route Method: 
<strong>GET</strong> 

##### Parameters: 
<strong>page_number</strong> 

##### Sample Request Object: 
None

##### Sample cURL Request:

```
curl http://localhost:3000/questions/page/1
```

##### Sample Success Response:

```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 23
}
```

### GET questions by category

##### Relative Route:
<strong>/category/{caetgory_id}/questions</strong>

##### Route Method: 
<strong>GET</strong> 

##### Parameters: 
<strong>caetgory_id</strong> 

##### Sample Request Object: 
None

##### Sample cURL Request:

```
curl http://localhost:3000/category/1/questions
```

##### Sample Success Response:

NOTE: this is not a complete response object
we have ommited several results to make this block of code more readable
this is why it state 7 results even though there are only 3 shown

```
{
  "current_category": "", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 7
}
```

### POST search term for a question

##### Relative Route:
<strong>/questions/search</strong>

##### Route Method: 
<strong>POST</strong> 

##### Parameters: 
None

##### Sample Request Object: 

```
{
    "searchTerm": "some_search_term"
}
```

##### Sample cURL Request:

```
curl -d '{"searchTerm":"title"}' -H "Content-Type: application/json" http://localhost:3000/questions
```

##### Sample Success Response:

```
{
  "current_category": "", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

### POST a question

##### Relative Route:
<strong>/questions</strong>

##### Route Method: 
<strong>POST</strong> 

##### Parameters: 
None

##### Sample Request Object: 

```
{
    "question": "sample_question_text",
    "answer": "sample_answer_text",
    "category": 1,
    "difficulty": 1
}
```

##### Sample cURL Request:

```
curl -d '{"question":"sample_question_text","answer":"sample_answer_text","difficulty":1, "category":1}' -H "Content-Type: application/json" http://localhost:3000/questions
```

##### Sample Success Response:

```
{
  "question": {
    "answer": "sample_answer_text", 
    "category": 1, 
    "difficulty": 1, 
    "question": "sample_question_text"
  }, 
  "success": true
}
```

### DELETE a question

##### Relative Route:
<strong>/question/{question_id}</strong> 

##### Route Method: 
<strong>DELETE</strong> 

##### Parameters: 
<strong>question_id</strong> 

##### Sample Request Object: 
None

##### Sample cURL Request:

```
curl -X DELETE http://localhost:3000/question/29
```

##### Sample Success Response:

```
{
  "method": "Delete", 
  "question": 29, 
  "success": true
}
```

### POST a quiz answer

##### Relative Route:
<strong>/questions/quiz</strong>

##### Route Method: 
<strong>POST</strong> 

##### Parameters: 
None

##### Sample Request Object: 

```
{
    "previous_questions": [1,2],
    "quiz_category": {
        "type": "click",
        "id":0
    }
}
```

##### Sample cURL Request:

```
curl -d '{"previous_questions":[5,11], "quiz_category":{"type":"Science", "id":0}}' -H "Content-Type: application/json" http://localhost:3000/questions/quiz
```

##### Sample Success Response:

```
{
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "success": true
}
```

### Sample 400 Error

description: if the request is not formatted properly the following error will be sent

##### Sample Response Object:

```
{
     "success": False, 
     "error": 400,
     "message": "Bad Request -- check your formatting "
  },400
```

### Sample 404 Error

description: if the requested resouces is not available the following error will be sent

##### Sample Response Object:

```
{
     "success": False, 
     "error": 404,
     "message": "Resource Not Found -- no such resource is accessible on the server"
  },404
```

### Sample 405 Error

description: if the request attempts to use an unapproved method the following error will be sent

##### Sample Response Object:

```
{
     "success": False, 
     "error": 405,
     "message": "Method Not Allowed -- the endpoint you accesssed does not allow such a method"
  },405
```

### Sample 422 Error

description: if the request is not of the appropriate data type the following error will be sent

##### Sample Response Object:

```
{
     "success": False, 
     "error": 422,
     "message": "Unprocessable Entity -- try submitting a different value"
  },422
```

### Sample 500 Error

description: if the application has an internal error not related to user input the following error will be sent

##### Sample Response Object:

```
{
     "success": False, 
     "error": 500,
     "message": "Internal Server Error -- oops, our bad"
  },500
```

## conclusion

Thank you for your interest in Trivia API!

If you have any questions feel free to send me a message here on git hub or leave a comment and I will try to get back to you as soon as possible.
