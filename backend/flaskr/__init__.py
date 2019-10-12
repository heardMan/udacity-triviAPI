import os
import sys
from flask import Flask, request, abort, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import random
import unittest

from models import db, Question, Category

QUESTIONS_PER_PAGE = 10


# create and configure the app
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
 
'''
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
'''
cors = CORS(app, resources={r'/': {'origins': '*'}}) 
'''
@TODO: Use the after_request decorator to set Access-Control-Allow
'''
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
  response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH,PUT,POST, DELETE, OPTIONS')
  return response

'''
@TODO: 
Create an endpoint to handle GET requests 
for all available categories.
'''
@app.route('/categories', methods=['GET'])
def get_categories():
  categories = [category.type for category in Category.query.all()]
  return jsonify({'categories': categories, 'success': True})

'''
@TODO: 
Create an endpoint to handle GET requests for questions, 
including pagination (every 10 questions). 
This endpoint should return a list of questions, 
number of total questions, current category, categories. 

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions. 
'''

@app.route('/questions/page/<int:page>', methods=['GET'])
def get_questions(page):
  error=False
  questions = []
  try:
    categories = [category.type for category in Category.query.all()]
    if categories == None:
      error_message = dumps({'Message': 'Cannot find Categories... Check your connection(s)?'})
      abort(Response(error_message, 404))
    
    query = Question.query.paginate(page, per_page=10)
    if query == None:
      error_message = dumps({'Message': 'Cannot fin Questions... Check your connection(s)'})
      abort(Response(error_message, 404))

    results = query.items
  
    for question in results:
      _question_ = {
        'key': question.id,
        'question': question.question,
        'answer': question.answer,
        'category': question.category,
        'difficulty': question.difficulty
      }
      questions.append(_question_)
    
    
  except:
    error=True
    error_message = dumps({'Message': 'Your request for Questions Page {} has failed.'.format(page)})
    
  finally:
    
    if error:
      abort(Response(error_message, 400))
    else:
      return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(query.query.all()),
            'categories': categories
    })
   

'''
@TODO: 
Create an endpoint to DELETE question using a question ID. 

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page. 
'''



'''
@TODO: 
Create an endpoint to POST a new question, 
which will require the question and answer text, 
category, and difficulty score.

TEST: When you submit a question on the "Add" tab, 
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.  
'''
@app.route('/questions', methods=['POST'])
def add_question():
  print('Request data: {}'.format(request.data))
  print('{}'.format(request.json))

  error=False

  try:
    new_question = Question(
      question=request.json['question'],
      answer=request.json['answer'],
      category=request.json['category'],
      difficulty=request.json['difficulty']
    )
    print(new_question)
    db.session.add(new_question)
    db.session.commit()
    
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

    if error:
      abort(400)
    else:
      
      return jsonify({
        'success': True,
        'question': request.json
        
      })


    


  

  
  
'''
@TODO: 
Create a POST endpoint to get questions based on a search term. 
It should return any questions for whom the search term 
is a substring of the question. 

TEST: Search by any phrase. The questions list will update to include 
only question that include that string within their question. 
Try using the word "title" to start. 
'''

'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''


'''
@TODO: 
Create a POST endpoint to get questions to play the quiz. 
This endpoint should take category and previous question parameters 
and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not. 
'''

'''
@TODO: 
Create error handlers for all expected errors 
including 404 and 422. 
'''
#@app.errorhandler(404)
  
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

    