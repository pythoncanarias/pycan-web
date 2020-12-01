function init() {
  document.getElementById('btn-make-matching').addEventListener('click', function (event) {
    event.preventDefault()

    let awardedTicket = document.getElementById('awarded-ticket')
    if (awardedTicket)
      awardedTicket.style.display = 'none'

    let button = document.getElementById('btn-make-matching')
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sorteando!'
    button.setAttribute('disabled', 'disabled')

    setTimeout(function () {
      window.location.href = button.href
    }, 2000);
  })
}

export default {
  init
}
