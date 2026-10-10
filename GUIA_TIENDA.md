# Guia para publicar la tienda (Lumina Joyas)

Esta tienda es una copia del mismo codigo que Lessa Joyeria, con su propia marca y su propia base de datos.
Se necesitan tres cuentas gratuitas: GitHub (guarda el codigo), Supabase (guarda productos, pedidos e inventario) y Netlify (publica la pagina).

## Datos que hay que completar antes

Archivo `src/config.js`:
- `CONTACTO.whatsapp` (con lada de pais, solo digitos, ej. 5215512345678) y `whatsappVisible` (ej. +52 55 1234 5678)
- `CONTACTO.email`, `instagram`, `instagramUrl`, `clabe`
- `CONTACTO.web`: la direccion final de la tienda (se conoce al publicar en Netlify; se puede corregir despues)
- `MARCA.eslogan` y `MARCA.descripcionPortada`: la frase de la portada (hay una de ejemplo)
- Los textos de envios y plazos (envios locales y a toda la republica, 15 y 30 dias, rangos de paqueteria) estan en `src/lib/store.js` y `src/pages/Landing.jsx`; ajustarlos si no aplican.

## Paso 1. GitHub

1. Crear un repositorio nuevo y privado, por ejemplo `lumina-joyas`.
2. Subir esta carpeta completa (`git init`, `git add .`, `git commit`, `git remote add origin ...`, `git push`).

## Paso 2. Supabase (base de datos)

1. En supabase.com crear un proyecto nuevo. Guardar la contraseña de la base de datos.
2. Generar el SQL de instalacion, con el prefijo de los folios, la contraseña del panel y las categorias:

```
python3 scripts/generar_instalar.py --prefijo LUMINA --clave "LaContraseñaDelPanel" --categorias "Aretes,Collares,Pulseras,Anillos,Dijes" --salida instalar.sql
```

3. En Supabase abrir SQL Editor, pegar TODO el contenido de `instalar.sql` y pulsar Run. Se corre una sola vez.
4. En Project Settings > API copiar la **Project URL** y la clave **anon public**.

La contraseña del panel que se eligio en el paso 2 es la que se usa en el boton "Ingresar" de la tienda. Conviene guardarla en un lugar seguro.

## Paso 3. Netlify (publicar)

1. En netlify.com: Add new site > Import from Git > elegir el repositorio.
2. Build command `npm run build`, publish directory `dist` (ya vienen en `netlify.toml`).
3. En Site configuration > Environment variables agregar:
   - `VITE_SUPABASE_URL` = la Project URL de Supabase
   - `VITE_SUPABASE_KEY` = la clave anon public
4. Deploy. La direccion que da Netlify se pone en `CONTACTO.web` de `src/config.js`.

## Paso 4. Cargar el catalogo

Las fotos se ordenan en una carpeta, una subcarpeta por categoria, y el nombre de cada foto lleva el codigo y el precio:

```
mis_fotos/ARETES/12345-$250.00.jpg
mis_fotos/COLLARES/20001-$480.jpg
```

Luego:

```
pip install pillow
python3 scripts/preparar_catalogo.py --fotos ./mis_fotos --stock 0
```

Esto crea las fotos chicas y grandes en `public/fotos`, un `catalogo.sql` y un `catalogo_revisar.txt` con las fotos que no se pudieron leer.
Pegar `catalogo.sql` en el SQL Editor de Supabase (Run), y subir los cambios a GitHub (`git add . && git commit && git push`): Netlify publica solo.
Para agregar productos nuevos mas adelante se repite este paso con las fotos nuevas, o se usa "Nuevo producto" en el panel.

## Uso diario

- "Ingresar" (arriba a la derecha) con la contraseña del panel: activa el modo edicion (inventario con + y -, destacados con la estrella, ocultar y borrar productos).
- Panel: pedidos pendientes, pedidos a proveedor, inventario actual, historial y registro de ventas manuales, y reportes.

## Importante

- Las fotos y el catalogo de Lessa Joyeria NO vienen incluidos: son de otra tienda.
- Nunca subir a GitHub la contraseña de la base de datos de Supabase.
