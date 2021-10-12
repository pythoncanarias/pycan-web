import NavbarBurger from './navbar-burger'
import Notifications from './notifications'
import Collapsable from './collapsable'
import ScrollUpButton from './scrollUpButton'

export default {
  init: () => {
    NavbarBurger.init()
    Notifications.init()
    Collapsable.init()
    ScrollUpButton.init()
  },
}
