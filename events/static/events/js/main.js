import General from './general'
import Event from './event'


document.addEventListener('DOMContentLoaded', () => {
  General.init()

  if (document.body.classList.contains('event-page')) {
    Event.init()
  }
})
