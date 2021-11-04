function init() {
  // Show the first quote
  getRandomQuote();

  // Change quote every RANDOM_QUOTE
  setInterval(function() { getRandomQuote(); }, random_quote_interval);

  // Retrieve random quote using the api
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
  }
}

export default {
  init
}
