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
num_games = 0
highest_score = 0
current_guesses = set()

# Home Page Route Displays the Game Board 
@app.route("/")
def display_root():
    """Displays the root page with game board"""
    global num_games
    global highest_score
    global current_guesses
    
    # Create a new board every time you reload the home page 
    board = boggle_game.make_board() 
    
    # Reset current_guesses everytime you reload home page 
    current_guesses.clear()
    
    # Save board into session 
    session["board"] = board 
    
    # Increment the number of games played 
    num_games += 1
    
    return render_template("home.html", board=board, num_games=num_games, highest_score=highest_score)
    
# Guess Route to accept a user's guesss 
@app.route("/guess", methods=['POST'])
def accept_guess():
    """Accepts a guess from the user"""
    global boggle_game
    global current_guesses
    
    # Create response object 
    response = {}
    
    # Will use this variable for keeping track of points 
    points = 0
    
    # Get current board 
    currentBoard = session["board"]
    
    # Get guess 
    guess = request.json["guess"]
    
    # Get a list of words from boggle_game object 
    words = boggle_game.words 
    
    # Check if the guess is a valid word in dictionary AND valid on board 
    checkResponse = boggle_game.check_valid_word(currentBoard, guess)
    
    if checkResponse == "ok" and guess not in current_guesses:
        current_guesses.add(guess)
        points = len(guess)
    elif checkResponse == "ok" and guess in current_guesses:
        checkResponse = "already-used"
        points = 0
    else:
        points = 0
    
    response["result"] = checkResponse 
    response["points"] = points
    
    return jsonify(response)

# Calculate the high score at the end of each game 
@app.route('/calculate-high-score', methods=['POST'])
def calculate_high_score():
    """Records new high score if current score is higher"""
    global highest_score 
    
    # Create response object 
    response = {}
    
    # Get the current score 
    current_score = request.json["score"]
    
    # Check if current score is higher than highest score 
    if int(current_score) > highest_score:
        highest_score = int(current_score) 
    
    response['highScore'] = highest_score
    
    return jsonify(response)