#!/usr/bin/env python3
"""Prepara las fotos y el SQL del catalogo a partir de una carpeta de fotos.

Estructura esperada (cada subcarpeta es una categoria; el nombre del archivo lleva el codigo y el precio):
  mis_fotos/
    ARETES/12345-$250.00.jpg
    COLLARES/20001-$480.jpg
    PULSERAS/30007-$1,099.00-2.jpg      (el sufijo despues del precio se ignora)

Uso:
  pip install pillow
  python3 scripts/preparar_catalogo.py --fotos ./mis_fotos --stock 0 [--recorte 1.0]

Genera:
  public/fotos/CODIGO.jpg          miniatura para las tarjetas (hasta 1024 px)
  public/fotos/grande/CODIGO.jpg   foto grande para la lupa (hasta 2000 px)
  catalogo.sql                     pegar en Supabase > SQL Editor > Run (crea categorias y productos)
  catalogo_revisar.txt             fotos que no se pudieron leer (sin codigo o sin precio en el nombre)

--recorte 0.86  conserva solo el 86% superior de la foto (sirve para quitar una franja con precio abajo).
Si corres el script otra vez, los precios y nombres de los productos existentes se actualizan.
"""
import argparse, os, re, sys
from multiprocessing import Pool
from PIL import Image

PAT = re.compile(r'^\s*([0-9A-Za-z]+(?:-[0-9]+)?)\s*[-_ ]*\s*\$\s*([0-9][0-9,]*(?:\.[0-9]+)?)')
EXT = ('.jpg', '.jpeg', '.png', '.webp')
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, 'public', 'fotos')

def procesar(args):
    sku, ruta, recorte = args
    try:
        im = Image.open(ruta)
        im.draft('RGB', (2000, 2000))
        im = im.convert('RGB')
        w, h = im.size
        if recorte < 1.0:
            im = im.crop((0, 0, w, int(h * recorte)))
        grande = im.copy(); grande.thumbnail((2000, 2000), Image.LANCZOS)
        grande.save(os.path.join(SALIDA, 'grande', sku + '.jpg'), quality=82, optimize=True, progressive=True)
        mini = im.copy(); mini.thumbnail((1024, 1024), Image.LANCZOS)
        mini.save(os.path.join(SALIDA, sku + '.jpg'), quality=82, optimize=True)
        return sku, None
    except Exception as e:
        return sku, str(e)

def sql_texto(t):
    return "'" + t.replace("'", "''") + "'"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fotos', required=True)
    ap.add_argument('--stock', type=int, default=0, help='Existencia inicial de cada producto nuevo')
    ap.add_argument('--recorte', type=float, default=1.0)
    a = ap.parse_args()
    os.makedirs(os.path.join(SALIDA, 'grande'), exist_ok=True)

    productos, revisar = {}, []
    for carpeta, _, archivos in os.walk(a.fotos):
        cat = os.path.basename(carpeta).strip()
        if os.path.abspath(carpeta) == os.path.abspath(a.fotos):
            cat = ''
        for f in sorted(archivos):
            if not f.lower().endswith(EXT):
                continue
            m = PAT.match(f)
            if not m or not cat:
                revisar.append(f'{os.path.join(carpeta, f)}  ->  ' + ('sin categoria (ponla dentro de una subcarpeta)' if m else 'no se encontro codigo y precio en el nombre'))
                continue
            sku, precio = m.group(1), float(m.group(2).replace(',', ''))
            if sku not in productos:
                productos[sku] = (cat.capitalize(), precio, os.path.join(carpeta, f))

    with Pool() as p:
        res = p.map(procesar, [(s, v[2], a.recorte) for s, v in productos.items()], chunksize=8)
    for sku, err in res:
        if err:
            revisar.append(f'{sku}: error con la foto ({err})'); productos.pop(sku, None)

    cats = sorted({v[0] for v in productos.values()})
    L = ['-- Catalogo generado por scripts/preparar_catalogo.py', '']
    if cats:
        vals = ', '.join(sql_texto(c) for c in cats)
        L.append(f"insert into categorias(nombre) select x from unnest(array[{vals}]) x where not exists (select 1 from categorias c where lower(c.nombre) = lower(x));")
        L.append('')
        L.append('insert into productos(nombre, precio, categoria_id, sku, stock, activo)')
        L.append('select v.nombre, v.precio, c.id, v.sku, v.stock, true')
        L.append('from (values')
        filas = [f"  ({sql_texto(cat + ' - ' + sku)}, {precio:.2f}, {sql_texto(cat)}, {sql_texto(sku)}, {a.stock})" for sku, (cat, precio, _) in sorted(productos.items())]
        L.append(',\n'.join(filas))
        L.append(') as v(nombre, precio, cat, sku, stock)')
        L.append('join categorias c on lower(c.nombre) = lower(v.cat)')
        L.append('on conflict (sku) do update set precio = excluded.precio, nombre = excluded.nombre, categoria_id = excluded.categoria_id;')
    open(os.path.join(RAIZ, 'catalogo.sql'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    open(os.path.join(RAIZ, 'catalogo_revisar.txt'), 'w', encoding='utf-8').write('\n'.join(revisar) + ('\n' if revisar else ''))
    print(f'{len(productos)} productos, {len(cats)} categorias. Fotos en public/fotos. SQL: catalogo.sql. Por revisar: {len(revisar)} (catalogo_revisar.txt)')

if __name__ == '__main__':
    main()
