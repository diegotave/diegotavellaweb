// ── works.js — GRILLA DE VIDEOS ───────────────────────────────────────────

const R2 = "https://pub-4ad247018d50485fa0850c9164489c59.r2.dev";

// ── DATA ─────────────────────────────────────────────────────────────────
// Agregar o quitar items acá — la grilla se adapta sola
// ratio: "16-9" | "9-16" | "1-1"
// type:  "reel" | "work"
// video: URL en R2 (opcional, si no hay se muestra el thumb)
// thumb: URL en R2 (imagen de portada)

const works = [
  {
    id:    "reel",
    title: "Demo Reel",
    type:  "reel",
    ratio: "16-9",
    thumb: R2 + "/WORKS/reel/thumb.jpg",
    video: R2 + "/WORKS/reel/reel.mp4",
  },
  // — agregar trabajos acá —
  // {
  //   id:    "trabajo-01",
  //   title: "Título del trabajo",
  //   type:  "work",
  //   ratio: "16-9",          // "16-9" | "9-16" | "1-1"
  //   thumb: R2 + "/WORKS/trabajo-01/thumb.jpg",
  //   video: R2 + "/WORKS/trabajo-01/clip.mp4",  // opcional
  // },
];

// ── RENDER ────────────────────────────────────────────────────────────────
const grid = document.getElementById("works-grid");

function renderWorks(){
  grid.innerHTML = "";

  works.forEach(w => {
    const item = document.createElement("div");
    item.className = "work-item" + (w.type === "reel" ? " is-reel" : "");
    item.dataset.ratio = w.ratio;
    item.dataset.id    = w.id;

    // Thumbnail
    if(w.thumb){
      const img = document.createElement("img");
      img.src = w.thumb;
      img.alt = w.title;
      img.loading = "lazy";
      item.appendChild(img);
    }

    // Info overlay
    const info = document.createElement("div");
    info.className = "work-item__info";
    info.innerHTML = `
      <p class="work-item__title">${w.title}</p>
      <p class="work-item__type">${w.type === "reel" ? "Demo Reel" : "Work"}</p>
    `;
    item.appendChild(info);

    // Click — abrir video (por ahora placeholder)
    item.addEventListener("click", () => openWork(w));

    grid.appendChild(item);
  });
}

// ── OPEN WORK — placeholder, se implementa con el diseño del player ───────
function openWork(work){
  console.log("Abrir:", work.title, work.video);
  // próxima etapa: modal o página de player
}

// ── INIT ──────────────────────────────────────────────────────────────────
renderWorks();
