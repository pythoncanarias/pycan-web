import NavbarBurger from './navbar-burger'
import Notifications from './notifications'
import Collapsable from './collapsable'
import ScrollUpButton from './scrollUpButton'
import DynAnchors from './dyn-anchors'

export default {
  init: () => {
    NavbarBurger.init()
    Notifications.init()
    Collapsable.init()
    ScrollUpButton.init()
    DynAnchors.init()
  },
}
