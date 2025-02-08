import unittest
from src.app import create_app
from src.database import db


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test app and database"""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    def setUp(self):
        """Set up fresh database for each test"""
        db.create_all()

    def tearDown(self):
        """Clean up database after each test"""
        db.session.remove()
        db.drop_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up application context"""
        cls.app_context.pop()
