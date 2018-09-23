import modalsHandler from './modals/modals-handler'

export default {
  init: () => {
    modalsHandler.addScope('speaker')
    modalsHandler.handleModalsDependingOnUrlHash()
  }
}
