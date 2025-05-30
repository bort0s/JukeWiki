const audio = document.getElementById("jukebox");
const title = document.getElementById("track-title");
const titleText = document.getElementById("track-title-text");
const playBtn = document.getElementById("play");
const volumeSlider = document.getElementById("volume");
const progressBar = document.getElementById("progress-bar");
const progressContainer = document.getElementById("progress-container");

let current = parseInt(localStorage.getItem("trackIndex")) || 0;

// === Carica e riprendi traccia ===
function loadTrack(i) {
  current = i;
  const track = tracks[i];
  if (!track) return;

  audio.src = track.file;

  // Aggiorna titoli
  if (title) title.textContent = track.title;
  if (titleText) titleText.textContent = track.title;

  // Salva dati
  localStorage.setItem("trackIndex", i);
  localStorage.setItem("trackTitle", track.title);
  localStorage.setItem("trackFile", track.file);

  // Quando i metadati sono pronti, imposta posizione e riprendi
  audio.onloadedmetadata = () => {
    const savedTime = parseFloat(localStorage.getItem("trackTime"));
    if (!isNaN(savedTime) && savedTime < audio.duration) {
      audio.currentTime = savedTime;
    }

    if (localStorage.getItem("isPlaying") === "true") {
      audio.play().then(() => {
        if (playBtn) playBtn.innerHTML = "⏸";
        document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.add("spin-center"));
      }).catch(() => {
        if (playBtn) playBtn.innerHTML = "▶";
      });
    }
  };

  if (typeof updateCarousel === "function") updateCarousel();

  // Forza rotazione dopo aggiornamento carousel
  if (!audio.paused) {
    document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.add("spin-center"));
  }
}

// === Play / Pause ===
function playPause() {
  if (audio.paused) {
    audio.play();
    if (playBtn) playBtn.innerHTML = "⏸";
    localStorage.setItem("isPlaying", "true");

    document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.add("spin-center"));

  } else {
    audio.pause();
    if (playBtn) playBtn.innerHTML = "▶";
    localStorage.setItem("isPlaying", "false");

    document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.remove("spin-center"));
  }
}

// === Navigazione tracce ===
function nextTrack() {
  current = (current + 1) % tracks.length;
  loadTrack(current);
  localStorage.setItem("isPlaying", "true");
  audio.play();
}

function prevTrack() {
  current = (current - 1 + tracks.length) % tracks.length;
  loadTrack(current);
  localStorage.setItem("isPlaying", "true");
  audio.play();
}

// === Event bindings ===
playBtn?.addEventListener("click", playPause);
document.getElementById("next")?.addEventListener("click", nextTrack);
document.getElementById("prev")?.addEventListener("click", prevTrack);

volumeSlider?.addEventListener("input", () => {
  audio.volume = volumeSlider.value;
  localStorage.setItem("volume", volumeSlider.value);
});

// === Salva tempo e aggiorna barra ===
audio.addEventListener("timeupdate", () => {
  localStorage.setItem("trackTime", audio.currentTime);

  if (progressBar && audio.duration) {
    const percent = (audio.currentTime / audio.duration) * 100;
    progressBar.style.width = percent + "%";
  }
});

// === Salto tramite click sulla barra ===
progressContainer?.addEventListener("click", (e) => {
  const rect = progressContainer.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const percent = clickX / rect.width;
  const newTime = percent * audio.duration;
  audio.currentTime = newTime;
  localStorage.setItem("trackTime", newTime);
});

// === Sync tra tab ===
window.addEventListener("storage", (e) => {
  if (e.key === "isPlaying") {
    const isPlaying = e.newValue === "true";
    if (isPlaying && audio.paused) {
      audio.play();
      if (playBtn) playBtn.innerHTML = "⏸";
      document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.add("spin-center"));
    } else if (!isPlaying && !audio.paused) {
      audio.pause();
      if (playBtn) playBtn.innerHTML = "▶";
      document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.remove("spin-center"));
    }
  }

  if (e.key === "trackIndex") {
    const newIndex = parseInt(e.newValue);
    if (!isNaN(newIndex) && newIndex !== current) {
      loadTrack(newIndex);
    }
  }
});

// === Avvio iniziale ===
if (!tracks[current]) {
  current = 0;
  localStorage.setItem("trackIndex", 0);
}

audio.volume = parseFloat(localStorage.getItem("volume")) || 0.4;
if (volumeSlider) volumeSlider.value = audio.volume;

loadTrack(current);

// Imposta icona corretta
if (localStorage.getItem("isPlaying") === "true") {
  if (audio.paused) {
    audio.play();
    if (playBtn) playBtn.innerHTML = "⏸";
    document.querySelectorAll(".vinyl-inner").forEach(v => v.classList.add("spin-center"));
  }
} else {
  if (playBtn) playBtn.innerHTML = "▶";
}
audio.addEventListener("ended", () => {
  nextTrack();
});