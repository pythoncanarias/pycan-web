document.addEventListener('DOMContentLoaded', () => {
  initNavbarBurguer()
})

function initNavbarBurguer() {
  const navbarBurger = document.querySelector('.navbar-burger')

  navbarBurger.addEventListener('click', () => {
    const menuId = navbarBurger.getAttribute('data-target')
    const menu = document.getElementById(menuId)

    navbarBurger.classList.toggle('is-active')
    menu.classList.toggle('is-active')
  })
}
