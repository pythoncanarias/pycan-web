import historyState from './utils/history-state'
import Event from './event'
import BuyArticle from './buy-article'


document.addEventListener('DOMContentLoaded', () => {
  historyState.setInitialPage()

  const pageClasses = document.body.classList

  if (pageClasses.contains('event-page')) {
    Event.init()
  }

  if (pageClasses.contains('buy-article-page')) {
    BuyArticle.init()
  }
})
