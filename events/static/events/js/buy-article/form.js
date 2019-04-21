function init() {
  const handler = getInitializedStripe()

  document.getElementById('button-go-to-payment').addEventListener('click', function (event) {
    event.preventDefault()

    if (validateForm()) {
      handler.open()
    }
  })
}

function getInitializedStripe() {
  return StripeCheckout.configure({
    key: window.STRIPE_SETTINGS.key,
    name: 'Python Canarias',
    description: window.STRIPE_SETTINGS.description,
    image: '/static/commons/img/logo-no-margin.png',
    locale: 'auto',
    currency: 'EUR',
    amount: window.STRIPE_SETTINGS.amount,
    zipCode: true,
    token: onCompletedCheckout,
  })
}

function onCompletedCheckout(token) {
  document.querySelector('.spinner-background').classList.remove('is-hidden')

  const form = document.getElementById('buy-article-form')

  const stripeTokenInput = createHiddenInput('stripeToken', token.id)
  const stripeEmailInput = createHiddenInput('stripeEmail', token.email)

  form.appendChild(stripeTokenInput)
  form.appendChild(stripeEmailInput)

  form.submit()
}

function createHiddenInput(name, value) {
  const input = document.createElement('input')
  input.setAttribute('type', 'hidden')
  input.setAttribute('name', name)
  input.setAttribute('value', value)
  return input
}

function validatePhone(phone) {
  return phone.match(/^\+?\d{9,20}/)
}

function validateForm() {
  let isValid = true

  hideValidationMessages()

  if (document.getElementById('name-input').value.trim() === '') {
    isValid = false
    showValidationMessage('name-validation-message')
  } else if (document.getElementById('surname-input').value.trim() === '') {
    isValid = false
    showValidationMessage('surname-validation-message')
  } else {
    let cleanedPhone = document.getElementById('phone-input').value.trim()
    if (cleanedPhone.length > 0 && !validatePhone(cleanedPhone)) {
      isValid = false
      showValidationMessage('phone-validation-message')
    }
    else if (document.querySelectorAll('.terms input[type=checkbox]:checked').length !== 2) {
      isValid = false
      showValidationMessage('checkboxes-validation-message')
    }
  }

  return isValid
}

function hideValidationMessages() {
  document.querySelectorAll('.validation-message').forEach((element) => {
    element.classList.add('is-hidden')
  })
}

function showValidationMessage(validationMessageId) {
  document.getElementById(validationMessageId).classList.remove('is-hidden')
}

export default {
  init
}


