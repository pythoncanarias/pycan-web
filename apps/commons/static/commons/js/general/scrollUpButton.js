'use strict'

function init() {
  const scrollToTopBtn = document.getElementById('scrollToTopBtn')

  const rootElement = document.documentElement

  function scrollToTop(ev) {
    ev.preventDefault()
    // Scroll to top logic
    rootElement.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }

  scrollToTopBtn.addEventListener('click', scrollToTop)
}

export default {
  init,
}
