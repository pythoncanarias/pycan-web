export default {
  setInitialPage: () => {
    window.history.replaceState({ is_initial: true }, null, '.')
  },

  isInitialPage: () => {
    return window.history.state && window.history.state.is_initial
  }
}
