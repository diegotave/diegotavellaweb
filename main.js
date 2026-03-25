// ── main.js — HOME ────────────────────────────────────────────────────────

// ── SCRAMBLE CONFIG ───────────────────────────────────────────────────────
const CHARS      = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&?";
const FRAME_MS   = 45;    // velocidad del scramble (ms por frame)
const LOCK_DELAY = 90;    // ms entre cada letra que se tilda
const START_DELAY = 200;  // ms antes de arrancar la animación

// ── SCRAMBLE ──────────────────────────────────────────────────────────────
const chars   = document.querySelectorAll(".logo-char");
const logoSub = document.getElementById("logo-sub");
const navBtn  = document.querySelector(".nav-btn");

let intervals = [];
let lockTimers = [];

function randomChar() {
  return CHARS[Math.floor(Math.random() * CHARS.length)];
}

function startScramble() {
  // Arrancar todos los chars scrambliando a la vez
  chars.forEach(el => {
    el.classList.add("scrambling");
    const iv = setInterval(() => {
      el.textContent = randomChar();
    }, FRAME_MS);
    intervals.push(iv);
  });

  // Tildar de a una, en orden, con delay acumulativo
  chars.forEach((el, i) => {
    const t = setTimeout(() => {
      // Detener el interval de este char
      clearInterval(intervals[i]);
      // Restablecer la letra correcta
      el.textContent = el.dataset.char;
      el.classList.remove("scrambling");
      el.classList.add("locked");

      // Cuando se tilda la última letra, mostrar POSTPRODUCTION y nav
      if (i === chars.length - 1) {
        setTimeout(() => {
          logoSub.classList.add("visible");
          navBtn.classList.add("ready");
        }, 200);
      }
    }, START_DELAY + LOCK_DELAY * i);

    lockTimers.push(t);
  });
}

// Iniciar scramble apenas carga la página
window.addEventListener("DOMContentLoaded", () => {
  // Scramble inmediato: poner chars random desde el vamos
  chars.forEach(el => { el.textContent = randomChar(); });
  setTimeout(startScramble, START_DELAY);
});