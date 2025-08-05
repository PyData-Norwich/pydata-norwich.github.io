function showNavbar() {
    document.querySelector('.navbar-links').classList.toggle('show')
}

function showDropDown(button) {
    const dropdown = button.parentElement
    
    content = dropdown.querySelector('.dropdown-content')
    content.classList.toggle('show')
}

function showDetails(button) {

    const post_content = button.parentElement.parentElement.parentElement

    detail_elements = post_content.querySelector('.event-details').querySelectorAll('.event-detail')

    for (el of detail_elements) {        
        el.classList.toggle('show')
    }

    show = (button.dataset.show === 'true')

    button.dataset.show = show ? 'false' : 'true'

    button.innerHTML = show ? 'show details' : 'hide details'

}