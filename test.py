from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))


    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                #i used 5 chips 
                sess['board'] = [["C", "H", "I", "P", "S"], ["C", "H", "I", "P", "S"], ["C", "H", "I", "P", "S"], ["C", "H", "I", "P", "S"], ["C", "H", "I", "P", "S"]]
        response = self.client.get('/check-word?word=chip')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=spiectakularspoodermain')
        self.assertEqual(response.json['result'], 'not-word')
