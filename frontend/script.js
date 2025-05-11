// Sections and Navigation
function showOnly(id) {
  const sections = ['intro', 'floor-select', 'gallery', 'floor4-description', 'art-detail'];
  sections.forEach(sectionId => {
    const el = document.getElementById(sectionId);
    if (el) el.classList.add('hidden');
  });

  const active = document.getElementById(id);
  if (active) active.classList.remove('hidden');

  pauseAllAudio();

  const footer = document.getElementById('legal-footer');
  if (footer) {
    footer.classList.toggle('hidden', id !== 'intro');
  }
}

function pauseAllAudio() {
  const audios = document.querySelectorAll('audio');
  audios.forEach(a => {
    a.pause();
    a.currentTime = 0;
  });
}

function showIntro() {
  showOnly('intro');
}

function showFloorSelect() {
  showOnly('floor-select');
}

function showGallery() {
  showOnly('gallery');
}

function startGallery() {
  history.pushState({ page: 'floor-select' }, '', '#floor-select');
  showFloorSelect();
}

function enterGallery(floor) {
  history.pushState({ page: `${floor}-description` }, '', `#${floor}-description`);
  showFloorDescription(floor);
}

function enterFloorGrid(floor) {
  history.pushState({ page: `${floor}-grid` }, '', '#gallery');
  showGallery();
}

function goBack() {
  history.back();
}

window.addEventListener('popstate', () => {
  const hash = location.hash;

  if (hash.includes('gallery')) {
    showGallery();
  } else if (hash.includes('floor4-description')) {
    showFloorDescription('floor4');
  } else if (hash === '#floor-select') {
    showFloorSelect();
  } else if (hash === '#art-detail') {
    showOnly('art-detail');
  } else {
    showIntro();
  }
});

if (location.hash === '#gallery') {
  showGallery();
} else if (location.hash === '#floor4-description') {
  showFloorDescription('floor4');
} else if (location.hash === '#floor-select') {
  showFloorSelect();
} else {
  showIntro();
}

function showFloorDescription(floorId) {
  showOnly(`${floorId}-description`);
}

// ------- Dynamic Gallery Logic -------

async function loadGallery() {
  try {
    const response = await fetch('assets/data/munchmuseet_data.json');
    const data = await response.json();

    const galleryContainer = document.getElementById("gallery-grid");
    galleryContainer.innerHTML = ""; // Clear existing content

    data.forEach((item, index) => {
      const div = document.createElement("div");
      div.className = "gallery-item";
      div.onclick = () => openArtwork(index);

      div.innerHTML = `
        <p class="art-title">${item.title}</p>
        <img class="art-image" src="${item.image}" alt="${item.title}" />
      `;

      galleryContainer.appendChild(div);
    });

    window.galleryData = data; // Store for access in openArtwork
  } catch (error) {
    console.error("Failed to load gallery data:", error);
  }
}

function openArtwork(index) {
  const item = window.galleryData?.[index];
  if (!item) return;

  document.getElementById('art-title').textContent = item.title;
  document.getElementById('art-image').src = item.image;
  document.getElementById('art-image').alt = item.title;
  document.getElementById('art-audio').src = item.audio;

  const creditsEl = document.querySelector(".art-credits");
  creditsEl.innerHTML = `
    <p>Edvard Munch, ${item.original_name}${item.year ? ', ' + item.year : ''}. Photo © Munchmuseet${item.photographer_name ? ' / ' + item.photographer_name : ''}</p>
    <p>Audio: Kamand Shayegan, Originally read by ${item.original_reader_s || "Unknown"}</p>
  `;

  history.pushState({ page: 'art-detail' }, '', '#art-detail');
  showOnly('art-detail');

  // Set PDF link dynamically
  const pdfLink = document.getElementById("pdf-link");
  pdfLink.href = `assets/pdfs/transc_fa_${index + 1}.pdf`;
}



// Load gallery on DOM load
document.addEventListener("DOMContentLoaded", loadGallery);
