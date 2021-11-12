// Event Handler for form submit 
let form = document.getElementById("game-form");
form.addEventListener("submit", handleGuess);

// Event Handler for form submit 
async function handleGuess(event) {
  // Prevent the page from reloading 
  event.preventDefault();
  
  // submit the quess 
  guess = event.target.guess.value;
  
  // Send guess to the backend
  response = await axios({
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

  result = response.data.result;
  
  // Get the game-guess dom element and insert result 
  guessElement = document.getElementById("game-guess");
  guessElement.innerText = result;
  
}

// When the whole page is loaded 
window.addEventListener('load', (event) => {
  // Do something here 
});