// CSS importado no HTML para evitar FOUC (Flash of Unstyled Content)
// Leaflet será carregado sob demanda quando o mapa for aberto

// Função para lazy load do Leaflet
async function loadLeaflet() {
  const L = (await import("leaflet")).default;
  await import("leaflet/dist/leaflet.css");
  return L;
}

const feiras = [
  {
    nome: "Feira da Orla de São Francisco",
    local: "Orla de São Francisco",
    dias: "2º domingo do mês",
    horario: "10h às 19h",
    bairro: "São Francisco",
    coordenadas: [-22.9162, -43.0947],
  },
  {
    nome: "Feira da Praça César Tinoco",
    local: "Praça César Tinoco, Ingá",
    dias: "1º e 3º sábado do mês",
    horario: "09h às 15h",
    bairro: "Ingá",
    coordenadas: [-22.9042, -43.1262],
  },
  {
    nome: "Feira da Praça Zumbi dos Palmares",
    local: "Praça Zumbi dos Palmares, São Domingos",
    dias: "Toda terça-feira",
    horario: "12h às 20h",
    bairro: "São Domingos",
    coordenadas: [-22.9008, -43.1327],
  },
  {
    nome: "Exposição de Artesanato do Centro Eco Cultural",
    local: "Centro Eco Cultural, Piratininga",
    dias: "Domingos",
    horario: "09h às 17h",
    bairro: "Piratininga",
    coordenadas: [-22.9546, -43.0481],
  },
  {
    nome: "Feira da Praça do Rink",
    local: "Rua Dr. Borman, Centro",
    dias: "1ª e 3ª quinta-feira do mês",
    horario: "09h às 17h",
    bairro: "Centro",
    coordenadas: [-22.8948, -43.1234],
  },
  {
    nome: "Feira da Praça do Expedicionário",
    local: "Av. Quintino Bocaiuva, São Francisco",
    dias: "Todo sábado",
    horario: "15h às 21h",
    bairro: "São Francisco",
    coordenadas: [-22.9174, -43.0965],
  },
  {
    nome: "Feira da Praça Dom Navarro",
    local: "Av. Ary Parreiras, em frente à Igreja São Judas Tadeu",
    dias: "1º e 3º domingo do mês",
    horario: "09h às 15h",
    bairro: "Icaraí",
    coordenadas: [-22.9088, -43.1039],
  },
  {
    nome: "Feira do Horto Fonseca",
    local: "Alameda São Boaventura, Fonseca",
    dias: "Sábados, domingos e feriados nacionais",
    horario: "09h às 18h",
    bairro: "Fonseca",
    coordenadas: [-22.8832, -43.0994],
  },
  {
    nome: "Feira do Campo de São Bento",
    local: "Campo de São Bento, Icaraí",
    dias: "Sábados, domingos e feriados nacionais",
    horario: "09h às 15h",
    bairro: "Icaraí",
    coordenadas: [-22.9046, -43.1107],
  },
  {
    nome: "Feira da Fibromialgia",
    local: "Av. Visconde do Rio Branco, entre o Bay Market e o McDonalds",
    dias: "2ª quarta-feira do mês",
    horario: "09h às 18h",
    bairro: "Centro",
    coordenadas: [-22.8935, -43.1238],
  },
];

const listaFeiras = document.querySelector("#listaFeiras");

if (listaFeiras) {
  feiras.forEach((feira) => {
    const card = document.createElement("article");

    card.className = "card-artesanal rounded-3xl p-6";

    card.innerHTML = `
      <div class="flex items-start justify-between gap-4">
        <div>
          <span class="badge-artesanal inline-block rounded-full px-3 py-1 text-xs font-extrabold">
            ${feira.bairro}
          </span>

          <h3 class="mt-4 text-xl font-extrabold text-madeira-escura">
            ${feira.nome}
          </h3>
        </div>

        <span class="text-3xl" aria-hidden="true">📍</span>
      </div>

      <div class="mt-4 space-y-2 text-texto-suave">
        <p><strong>Local:</strong> ${feira.local}</p>
        <p><strong>Dias:</strong> ${feira.dias}</p>
        <p><strong>Horário:</strong> ${feira.horario}</p>
      </div>

      <a
        href="https://www.google.com/maps?q=${feira.coordenadas[0]},${feira.coordenadas[1]}"
        target="_blank"
        rel="noopener noreferrer"
        class="btn-secundario mt-5 inline-flex rounded-full px-5 py-2.5 text-sm font-extrabold"
      >
        Como chegar
      </a>
    `;

    listaFeiras.appendChild(card);
  });
}

