'use strict'

function init() {
  const collapsableItems = document.querySelectorAll('.js-nav-item')
  for (const collapsableItem of collapsableItems) {
    collapsableItem.addEventListener('click', (ev) => {
      ev.preventDefault()
      const clickedItem = ev.currentTarget
      const clickedCollapsable = clickedItem.parentNode

      const allCollapsables = document.querySelectorAll('.js-nav-dropdown')
      for (const collapsable of allCollapsables) {
        // compruebo si es el collapsable pulsado
        if (clickedCollapsable === collapsable.parentNode) {
          // si es el pulsado, le hago un toggle
          console.log(collapsable)
          collapsable.classList.toggle('collapsable--close')
        } else {
          console.log('else')
          // si no es el pulsado, lo cierro
          collapsable.classList.add('collapsable--close')
        }
      }
    })
  }
}

export default {
  init,
}
