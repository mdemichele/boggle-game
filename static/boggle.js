// 01. Attach event handler for submitting guesses from form 
let form = document.getElementById("game-form");
form.addEventListener("submit", handleGuess);

// 02. Setup Timer  
let myVar = setInterval(handleTimer, 1000);

// FUNCTION 1: Event Handler for form submit 
async function handleGuess(event) {
  // Prevent the page from reloading 
  event.preventDefault();
  
  // submit the quess 
  let guess = event.target.guess.value;
  
  // Send guess to the backend
  let response = await axios({
    method: 'post',
    url: '/guess',
    headers: {
      "Content-Type": "application/json",
    },
    data: {
      guess: guess
    }
  });
  
  if (response.status == 200) {
    console.log("form submission successful");
  } else {
    console.log(`there was a ${response.status} error`);
  }

  // Get the resulting response back from the backend and score 
  let result = response.data.result;
  let points = response.data.points;
  
  // Get the game-guess dom element and insert result 
  let guessElement = document.getElementById("game-guess");
  guessElement.innerText = result;
  
  // Add the score 
  let pointsElement = document.getElementById("game-score");
  
  // Increment Points on DOM
  let newPoints = parseInt(pointsElement.innerText) + parseInt(points);
  pointsElement.innerText = newPoints;
  
}

// FUNCTION 2: Returns after 1 second 
function pauseOneSecond(milliseconds) {
  let initialDate = new Date();
  while ((new Date()) - initialDate <= milliseconds) {
    // Do Nothing while waiting
  }
}

// FUNCTION 3: Attaches the new time to DOM until timer reaches 0
async function handleTimer() {
  let timeElement = document.getElementById("timer");
  let currentTime = parseInt(timeElement.innerText);
  let newTime = currentTime - 1;
  
  // Stop at 0 
  if (newTime <= -1) {
    // Stop decrementing timer 
    clearInterval(myVar);
    
    // Remove the old event listener 
    form.removeEventListener("submit", handleGuess);
    
    // get the current score from DOM
    let currentScore = document.getElementById("game-score").innerText;
    
    // submit current Score 
    let response = await axios({
      method: 'post',
      url: '/calculate-high-score',
      data: {
        score: currentScore 
      }
    });
    
    // Replace high score in DOM if currentScore is the new high score 
    let highScore = response.data.highScore; 
    
    if (highScore == currentScore) {
      console.log("new high score: " + highScore);
      let scoreElement = document.getElementById("highest-score");
      scoreElement.innerText = highScore;
    }
    
    // Add the end of game listener 
    form.addEventListener("submit", function() {
      event.preventDefault();
    });
    
    return 0;
  } else {
    timeElement.innerHTML = newTime;
  }
  
}