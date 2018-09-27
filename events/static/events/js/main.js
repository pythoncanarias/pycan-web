import historyState from './utils/history-state'
import General from './general'
import Event from './event'
import BuyArticle from './buy-article'


document.addEventListener('DOMContentLoaded', () => {
  historyState.setInitialPage()

  General.init()

  const pageClasses = document.body.classList

  if (pageClasses.contains('event-page')) {
    Event.init()
  }

  if (pageClasses.contains('buy-article-page')) {
    BuyArticle.init()
  }
})
