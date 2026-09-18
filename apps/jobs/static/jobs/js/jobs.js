const SHOW_JOB_BTN_TEXT =
  '<i class="fas fa-chevron-circle-down"></i> Mostrar descripción'
const HIDE_JOB_BTN_TEXT =
  '<i class="fas fa-chevron-circle-up"></i> Ocultar descripción'

document.querySelectorAll('.btn-toggle-job-description').forEach((item) => {
  item.addEventListener('click', function (event) {
    event.preventDefault()
    const srcButton = event.srcElement
    const jobDescription = srcButton.nextElementSibling
    const jobDescriptionMaxHeight = getComputedStyle(jobDescription, null)[
      'max-height'
    ]

    jobDescription.classList.toggle('job-description-text-show')
    if (jobDescriptionMaxHeight === '0px') {
      srcButton.innerHTML = HIDE_JOB_BTN_TEXT
    } else {
      srcButton.innerHTML = SHOW_JOB_BTN_TEXT
    }
  })
})
