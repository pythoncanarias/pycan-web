import historyState from './utils/history-state'
import General from './general'
import Event from './event'


document.addEventListener('DOMContentLoaded', () => {
  historyState.setInitialPage()

  General.init()

  if (document.body.classList.contains('event-page')) {
    Event.init()
  }
})
