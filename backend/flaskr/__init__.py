import os
import sys
from flask import Flask, request, abort, flash, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import random
import unittest

from models import db, Question, Category

# set the number of pages fpr pagination
QUESTIONS_PER_PAGE = 10

# create and configure the app
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# set up cors for the application
cors = CORS(app, resources={r'/': {'origins': '*'}})

# to set Access-Control-Allow Headers and Methods
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, PATCH,PUT,POST, DELETE, OPTIONS')
    return response

# endpoint to handle GET requests for all available categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = [category.type for category in Category.query.all()]
    return jsonify({'categories': categories, 'success': True})

# endpoint to handle GET requests for questions with pagination
@app.route('/questions/page/<int:page>', methods=['GET'])
def get_questions(page):
    error = False
    questions = []
    # if question id is not an integer
    if type(page) is not int:
        # let them know their input is not processable
        abort(422)
    # ensure proper request method
    if request.method == 'GET':
        try:
            # query for all categories
            categories = [category.type for category in Category.query.all()]
            if categories is None:
                # let the user know that no resource was found
                abort(404)

            query = Question.query.paginate(page, per_page=10)
            if query is None:
                # let the user know that no resource was found
                abort(404)

            results = query.items
            # format data
            for question in results:
                _question_ = {
                    'id': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'category': question.category,
                    'difficulty': question.difficulty
                }
                questions.append(_question_)
        except RuntimeError:
            # set error to true and log on the server
            error = True
            print('Error: {}'.format(sys.exc_info()))
        finally:

            if error:
                # let the user know their request was not successful
                abort(400)
            else:
                # if successful send back success response
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(query.query.all()),
                    'categories': categories
                })
    else:
        # send method not allowed error
        abort(405)


# endpoint to delete a question from the database
@app.route('/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    error = False

    # ensure proper request method
    if request.method == 'DELETE':

        # if question id is not an integer
        if type(question_id) is not int:
            # let them know their input is not processable
            abort(422)

        try:
            # get user selected question from database
            question = Question.query.get(question_id)
            # stage question delete
            db.session.delete(question)
            # commit deletion to the database
            db.session.commit()
        except RuntimeError:
            # set error to true and log on the server
            error = True
            print('Error: {}'.format(sys.exc_info()))

        finally:
            # close database session
            db.session.close()

            if error:
                # send bad request error
                abort(400)

            else:
                # if no error send success object and log on server
                return jsonify({
                    'success': True,
                    'method': 'Delete',
                    'question': question_id
                })
    else:
        # send method not allowed error
        abort(405)


# endpoint to add a question to the database
@app.route('/questions', methods=['POST'])
def add_question():
    error = False

    # ensure proper request method
    if request.method == 'POST':
        try:
            # format data for database
            new_question = Question(
                question=request.json['question'],
                answer=request.json['answer'],
                category=request.json['category'],
                difficulty=request.json['difficulty']
            )
            # stage data in database
            db.session.add(new_question)
            # commit data to database
            db.session.commit()

        except RuntimeError:
            # set error to true and log on the server
            error = True
            db.session.rollback()
            print('Error: {}'.format(sys.exc_info()))

        finally:
            # close database session
            db.session.close()

            if error:
                # send bad request error
                abort(400)
            else:
                # if no error send success object and log on server
                print('Added: {}'.format(new_question))
                return jsonify({
                    'success': True,
                    'question': request.json

                })
    else:
        # send method not allowed error
        abort(405)


# endpoint to search for for questions in the database
@app.route('/questions/search', methods=['POST'])
def search_questions():
    error = False

    # ensure proper request method
    if request.method == 'POST':

        # set esrch term from user request
        search_term = str(request.json['searchTerm'])
        # if the user submits something other than a string of text block it
        if type(search_term) is not str:
            # let them know their input is not processable
            abort(422)

        try:
            # query database using user provided search term
            query_results = Question.query.filter(
                Question.question.ilike('%{}%'.format(search_term))).all()
            questions = []
            # get categories from database
            categories = [category.type for category in Category.query.all()]
            # format response data
            for question in query_results:
                _question_ = {
                    'id': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'category': question.category,
                    'difficulty': question.difficulty
                }
                questions.append(_question_)

        except RuntimeError:
            # set error to true and log on the server
            error = True
            print('Error: {}'.format(sys.exc_info()))

        finally:
            if error:
                # send bad request error
                abort(400)
            else:
                # if no error send success object
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(questions),
                    'current_category': ''
                })
    else:
        # send method not allowed error
        abort(405)

# endpoint to get questions by a specific category
@app.route('/category/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
    error = False

    # ensure proper request method
    if request.method == 'GET':

        # if category id is not an integer
        if type(category_id) is not int:
            # let them know their input is not processable
            abort(422)

        try:
            # get questions by user selected category
            query = Question.query.filter_by(category=str(category_id)).all()
            questions = []
            # format response data
            for question in query:
                _question_ = {
                    'id': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'category': question.category,
                    'difficulty': question.difficulty
                }
                questions.append(_question_)
        except RuntimeError:
            # set error to true and log on the server
            error = True
            print('Error: {}'.format(sys.exc_info()))

        finally:
            if error:
                # send bad request error
                abort(400)
            else:
                # if no error send success object
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(questions),
                    'current_category': ''
                })
    else:
        # send method not allowed error
        abort(405)

# endpoint to initiate quiz
@app.route('/questions/quiz', methods=['POST'])
def quizzes():
    error = False

    # ensure proper request method
    if request.method == 'POST':

        try:
            data = request.json
            # get questions from any category
            if data['quiz_category']['id'] == 0:
                query = Question.query.all()
            # get questions from user specified caetgory
            else:
                query = Question.query.filter_by(
                    category=str(int(data['quiz_category']['id'])+1)).all()
            # randomly select new non previously selected question
            previous_questions = data['previous_questions']
            index = random.randint(0, len(query)-1)
            potential_question = query[index]
            selected = False
            while selected is False:
                if potential_question.id in previous_questions:
                    index += 1
                    potential_question = query[index]
                else:
                    selected = True
            # set question
            _question_ = potential_question
            # format data
            next_question = {
                'id': _question_.id,
                'question': _question_.question,
                'answer': _question_.answer,
                'category': _question_.category,
                'difficulty': _question_.difficulty
            }
        except RuntimeError:
            # set error and log error on the server
            error = True
            print('Error: {}'.format(sys.exc_info()))

        finally:

            if error:
                # send internal server error
                abort(500)
            else:
                # if no error send success object
                return jsonify({
                    'success': True,
                    'question': next_question
                })
    else:
        # send method not allowed error
        abort(405)

# handle bad request errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": BAD_REQUEST_MESSAGE
    }), 400

# handle resource not found errors
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found -- no such resource is accessible"
    }), 404

# handle resource not found errors
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
    }), 405

# handle unprocessable entity errors
@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity -- try submitting a different value"
    }), 422

# handle internal server errors
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error -- oops, our bad"
    }), 500


# Default port:
if __name__ == '__main__':
    app.run()
