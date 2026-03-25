# diegotavellaweb

Portfolio de Diego Tavella — editor de video.

## Stack
- HTML + CSS + JS vanilla
- GitHub Pages
- Videos en Cloudflare R2

## Estructura

```
diegotavellaweb/
├── index.html      ← Home con logo animado
├── works.html      ← Grilla de videos
├── style.css       ← Reset y variables compartidas
├── index.css       ← Estilos de la home
├── works.css       ← Estilos de la grilla
├── main.js         ← Lógica de la home
└── works.js        ← Datos y render de los videos
```

## Agregar un video

En `works.js`, agregar un objeto al array `works`:

```js
{
  id:    "nombre-del-trabajo",
  title: "Título que aparece en pantalla",
  type:  "work",          // "reel" | "work"
  ratio: "16-9",          // "16-9" | "9-16" | "1-1"
  thumb: R2 + "/WORKS/nombre-del-trabajo/thumb.jpg",
  video: R2 + "/WORKS/nombre-del-trabajo/clip.mp4",
}
```

## Estructura en Cloudflare R2

```
/WORKS/
  reel/
    thumb.jpg
    reel.mp4
  nombre-del-trabajo/
    thumb.jpg
    clip.mp4
```

## Capacidad de la grilla
- 6 items → 3 columnas × 2 filas
- 9 items → 3 columnas × 3 filas
- 12 items → 3 columnas × 4 filas
(el reel ocupa 2 columnas automáticamente)
