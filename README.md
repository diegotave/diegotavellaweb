# diegotavellaweb

Portfolio personal de Diego Tavella. Sitio web de acceso restringido (password gate) con videoteca de works y sección de contacto.

---

## Archivos activos

| Archivo | Rol |
|---|---|
| `index.html` | Entrada — password gate + video intro → redirige a `hom6dtv.html` |
| `index.css` | Estilos compartidos |
| `hom6dtv.html` | Home — logo animado (`armalogo_hom6dtv.webm`), swipe up → `workka2.html`, swipe down → `ajuste.html` |
| `workka2.html` | Works + Contact — página única de `200dvh`, dos secciones en `#pages-wrap` |
| `workka2.css` | Estilos de `workka2.html` |
| `hom4dtv.html` | Destino del botón home dentro de workka2 |

> `hom3dtv.html`, `workka.html`, `workka.css`, `contact.html`, `contact2.html` son archivos legacy/experimentales, no están en el flujo activo.

---

## Flujo de navegación

```
index.html (gate + logointro.webm)
    → hom6dtv.html (armalogo animado)
        → [swipe up]   → workka2.html — sección WORK
            → [swipe up]   → workka2.html — sección CONTACT (mismo DOM, push in-page)
            → [swipe down] → workka2.html — sección WORK
            → [swipe down desde WORK] → hom6dtv.html
            → [botón home] → hom4dtv.html
        → [swipe down] → ajuste.html
```

---

## Sistema de página única (workka2.html)

Work y Contact son dos secciones de `100dvh` dentro de un `#pages-wrap` de `200dvh`.

```html
<div id="pages-wrap">          <!-- 200dvh, transición con translateY -->
  <div id="screen-work">       <!-- 100dvh — videoteca VHS -->
    <div id="stage"> … </div>
  </div>
  <div id="screen-contact">    <!-- 100dvh — sección CONTACT -->
    <div id="contact-stage"> … </div>
  </div>
</div>
```

- `body` tiene `overflow: hidden` y `height: 100dvh` — actúa como viewport.
- La transición entre secciones es un `translateY` sobre `#pages-wrap` con `transition: transform 700ms cubic-bezier(0.4,0,0.2,1)`.
- Estado gestionado por `_pageState = 'work' | 'contact'` + `_exitTriggered` con cooldown.
- Al hacer resize mientras se está en contact, se recalcula el offset sin transición.
- `pageshow` resetea el estado a `work` al volver desde hom6dtv (BFCache).

---

## Videoteca VHS (sección WORK)

### Estructura DOM generada por JS
```
#shelf-wrap
  └─ #shelf-rail
       └─ .vhs-spine[data-index]  ×7
            └─ .vhs-visual
                 ├─ .vhs-png     (imagen lomo coloreado)
                 └─ .vhs-label   (título)
```

- `#shelf-wrap` posicionado con `bottom: -74vh` dentro de `#stage` (overflow hidden).
- `calibrateBlock()` calcula el `height` del rail para que los visuals llenen el frame interior.
- Los spines entran animados desde abajo (`spine-enter` keyframe) con stagger de 60ms.
- Hover en landscape: el spine activo sube al centro del frame (`translateY`), los demás bajan fuera del stage.
- Tilt: efecto de inclinación por velocidad del mouse (`rotateZ`).
- Ruler: línea de dashes con el título del video activo.

### Portrait
- El rail se convierte en columna vertical a la izquierda (40vw).
- Las imágenes `.vhs-png` se rotan 90° y se posicionan en la derecha del spine.
- El botón home se mueve a la esquina superior derecha.

---

## Sección CONTACT

Mismos VHS que WORK pero pre-renderizados (sin animación de entrada), posicionados con:

- `calibrateContact()`: `railHeight = (stageH - 40) / 0.85`, `shelf-wrap.bottom = window.innerHeight * 0.26`
- El `bottom: 26vh` alinea el borde inferior de los VHS con el borde superior del viewport de WORK (`-74vh`), creando continuidad visual tipo rompecabezas en la transición.

---

## Botón home (workka2 → hom4dtv)

- Posicionado por JS en `#stage` como `position: absolute`.
- **Landscape**: top ~6% del stage, left alineado con el primer VHS spine.
- **Portrait**: top 60px, right 16px. Hover se expande hacia la izquierda.
- Hit area separada (`#home-hit`) que se expande al ancho del hover.
- Parpadeo del triángulo de play (`home-blink`) que se detiene en hover.

---

## Transición hom6dtv → workka2

`hom6dtv.html` setea `sessionStorage('from_hom6dtv', '1')` antes de navegar.

`workka2.html` lo lee al cargar: crea un `<video>` overlay con `armalogo_hom6dtv.webm` pausado en el último frame, anima el logo hacia la posición del botón home y lo desvanece. Esto crea la ilusión de continuidad visual entre las dos páginas.

---

## Imágenes VHS (lomos)

| Archivo | Color |
|---|---|
| `vhslomorojo.png` | Rojo |
| `vhslomonaranja.png` | Naranja |
| `vhslomoamarillo.png` | Amarillo |
| `vhslomoverde.png` | Verde |
| `vhslomocian.png` | Cian |
| `vhslomovioleta.png` | Violeta |
| `vhslomorosa.png` | Rosa |

---

## Videos

| Archivo | Uso |
|---|---|
| `armalogo_hom6dtv.webm` | Logo animado en hom6dtv + overlay de transición en workka2 |
| `fondo_videoteca.webm` | Fondo animado (videoteca) |

Videos de works: alojados en Cloudflare R2 (`https://pub-5dae75b9216945058a34d5462aa57b48.r2.dev/WORKS/...`).
