# diegotavellaweb

Portfolio personal de Diego Tavella. Sitio web de acceso restringido (password gate) con videoteca de works.

---

## Archivos activos

| Archivo | Rol |
|---|---|
| `index.html` | Entrada — password gate + video intro (`logointro3.webm`) → redirige a `hom3dtv.html` |
| `index.css` | Estilos compartidos por `index.html` y `hom3dtv.html` |
| `hom3dtv.html` | Home — VHS cassette animado, botón "play demo" y "watch some work" |
| `workka.html` | Works — videoteca de VHS spines + player |
| `workka.css` | Estilos de `workka.html` |

> `work.html`, `works.html`, `texture-diagonal.html` son archivos legacy/experimentales, no están en el flujo activo.

---

## Flujo de navegación

```
index.html (gate + logointro3.webm)
    → hom3dtv.html (VHS cassette)
        → [click "play demo"]  → workka.html (autoplay video 1)
        → [click "watch work"] → introwork.webm overlay → workka.html
        → [back desde workka]  → pushBack animation → hom3dtv.html
```

**Transición hom3dtv → workka:** se crea un `<video>` overlay con `introwork.webm` sobre la página, `hom3dtv` se oculta a los 5 frames (~167ms), workka arranca cuando el video termina (`skipIntro` en sessionStorage).

**Transición workka → hom3dtv:** botón home setea `pushBack` en sessionStorage, hom3dtv lo lee al cargar y hace un slide-in desde arriba.

---

## Sistema de temas

Persiste en `localStorage` bajo la clave `"theme"`. Valores: `orange` (default) · `dark` · `red` · `light`.

El tema se aplica como clase en `<body>` mediante un inline script al inicio del body (evita FOUC).

| Clase body | Fondo | Frame border |
|---|---|---|
| `.orange` (default) | `rgb(255,170,0)` | blanco |
| *(ninguna = dark)* | `#000` | blanco |
| `.red` | `#FF2200` | blanco |
| `.light` | `#fff` | negro |

El frame visible es un `body::after` con `position:fixed; inset:10px; box-shadow: 0 0 0 20px [color]` — se define en `index.css` (para index/hom3dtv) y en `workka.css` (para workka).

El panel de temas está en ambas páginas como `#blend-panel` (fixed, derecha).

---

## Botones en hom3dtv

### `#boton-demo` / hit: `#boton-hit`
Botón circular — "play demo" — reproduce el reel (video 1) al navegar a workka.

### `#boton-cuadrado` / hit: `#boton-hit-cuadrado`
Botón rectangular — "watch some work" — navega a workka mostrando la videoteca.
- El fondo naranja (`#boton-fondo`) se expande hacia la derecha en hover via `width` CSS transition.
- El texto se revela con `clip-path: inset(0 100% 0 0)` → `inset(0 0% 0 0)`.
- El triángulo de play parpadea (`play-blink` keyframe) y se detiene en hover.
- El ancho del hover se calcula dinámicamente en JS (`setFondoWidth`).
- En touch: tap 1 activa hover, tap 2 navega.
- Al hover se reproduce `video-somework` (preview del reel).

---

## Videoteca (workka)

### Estructura DOM generada por JS
```
#shelf-wrap
  └─ #shelf-rail
       └─ .vhs-spine[data-index]  ×9
            └─ .vhs-visual
                 ├─ .vhs-cover   (thumbnail, img)
                 ├─ .vhs-png     (overlay lomo VHS, img)
                 └─ .vhs-label   (título)
```

- `#shelf-wrap` posicionado con `bottom: -44vh` dentro de `#stage` (overflow hidden), creando el efecto de estantería emergente desde abajo.
- `calibrateBlock()` calcula el `height` del rail para que los visuals llenen exactamente el frame interior.
- Hover en landscape: el spine activo sube al centro del frame (`translateY`), los demás bajan fuera del stage.
- Click: abre el player (`openPlayer`) con animación `clipPath circle`.
- Tilt: efecto de inclinación por velocidad del mouse (`rotateZ`).

### Filtros de color por tema
- Default (dark): `filter: saturate(0)` en reposo, `saturate(1) invert(1)` en activo (excepto `vhslomo2`).
- Orange/light: `saturate(1)` sin invert en activo.

### Ruler
Línea de texto con dashes que aparece al elevar un spine, mostrando el título del video.

---

## Botón home (workka → hom3dtv)

Mismo diseño que `#boton-cuadrado` de hom3dtv. Texto: "home".

- Posicionado por JS (`positionHomeBtn`) en `#stage` como `position: absolute`.
- **Landscape**: top ~6% del stage, left alineado con el primer VHS spine.
- **Portrait phone**: top 60px (alineado con primer spine), right 16px (mismo margen que blend-panel). Hover se expande hacia la **izquierda**.
- Hit area separada (`#home-hit`) que se expande al ancho del hover para evitar flickering.
- Click: setea `pushBack` en sessionStorage y navega a `hom3dtv.html`.

---

## Breakpoints definidos (implementación pendiente)

| Target | Media query |
|---|---|
| **Landscape desktop** | base (sin query) — ≥ 1024px landscape |
| **Landscape tablet** | `@media (orientation: landscape) and (max-width: 1366px)` |
| **Portrait phone** | `@media (orientation: portrait) and (max-width: 767px)` |

> Actualmente el portrait usa solo `@media (orientation: portrait)` sin límite de ancho. Pendiente acotar a `max-width: 767px` y separar estilos por breakpoint con valores fijos en lugar de fórmulas fluidas.

---

## Videos

| Archivo | Uso |
|---|---|
| `logointro3.webm` | Intro animada en index.html |
| `vhsindex.webm` | VHS cassette animado en hom3dtv |
| `introwork.webm` | Transición hom3dtv → workka |
| `tagsomework.webm` | Preview en hover del botón "watch some work" |

Videos de works: alojados en Cloudflare R2 (`https://pub-5dae75b9216945058a34d5462aa57b48.r2.dev/WORKS/...`).
