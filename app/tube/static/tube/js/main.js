const popupOpener = document.getElementById('account-popup');

const closeTogglePopup = () => {
    document.getElementById('popup').classList.toggle('hide')
}

popupOpener.addEventListener('click', closeTogglePopup);


// onclick send to url
const sendToUrl = (url) => window.location.href = window.location.origin + url + '?next=' + window.location.pathname;