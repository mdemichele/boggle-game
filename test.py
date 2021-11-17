from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # Test "/" GET route
    def test_homepage(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle Game</title>', html)
    
    # Test "/guess" POST route: NOT in form  
    def test_not_one_board(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
            # setup board 
                sess["board"] = [["E", "S", "T", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"]]
            
            response = client.post("/guess", json={ 'guess': 'impossible'} )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["result"], 'not-on-board')
            self.assertEqual(response.json['points'], 0)
            
    # Test "/guess" POST route: In form 
    def test_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # setup board 
                sess["board"] = [["E", "S", "T", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"]]
                                
            response = client.post("/guess", json={'guess': 'test'})
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')
            self.assertEqual(response.json['points'], 4)
            
    # Test "/guess" POST route: Not a word 
    def test_not_word(self):
        with app.test_client() as client:
            with client.session_transaction() as sess: 
                sess["board"] = [["E", "S", "T", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"],
                                 ["E", "T", "S", "T", "S"]]
                                 
        response = client.post("/guess", json={'guess': 'fafadzzde'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'not-word')
        self.assertEqual(response.json['points'], 0)