const modalMapa = document.querySelector("#modalMapa");
const abrirMapa = document.querySelector("#abrirMapa");
const abrirMapaSecundario = document.querySelector("#abrirMapaSecundario");
const fecharMapa = document.querySelector("#fecharMapa");

const modalGaleria = document.querySelector("#modalGaleria");
const abrirGaleria = document.querySelector("#abrirGaleria");
const fecharGaleria = document.querySelector("#fecharGaleria");
const gridGaleria = document.querySelector("#gridGaleria");

const abrirGaleriaBtn = document.querySelector("#abrirGaleriaBtn");

const fotosGaleria = [
  { src: "/img/feira-01.jpg", alt: "Banca com peças artesanais expostas em feira" },
  { src: "/img/feira-02.webp", alt: "Detalhes de peças artesanais" },
  { src: "/img/feira-03.webp", alt: "Produtos artesanais em exposição" },
  { src: "/img/feira-04.webp", alt: "Peças artesanais coloridas" },
  { src: "/img/feira-05.webp", alt: "Banca de artesanato em feira" },
  { src: "/img/feira-06.webp", alt: "Produção artesanal feita à mão" },
  { src: "/img/feira-07.webp", alt: "Produtos artesanais com identidade local" },
  { src: "/img/IMG_9372.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9373.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9375.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9377.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9380.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9381.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9382.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9383.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9389.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9390.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9392.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9393.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9395.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9396.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9398.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9401.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9402.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9403.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9404.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9408.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9409.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9411.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9416.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9419.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9421.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9424.jpg", alt: "Imagem da galeria de evento artesanal" },
  { src: "/img/IMG_9426.jpg", alt: "Imagem da galeria de evento artesanal" },
];

const fotosGaleriaPrincipal = fotosGaleria.slice(0, 7);

let mapaCriado = false;
let map;

function abrirModalMapa() {
  if (!modalMapa) return;

  modalMapa.classList.remove("hidden");
  bloquearScroll();

  if (!mapaCriado) {
    criarMapa();
    mapaCriado = true;
  } else {
    map.invalidateSize();
  }
}

if (abrirMapa) {
  abrirMapa.addEventListener("click", abrirModalMapa);
}

if (abrirMapaSecundario) {
  abrirMapaSecundario.addEventListener("click", abrirModalMapa);
}

if (fecharMapa) {
  fecharMapa.addEventListener("click", () => {
    modalMapa.classList.add("hidden");
    liberarScroll();
  });
}

if (modalMapa) {
  modalMapa.addEventListener("click", (event) => {
    if (event.target === modalMapa) {
      modalMapa.classList.add("hidden");
      liberarScroll();
    }
  });
}

function bloquearScroll() {
  document.body.style.overflow = "hidden";
}

function liberarScroll() {
  document.body.style.overflow = "";
}

function abrirModalGaleria() {
  if (!modalGaleria) return;
  modalGaleria.classList.remove("hidden");
  bloquearScroll();
}

function fecharModalGaleria() {
  if (!modalGaleria) return;
  modalGaleria.classList.add("hidden");
  liberarScroll();
}

