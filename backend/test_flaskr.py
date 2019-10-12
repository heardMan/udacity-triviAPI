import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flaskr import app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.

    

    """
    #test route get questions
    def test_get_categories(self):
        """Test the get categories route"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['categories']),0)

    def test_get_questions(self):
        """Test the get paginated questions route"""
        res = self.client().get('/questions/page/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['categories']),0)
        self.assertGreater(len(data['questions']),0)
        self.assertGreater(data['total_questions'],0)

    def test_post_question(self):
        """Test the post question route"""

        get_before = self.client().get('/questions/page/1')
        get_before_data = get_before.json
        init_question_num = get_before_data['total_questions']
        
        post = self.client().post('/questions',json={
            'question': 'test question one',
            'answer': 'test answer one',
            'category': 1,
            'difficulty': 2
        })
        post_data = json.loads(post.data)

        get_after = self.client().get('/questions/page/1')
        get_after_data = get_after.json
        final_question_num = get_after_data['total_questions']

        self.assertEqual(post.status_code, 200)
        self.assertEqual(post_data['success'], True)
        self.assertGreater(final_question_num, init_question_num)


    def test_delete_questions(self):
        """Test the delete questions route"""
        
        get_before = self.client().get('/questions/page/1')
        get_before_data = get_before.json
        init_question_num = get_before_data['total_questions']

        if get_before_data['total_questions']%10 == 0:
            last_page = get_before_data['total_questions']//10
        else:
            last_page = (get_before_data['total_questions']//10)+1

        final_page = self.client().get('/questions/page/{}'.format(last_page))
        final_questions = final_page.json['questions']
        final_question = final_questions[len(final_questions)-1]
        
        delete = self.client().delete('/question/{}'.format(final_question['id']))
        delete_data= delete.json

        get_after = self.client().get('/questions/page/1')
        get_after_data = get_after.json
        final_question_num = get_after_data['total_questions']

        self.assertEqual(delete.status_code, 200)
        self.assertEqual(delete.json['success'], True)

        self.assertGreater(init_question_num, final_question_num)

    def test_search_questions(self):
        """Test the search questions route"""

        get_before = self.client().get('/questions/page/1')
        get_before_data = get_before.json
        init_question_num = len(get_before_data['questions'])
        
        post = self.client().post('/questions/search',json={
            'searchTerm': 'title',
        })
        post_data = json.loads(post.data)

        final_question_num = len(post_data['questions'])

        self.assertEqual(post.status_code, 200)
        self.assertEqual(post_data['success'], True)
        self.assertGreater(init_question_num, final_question_num)

    def test_get_questions_by_category(self):
        """Test the get questions by category route"""

        get_before = self.client().get('/questions/page/1')
        get_before_data = get_before.json
        init_question_num = len(get_before_data['questions'])

        post = self.client().post('/questions/search',json={
            'searchTerm': 'title',
        })
        post_data = json.loads(post.data)

        final_question_num = len(post_data['questions'])

        self.assertEqual(post.status_code, 200)
        self.assertEqual(post_data['success'], True)
        self.assertGreater(init_question_num, final_question_num)

    def test_quiz(self):
        """Test the quiz init route"""
        #TEST: In the "Play" tab, after a user selects "All" or a category,
        #one question at a time is displayed, the user is allowed to answer
        #and shown whether they were correct or not. 
        first_question_get_res = self.client().post('/questions/quiz',json={
            'previous_questions': [],
            'quiz_category': {
                'type':'click',
                'id':0
            }
        })

        first_question_data= json.loads(first_question_get_res.data)
        self.assertEqual(first_question_get_res.status_code, 200)
        self.assertEqual(first_question_data['success'], True)
        first_question = first_question_data['question']
        first_answer = first_question['answer']


        second_question_get_res = self.client().post('/questions/quiz',json={
            'previous_questions': [5,11],
            'quiz_category': {
                'type':'Sports',
                'id':0
            }
        })
        second_question_data = json.loads(second_question_get_res.data)
        self.assertEqual(second_question_get_res.status_code, 200)
        self.assertEqual(second_question_data['success'], True)
        second_question = second_question_data['question']
        second_answer = second_question['answer']
            
        self.assertNotEqual(first_question, second_question)
        self.assertNotEqual(first_answer, second_answer)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()