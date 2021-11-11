// Event Handler for form submit 
let form = document.getElementById("game-form");
form.addEventListener("submit", handleGuess);

// Event Handler for form submit 
async function handleGuess(event) {
  // Prevent the page from reloading 
  event.preventDefault();
  
  // submit the quess 
  guess = event.target.guess.value;
  console.log(guess);
  
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
  
}

// When the whole page is loaded 
window.addEventListener('load', (event) => {
  // Do something here 
});