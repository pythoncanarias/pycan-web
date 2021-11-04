function init() {
  getRandomQuote();

  // Change quote every RANDOM_QUOTE_INTERVAL
  setInterval(function() { getRandomQuote(); }, random_quote_interval);

  function getRandomQuote() {
    // Get the text and author span id
    let text = document.getElementById("quote-text");
    let author = document.getElementById("quote-author");
    // Load random quote and convert to JSON
    fetch(quotes_api_url)
      .then(response => response.json())
      .then(data => {
        text.textContent = data.result.text
        author.textContent = data.result.author
      })
    // Animate display
    let quote_block = document.getElementById("quote-block");
    fadeInQuote(quote_block)
  }
}

function fadeInQuote(quote, duration=2000) {
  quote.animate([
    { // from
      opacity: 0,
    },
    { // to
      opacity: 1,
    }
  ], duration);
}

export default {
  init
}
