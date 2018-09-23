function Modal({ modalElement, onClose = close}) {
  const htmlElement = document.querySelector('html')
  const hidersElements = modalElement.querySelectorAll('.hide-modal')

  function open() {
    modalElement.classList.add('is-active')
    htmlElement.classList.add('no-scroll')

    addEventListeners()
  }

  function close() {
    modalElement.classList.remove('is-active')
    htmlElement.classList.remove('no-scroll')

    removeEventListeners()
  }

  function addEventListeners() {
    document.addEventListener('keydown', closeModalWhenEscKeyIsPressed, false)
    hidersElements.forEach(element => {
      element.addEventListener('click', onClose, false)
    })
  }

  function removeEventListeners() {
    document.removeEventListener('keydown', closeModalWhenEscKeyIsPressed, false)
    hidersElements.forEach(element => {
      element.removeEventListener('click', onClose, false)
    })
  }

  function closeModalWhenEscKeyIsPressed(event) {
    event.key === 'Escape' && onClose()
  }

  return Object.freeze({
    open,
    close
  })
}

export default Modal
