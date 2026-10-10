// Configuracion de la tienda. Para crear otra tienda con este mismo codigo, solo se cambia este archivo
// (y los logos en /public). Todo lo demas toma estos valores.
export const MARCA = {
  nombre: 'Lumina Joyas',           // nombre completo
  nombreCorto: 'Lumina',            // como se nombra en frases: "Lumina te confirmará..."
  subtitulo: '',                    // texto pequeño debajo del logo grande del inicio ('' porque el logo ya dice JOYAS)
  logo: '/logo.png',                // logo horizontal para el menu, el login, los recibos y los PDF
  wordmark: '/lumina-wordmark.png', // logo completo para la portada
  logoAncho: true,                  // el logo del menu es horizontal (no cuadrado)
  wordmarkMultiplicar: true,        // el logo tiene fondo blanco: se mezcla con el fondo de la portada
  eslogan: 'Joyas que iluminan cada momento',                 // EDITAR: frase principal de la portada
  descripcionPortada: 'Piezas elegantes para cada ocasión. Envíos locales y a toda la república.', // EDITAR
  anio: 2026,
  creditos: 'Powered by Aria by BP&S - Anthropic IA',
  claveCarrito: 'lumina_cart',
  archivoPrefijo: 'lumina',
}

export const CONTACTO = {
  whatsapp: 'PENDIENTE',                  // con lada de pais, solo digitos. Ej: 5215512345678
  whatsappVisible: 'PENDIENTE',           // Ej: +52 55 1234 5678
  email: 'PENDIENTE',
  instagram: '@PENDIENTE',
  instagramUrl: 'https://www.instagram.com/PENDIENTE',
  web: 'https://PENDIENTE.netlify.app',   // la direccion final de la tienda
  clabe: 'PENDIENTE',
}

// Colores de la marca (dorado de Lumina). Se aplican como variables CSS al abrir la pagina.
export const COLORES = {
  primary: '#8A6A2F',        // color principal (botones, titulos)
  primaryLight: '#EBD9B4',
  marca: '#8A6A2F',          // color principal de la portada y acentos
  marcaOscura: '#6E531F',
  marcaSuave: '#FBF6EA',     // fondos suaves
  marcaSuave2: '#F6EEDB',
  heroFondo: '#F3E9D2',      // fondo de la foto/logo en la portada
  ctaA: '#A87C2A',           // degradado del boton "Agregar" de destacados
  ctaB: '#7A5A1E',
  franja: '#2B2418',         // franja oscura de beneficios
  fondo: '#FFFDF8',          // fondo general
}
