const cards = document.querySelectorAll('.card');
const popups = document.querySelectorAll('.popup');
const closeButtons = document.querySelectorAll('.close-button');


cards.forEach(card => {
    card.addEventListener('click', () => {
      const targetPopup = card.nextElementSibling;
      targetPopup.style.display = 'block';
      setTimeout(() => {
        targetPopup.classList.add('active');
      }, 50);
    });
});

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const popup = button.closest('.popup');
    popup.classList.remove('active'); 
    setTimeout(() => {
      popup.style.display = 'none';
    }, 300); 
  });
});

popups.forEach(popup => {
  popup.addEventListener('click', (event) => {
    if (event.target == popup) {
      popup.classList.remove('active');
      setTimeout(() => {
        popup.style.display = 'none';
      }, 300); 
    }
  });
});
