const cards = document.querySelectorAll('.card');
const popups = document.querySelectorAll('.popup');
const closeButtons = document.querySelectorAll('.close-button');
const expandableSections = document.querySelectorAll('.expandable_section');
const expandables = document.querySelectorAll('.expandable_card');

function getJson(section){
	fetch('./descriptions.json')
		.then(res => res.json())
		.then(data => {
      data_filter = data.filter( feature => feature.pillar_id == pillarNum);
			data_filter.forEach(feature => {
        section.insertAdjacentHTML('beforeend', 
          `
          <div class="expandable_card_wrapper">
            <div class="expandable_card">
              <div class = "expandable_icon">
                <ion-icon name="chevron-down-outline"></ion-icon>
              </div>
              <h5 class="expandable_title">${feature.feature_name}</h5>
              <p class="expandable_body">${feature.feature_brief}</p>
              <div class="expandable_footer">
                <small class="text-muted">Feature ${feature.pillar_id}-${feature.feature_num}</small>
                <small class="text-muted">${feature.facet}</small>
              </div>
            </div>
            <div class="expandable_content_wrapper">
              <div class="expandable_content">
                <p>${feature.feature_use_case}</p>
              </div>
            </div>
          </div>
          `
        );
      })
		});
}

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

expandableSections.forEach(expandableSection => {
	getJson(expandableSection);
});

expandables.forEach(expandable => {
  expandable.addEventListener('click', () => {
    expandable.parentNode.classList.toggle("expandable_card-open");
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".expandable_card").forEach((expandable) => {
    expandable.addEventListener('click', () => {
      expandable.parentNode.classList.toggle("expandable_card-open");
    });
  });
});