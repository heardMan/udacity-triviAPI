import os
import sys
from flask import Flask, request, abort, flash, jsonify, Response
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
      abort(404)
    
    query = Question.query.paginate(page, per_page=10)
    if query == None:
      abort(404)

    results = query.items
  
    for question in results:
      _question_ = {
        'id': question.id,
        'question': question.question,
        'answer': question.answer,
        'category': question.category,
        'difficulty': question.difficulty
      }
      questions.append(_question_)
    
    
  except:
    error=True
    print(sys.exc_info())
  finally:
    
    if error:
      abort(400)
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
@app.route('/question/<int:question_id>', methods=['DELETE', 'GET'])
def delete_question(question_id):

  print(question_id)

  error=False

  if request.method == 'DELETE':
    try:
      #something
      question = Question.query.get(question_id)
      db.session.delete(question)
      db.session.commit()
    except:
      error=True
      print(sys.exc_info())
    finally:
      db.session.close()
      #something
      if error:
        
        abort(400)
        
      else:
        return jsonify({
          'success': True,
          'method': 'Delete',
          'question': question_id
        })

    

  if request.method == 'GET':
    return jsonify({
      'success': True,
      'method': 'Get',
      'implemented': False
    })

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

  error=False

  try:
    new_question = Question(
      question=request.json['question'],
      answer=request.json['answer'],
      category=request.json['category'],
      difficulty=request.json['difficulty']
    )
    print('Added: {}'.format(new_question))
    db.session.add(new_question)
    db.session.commit()
    
  except:
    error=True
    db.session.rollback()
    print('Error: {}'.format(sys.exc_info()))
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

@app.route('/questions/search', methods=['POST'])
def search_questions():
  search_term = request.json['searchTerm']
  print(search_term)
  query_results = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
  questions = []
  categories = [category.type for category in Category.query.all()]
  for question in query_results:
    _question_ = {
      'id':question.id,
      'question': question.question,
      'answer': question.answer,
      'category': question.category,
      'difficulty': question.difficulty
    }
    questions.append(_question_)

  print(questions)

  return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': ''
        
      })


'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''
@app.route('/category/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
  print(category_id)
  query = Question.query.filter_by(category=category_id).all()
  questions = []
  for question in query:
    _question_={
      'id': question.id,
      'question': question.question,
      'answer':question.answer,
      'category': question.category,
      'difficulty': question.difficulty
    }
    questions.append(_question_)
  print(query)
  
  return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': ''
        
        })

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

@app.route('/questions/quiz', methods=['POST'])
def quizzes():
  data = request.json
  if data['quiz_category']['id'] == 0:
    query = Question.query.all()
  else:
    query = Question.query.filter_by(category=int(data['quiz_category']['id'])+1).all()


  previous_questions=data['previous_questions']
  index = random.randint(0,len(query)-1)
  potential_question = query[index]
  selected = False
  while selected == False:
    if potential_question.id in previous_questions:
      index +=1
      potential_question = query[index]
      print(potential_question)
    else:
      selected = True
  
  _question_ = potential_question

  next_question = {
    'id': _question_.id,
    'question':_question_.question,
    'answer':_question_.answer,
    'category':_question_.category,
    'difficulty':_question_.difficulty
  }

  print(data)
  return jsonify({
          'success': True,
          'question': next_question
        
        })
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

    