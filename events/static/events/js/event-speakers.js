const modalActions = ModalActions()

function init() {
  document.addEventListener('DOMContentLoaded', () => {
    if (document.body.classList.contains('event-page')) {
      window.addEventListener('hashchange', manageModalsBasedOnHash, false)

      showInitialModal()
    }
  })
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


const UTILS = {
  addClass(selector, _class) {
    const element = document.querySelector(selector)
    element && element.classList.add(_class)
  },

  removeClass(selector, _class) {
    const element = document.querySelector(selector)
    element && element.classList.remove(_class)
  }
}


export const initEventSpeakers = init
