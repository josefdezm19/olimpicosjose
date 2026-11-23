# Herramientas de construcción

`index.html` (raíz) se genera a partir de estos archivos:

1. `parse.py` lee el PDF original (páginas 52–140 = semanas 5–12) con pdfplumber y genera `raw.json`.
   Columnas por posición x: set <60, ejercicio 60–228, carga 228–380, timing 380–540, descripción >540.
   Los enlaces de vídeo se toman de los hipervínculos de YouTube de cada página.
2. `build_data.py` limpia `raw.json` (párrafos, categorías olímpico/fuerza/core/técnica) y escribe `data.js` (`const PROGRAM=[...]`).
3. Se sustituye el marcador `/*__DATA__*/` de `template.html` por el contenido de `data.js` para obtener `index.html`:

```python
t=open('template.html').read()
open('../index.html','w').write(t.replace('/*__DATA__*/',open('data.js').read()))
```

`iphone.py` + `frame.html` generan capturas a tamaño iPhone 17 Pro (402×874 @3x) con Playwright.
La ruta del PDF en `parse.py` debe ajustarse a donde esté el archivo.
