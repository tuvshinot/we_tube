const popupOpener = document.getElementById('account-popup');

const closeTogglePopup = () => {
    document.getElementById('popup').classList.toggle('hide')
}

popupOpener.addEventListener('click', closeTogglePopup);

// document.getElementById('popup-sign-up').addEventListener('click', () => {
//     closeTogglePopup()
//     centeredPopup('http://127.0.0.1:8000/auth/signup', 'Sign up')
// })

// document.getElementById('popup-sign-in').addEventListener('click', () => {
//     closeTogglePopup()
//     centeredPopup('http://127.0.0.1:8000/auth/signin', 'Sign in')
// })


function centeredPopup(url, winName) {
    const fromLeft = (screen.width - 500) / 2
    const fromTop = (screen.height - 600) / 2

    settings = 'height=600 ,width=500 ,top=' + fromTop + ',left=' + fromLeft + ',resizable'
    popupWindow = window.open(url, winName, settings)
}