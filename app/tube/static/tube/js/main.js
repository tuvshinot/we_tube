const popupOpener = document.getElementById('account-popup');

const closeTogglePopup = () => {
    document.getElementById('popup').classList.toggle('hide')
}

popupOpener.addEventListener('click', closeTogglePopup);


