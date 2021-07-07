const sidebar = {
    visibility: false,
    position: document.querySelector('#sidebar')
}

const menu = document.querySelector('.hiddenNav')
console.log(sidebar.visibility)
menu.addEventListener('click', function(){
    sidebar.visibility =! sidebar.visibility
    sidebar.visibility ? sidebar.position.classList.add('sidebarNotHidden') : sidebar.position.classList.remove('sidebarNotHidden')
})