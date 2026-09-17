function fadeInQuote(duration=2000) {
    // Animate display
    let quote = document.getElementById("quote-block");
    quote.animate([
        { // from
            opacity: 0,
        },
        { // to
            opacity: 1,
        }
        ], duration);
    };


function getRandomQuote() {
    // Get the text and author span id
    let text = document.getElementById("quote-text");
    let author = document.getElementById("quote-author");
    // Load random quote and convert to JSON
    fetch(quotes_api_url)
        .then(response => response.json())
        .then(data => {
            text.textContent = data.result.text;
            author.textContent = data.result.author;
            })
        .then(fadeInQuote);
    };
