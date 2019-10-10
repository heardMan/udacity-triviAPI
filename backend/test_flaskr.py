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
        #self.assertGreater(data['total_questions'],0)
    
    def test_delete_questions(self):
        """Test the delete questions route"""
        #TEST: When you click the trash icon next to a question, the question will be removed.
        #This removal will persist in the database and when you refresh the page.
        pass

    def test_post_question(self):
        """Test the post question route"""
        #TEST: When you submit a question on the "Add" tab, 
        #the form will clear and the question will appear at the end of the last page
        #of the questions list in the "List" tab.
        pass

    def test_search_questions(self):
        """Test the search questions route"""
        #TEST: Search by any phrase. The questions list will update to include 
        #only question that include that string within their question. 
        #Try using the word "title" to start.
        pass

    def test_get_questions_by_category(self):
        """Test the search questions route"""
        #TEST: In the "List" tab / main screen, clicking on one of the 
        #categories in the left column will cause only questions of that 
        #category to be shown. 
        pass

    def test_quiz(self):
        """Test the quiz init route"""
        #TEST: In the "Play" tab, after a user selects "All" or a category,
        #one question at a time is displayed, the user is allowed to answer
        #and shown whether they were correct or not. 
        pass




        
    
        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()