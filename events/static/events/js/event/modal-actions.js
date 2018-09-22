import UTILS from '../utils'

function ModalActions() {
  function showModal(speakerId) {
    UTILS.addClass(`#modal-speaker-${speakerId}`, 'is-active')
    UTILS.addClass('html', 'no-scroll')

    addEventListeners()
  }

  function hideModal() {
    UTILS.removeClass('.speakers .modal.is-active', 'is-active')
    UTILS.removeClass('html', 'no-scroll')

    removeEventListeners()
  }

  function addEventListeners() {
    document.addEventListener('keydown', hideModalWhenEscKeyIsPressed, false)
    document.querySelectorAll('.modal.is-active .speaker-hide-modal').forEach(element => {
      element.addEventListener('click', hideModalThroughUserInteraction, false)
    })
  }

  function removeEventListeners() {
    document.removeEventListener('keydown', hideModalWhenEscKeyIsPressed, false)
    document.querySelectorAll('.modal.is-active .speaker-hide-modal').forEach(element => {
      element.addEventListener('click', hideModalThroughUserInteraction, false)
    })
  }

  function hideModalWhenEscKeyIsPressed(event) {
    event.key === 'Escape' && hideModalThroughUserInteraction()
  }

  function hideModalThroughUserInteraction() {
    history.state && history.state.entry_page ? goToEventPage() : history.back()
  }

  function goToEventPage() {
    window.location.hash = '#'
    history.replaceState(null, null, '.')
  }

  return Object.freeze({
    showModal,
    hideModal
  })
}

export default ModalActions
