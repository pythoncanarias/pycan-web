const modalActions = ModalActions()

document.addEventListener('DOMContentLoaded', () => {
  if (document.body.classList.contains('event-page')) {
    modalActions.addListeners()

    window.addEventListener('hashchange', manageModalsBasedOnHash, false)

    const speakerId = getSpeakerIdFromHash()
    if (speakerId) {
      showInitialModal(speakerId)
    }
  }
})

function showInitialModal(speakerId) {
  history.replaceState(undefined, undefined, '.')
  modalActions.showModal(speakerId)
  history.pushState(undefined, undefined, `#speaker=${speakerId}`)
}

function manageModalsBasedOnHash() {
  modalActions.hideModal()

  const speakerId = getSpeakerIdFromHash()
  if (speakerId) {
    modalActions.showModal(speakerId)
  }
}

function getSpeakerIdFromHash() {
  const [speakerHash, speakerId] = window.location.hash.split('=')
  return speakerHash === '#speaker' ? speakerId : null
}


function ModalActions() {
  function addListeners() {
    document.querySelectorAll('.speaker-show-more').forEach(element => {
      element.addEventListener('click', showModalEvent, false)
    })
    document.querySelectorAll('.speaker-hide-modal').forEach(element => {
      element.addEventListener('click', hideModalEvent, false)
    })
  }

  function showModal(speakerId) {
    UTILS.addClass(`#modal-speaker-${speakerId}`, 'is-active')
    UTILS.addClass('html', 'no-scroll')

    document.addEventListener('keydown', hideModalWithEscKey, false)
  }

  function hideModal() {
    UTILS.removeClass('.speakers .modal.is-active', 'is-active')
    UTILS.removeClass('html', 'no-scroll')

    document.removeEventListener('keydown', hideModalWithEscKey, false)
  }

  function showModalEvent(event) {
    const speakerId = event.target.getAttribute('data-speaker-id')
    showModal(speakerId)
    history.pushState(undefined, undefined, `#speaker=${speakerId}`)
  }

  function hideModalWithEscKey(event) {
    event.key === 'Escape' && hideModalEvent()
  }

  function hideModalEvent() {
    hideModal()
    history.back()
  }

  return Object.freeze({
    addListeners,
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
