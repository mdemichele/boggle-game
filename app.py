from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

# Create instance of flask app 
app = Flask(__name__)

# Set the secret key for sessions 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Set secret key for debug toolbar 
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

debug = DebugToolbarExtension(app)

# Create instance of the boggle game and create a random board 
boggle_game = Boggle()
board = boggle_game.make_board()

# Home Page Route Displays the Game Board 
@app.route("/")
def display_root():
    """Displays the root page with game board"""
    session["board"] = board 
    
    return render_template("home.html", board=board)
    
# Guess Route to accept a user's guesss 
@app.route("/guess", methods=['POST'])
def accept_guess():
    """Accepts a guess from the user"""
    global boggle_game
    
    # Create response object 
    response = {}
    
    # Get current board 
    currentBoard = session["board"]
    
    # Get guess 
    guess = request.json["guess"]
    
    # Get a list of words from boggle_game object 
    words = boggle_game.words 
    
    # Check if the guess is a valid word in dictionary AND valid on board 
    checkResponse = boggle_game.check_valid_word(currentBoard, guess)
    
    response["result"] = checkResponse 
    
    print(response)
    
    return jsonify(response)