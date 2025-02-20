const SECS = 1000; /* Interval works with miliseconds */
const RANDOM_QUOTE_INTERVAL = 10 * SECS; /* 10 seconds */
const QUOTES_API_URL = "/api/v1/quotes/";

const fadeOut = function(elem, duration=2000) { elem.animate([{ opacity: 1}, { opacity: 0} ], duration); };

const fadeIn = function(elem, duration=2000) { elem.animate([{ opacity: 0}, { opacity: 1} ], duration); };


function init() {
  let quote_block = document.getElementById("quote-block");
  let quote_text = document.getElementById("quote-text");
  let quote_author = document.getElementById("quote-author");

  let getRandomQuote = function () {
    fadeOut(quote_block);
    fetch(QUOTES_API_URL)
      .then(function(response) { return response.json() })
      .then(function(data) {
        quote_text.textContent = data.result.text;
        quote_author.textContent = data.result.author;
        fadeIn(quote_block);
      })
    }
  setInterval(getRandomQuote, RANDOM_QUOTE_INTERVAL);
  }


window.onload = function() {
  init();
  };
