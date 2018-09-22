import ModalActions from './modal-actions'

const modalActions = ModalActions()

function init() {
  window.addEventListener('hashchange', manageModalsBasedOnHash, false)

  showInitialModal()
}

function showInitialModal() {
  const speakerId = getSpeakerIdFromUrlHash()
  if (speakerId) {
    history.replaceState({entry_page: true}, null, '')
    modalActions.showModal(speakerId)
  }
}

function manageModalsBasedOnHash() {
  modalActions.hideModal()

  const speakerId = getSpeakerIdFromUrlHash()
  if (speakerId) {
    modalActions.showModal(speakerId)
  }
}

function getSpeakerIdFromUrlHash() {
  const [speakerHash, speakerId] = window.location.hash.split('=')
  return speakerHash === '#speaker' ? speakerId : null
}

export default {
  init
}