if (gridGaleria) {
  // Variável para rastrear foto atual no modal
  let fotoAtualIndex = 0;

  function atualizarGaleria(index) {
    fotoAtualIndex = (index + fotosGaleria.length) % fotosGaleria.length;
    document.getElementById("fotoGrande").src = fotosGaleria[fotoAtualIndex].src;
    document.getElementById("fotoAtual").textContent = fotoAtualIndex + 1;

    // Atualizar thumbnails ativas
    document.querySelectorAll("#thumbnails button").forEach((thumb, i) => {
      thumb.classList.toggle("ring-2", i === fotoAtualIndex);
      thumb.classList.toggle("ring-terracota", i === fotoAtualIndex);
    });
  }

  fotosGaleriaPrincipal.forEach((foto, index) => {
    const card = document.createElement("article");
    card.className = "overflow-hidden rounded-3xl border border-madeira/20 bg-base shadow-sm";
    card.innerHTML = `
      <img src="${foto.src}" alt="${foto.alt}" loading="lazy"
        class="h-48 w-full object-cover transition duration-300 hover:scale-105 cursor-pointer" />
      <div class="p-4">
        <p class="text-sm font-semibold text-madeira-escura">${foto.alt}</p>
      </div>
    `;
    card.addEventListener("click", () => {
      abrirModalGaleria();
      atualizarGaleria(index);
    });
    gridGaleria.appendChild(card);
  });

  // Criar thumbnails no modal
  const thumbnails = document.getElementById("thumbnails");
  fotosGaleria.forEach((foto, index) => {
    const thumb = document.createElement("button");
    thumb.type = "button";
    thumb.className = "w-16 h-16 rounded-lg overflow-hidden border-2 border-white/30 hover:border-white/60 transition";
    if (index === 0) thumb.classList.add("ring-2", "ring-terracota");
    thumb.innerHTML = `<img src="${foto.src}" alt="Miniatura ${index + 1}" class="w-full h-full object-cover">`;
    thumb.addEventListener("click", () => atualizarGaleria(index));
    thumbnails.appendChild(thumb);
  });

  document.getElementById("totalFotos").textContent = fotosGaleria.length;
  atualizarGaleria(0);

  // Navegação com botões
  const fotoPrev = document.getElementById("fotoPrev");
  const fotoNext = document.getElementById("fotoNext");

  if (fotoPrev) {
    fotoPrev.addEventListener("click", () => atualizarGaleria(fotoAtualIndex - 1));
  }

  if (fotoNext) {
    fotoNext.addEventListener("click", () => atualizarGaleria(fotoAtualIndex + 1));
  }

  // Navegar com teclado
  document.addEventListener("keydown", (e) => {
    if (!modalGaleria.classList.contains("hidden")) {
      if (e.key === "ArrowLeft") atualizarGaleria(fotoAtualIndex - 1);
      if (e.key === "ArrowRight") atualizarGaleria(fotoAtualIndex + 1);
    }
  });
}

if (abrirGaleria) {
  abrirGaleria.addEventListener("click", abrirModalGaleria);
}

if (abrirGaleriaBtn) {
  abrirGaleriaBtn.addEventListener("click", abrirModalGaleria);
}

if (abrirGaleriaSecundaria) {
  abrirGaleriaSecundaria.addEventListener("click", abrirModalGaleria);
}

if (abrirGaleria) {
  abrirGaleria.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      abrirModalGaleria();
    }
  });
}

if (fecharGaleria) {
  fecharGaleria.addEventListener("click", fecharModalGaleria);
}

if (modalGaleria) {
  modalGaleria.addEventListener("click", (event) => {
    if (event.target === modalGaleria) {
      fecharModalGaleria();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!modalGaleria.classList.contains("hidden") && event.key === "Escape") {
      fecharModalGaleria();
    }
  });
}

async function criarMapa() {
  const L = await loadLeaflet();

  map = L.map("map").setView([-22.9068, -43.1109], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
  }).addTo(map);

  // Configurar ícone padrão com lazy load
  const markerIcon = await import("leaflet/dist/images/marker-icon.png");
  const markerShadow = await import("leaflet/dist/images/marker-shadow.png");

  const defaultIcon = L.icon({
    iconUrl: markerIcon.default,
    shadowUrl: markerShadow.default,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
  });

  L.Marker.prototype.options.icon = defaultIcon;

  feiras.forEach((feira) => {
    L.marker(feira.coordenadas).addTo(map).bindPopup(`
      <strong>${feira.nome}</strong><br>
      ${feira.local}<br>
      ${feira.dias}<br>
      ${feira.horario}<br><br>
      <a
        href="https://www.google.com/maps?q=${feira.coordenadas[0]},${feira.coordenadas[1]}"
        target="_blank"
        rel="noopener noreferrer"
      >
        Abrir no Google Maps
      </a>
    `);
  });
}