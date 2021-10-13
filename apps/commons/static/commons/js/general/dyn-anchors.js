function init() {
    document.querySelectorAll('.dyn-anchor-heading').forEach((item) => {
        item.addEventListener('mouseenter', function(event) {
            event.preventDefault()
            let anchor = event.target.querySelector('.dyn-anchor-link')
            anchor.classList.add('show-it')
        })
        item.addEventListener('mouseleave', function(event) {
            event.preventDefault()
            let anchor = event.target.querySelector('.dyn-anchor-link')
            anchor.classList.remove('show-it')
        })
    })
}

export default {
    init
}
