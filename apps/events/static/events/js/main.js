import historyState from './utils/history-state'
import Event from './event'
import BuyArticle from './buy-article'
import Raffle from './raffle'


document.addEventListener('DOMContentLoaded', () => {
  historyState.setInitialPage()

  const pageClasses = document.body.classList

  if (pageClasses.contains('event-page')) {
    Event.init()
  }

  if (pageClasses.contains('buy-article-page')) {
    BuyArticle.init()
  }

  if (pageClasses.contains('raffle-gift-page')) {
    Raffle.init()
  }
})
