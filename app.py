from flask import Flask 
from boggle import Boggle

# Create instance of flask app 
app = Flask(__name__)

# Create instance of the boggle game 
boggle_game = Boggle()
