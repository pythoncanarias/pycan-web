export default {
  addClass(selector, _class) {
    const element = document.querySelector(selector)
    element && element.classList.add(_class)
  },

  removeClass(selector, _class) {
    const element = document.querySelector(selector)
    element && element.classList.remove(_class)
  }
}
