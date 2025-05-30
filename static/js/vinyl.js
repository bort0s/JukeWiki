const carousel = document.getElementById("carousel");

function createVinyl(position, trackIndex) {
  const vinyl = document.createElement("div");
  vinyl.className = "carousel-vinyl " + position;

  const inner = document.createElement("div");
  inner.className = "vinyl-inner";

  const disc = document.createElement("div");
  disc.className = "vinyl-disc";

  const rings = document.createElement("div");
  rings.className = "vinyl-rings";

  const cover = document.createElement("img");
  cover.src = tracks[trackIndex].cover;
  cover.className = "vinyl-cover";

  const hole = document.createElement("div");
  hole.className = "vinyl-hole";

  disc.appendChild(rings);
  disc.appendChild(cover);
  disc.appendChild(hole);
  inner.appendChild(disc);
  vinyl.appendChild(inner);
  carousel.appendChild(vinyl);

  if (position === "center" && !audio.paused) {
    inner.classList.add("spin-center");
  }
}

function updateCarousel() {
  const carousel = document.getElementById("carousel");
  if (!carousel) return;

  carousel.innerHTML = "";

  const prevIndex = (current - 1 + tracks.length) % tracks.length;
  const nextIndex = (current + 1) % tracks.length;

  createVinyl("left", prevIndex);
  createVinyl("center", current);
  createVinyl("right", nextIndex);

  const trackTitle = document.getElementById("track-title");
  const trackText = document.getElementById("track-title-text");
  if (trackTitle) trackTitle.textContent = tracks[current].title;
  if (trackText) trackText.textContent = tracks[current].title;

  localStorage.setItem("trackIndex", current);
}


// un solo set di listener per i bottoni
document.getElementById("next").addEventListener("click", nextTrack);
document.getElementById("prev").addEventListener("click", prevTrack);

// Aggiorna carosello al primo load
if (document.getElementById("carousel")) {
  updateCarousel();
}

window.addEventListener("storage", (e) => {
  if (e.key === "trackIndex") {
    current = parseInt(e.newValue);
    updateCarousel();
  }
});