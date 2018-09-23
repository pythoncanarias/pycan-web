import modalsHandler from './modals/modals-handler'

export default {
  init: () => {
    modalsHandler.addScope('speaker')
    modalsHandler.addScope('slot')
    modalsHandler.handleModalsDependingOnUrlHash()
  }
}
