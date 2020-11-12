import historyState from '../../utils/history-state'
import Modal from './modal'

function ModalsHandler() {
  let currentModal
  let scopes = []

  window.addEventListener('hashchange', handleModalsDependingOnUrlHash, false)

  function addScope(scope) {
    scopes.push(scope)
  }

  function handleModalsDependingOnUrlHash() {
    currentModal && currentModal.close()
    currentModal = null

    const [hashScope, hashId] = window.location.hash.slice(1).split('=')
    if (scopes.includes(hashScope)) {
      openModalIfExists(hashScope, hashId)
    }
  }

  function openModalIfExists(scope, id) {
    const onClose = historyState.isInitialPage() ? goToBasePage : goToPreviousPage

    const modalElement = document.querySelector(`#modal-${scope}-${id}`)
    if (modalElement) {
      currentModal = Modal({ modalElement, onClose })
      currentModal.open()
    }
  }

  function goToBasePage() {
    window.location.hash = '#'
    history.replaceState(null, null, '.')
  }

  function goToPreviousPage() {
    history.back()
  }

  return Object.freeze({
    addScope,
    handleModalsDependingOnUrlHash
  })
}

export default ModalsHandler()
