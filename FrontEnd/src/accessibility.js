/* =========================================================
   ACESSIBILIDADE — Casa do Artesão de Niterói
   Funcionalidades:
     1. Menu sanduíche (mobile)
     2. Aumentar / diminuir fonte
     3. Alto contraste
     4. Widget VLibras (Libras)
   ========================================================= */

// ── 1. MENU SANDUÍCHE ────────────────────────────────────────

function initMenuSanduiche() {
  const btnMenu = document.querySelector("#btnMenu");
  const menuMobile = document.querySelector("#menuMobile");
  const overlay = document.querySelector("#menuOverlay");
  const linksMenu = document.querySelectorAll("#menuMobile a");

  if (!btnMenu || !menuMobile) return;

  function abrirMenu() {
    menuMobile.classList.remove("menu-fechado");
    menuMobile.classList.add("menu-aberto");
    btnMenu.setAttribute("aria-expanded", "true");
    btnMenu.setAttribute("aria-label", "Fechar menu");
    overlay?.classList.remove("hidden");
    document.body.style.overflow = "hidden";
    // Foca o primeiro link do menu
    const primeiroLink = menuMobile.querySelector("a");
    primeiroLink?.focus();
  }

  function fecharMenu() {
    menuMobile.classList.remove("menu-aberto");
    menuMobile.classList.add("menu-fechado");
    btnMenu.setAttribute("aria-expanded", "false");
    btnMenu.setAttribute("aria-label", "Abrir menu");
    overlay?.classList.add("hidden");
    document.body.style.overflow = "";
    btnMenu.focus();
  }

  btnMenu.addEventListener("click", () => {
    const estaAberto = btnMenu.getAttribute("aria-expanded") === "true";
    estaAberto ? fecharMenu() : abrirMenu();
  });

  overlay?.addEventListener("click", fecharMenu);

  linksMenu.forEach((link) => {
    link.addEventListener("click", fecharMenu);
  });

  // Fechar com ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && btnMenu.getAttribute("aria-expanded") === "true") {
      fecharMenu();
    }
  });

  // Trap focus dentro do menu aberto
  menuMobile.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return;
    const focaveis = menuMobile.querySelectorAll(
      'a, button, [tabindex]:not([tabindex="-1"])'
    );
    const primeiro = focaveis[0];
    const ultimo = focaveis[focaveis.length - 1];
    if (e.shiftKey && document.activeElement === primeiro) {
      e.preventDefault();
      ultimo.focus();
    } else if (!e.shiftKey && document.activeElement === ultimo) {
      e.preventDefault();
      primeiro.focus();
    }
  });
}

// ── 2. TAMANHO DE FONTE ──────────────────────────────────────

const FONT_KEY = "casaArtesao_fontSize";
const FONT_PASSOS = [100, 112, 125]; // % do root (normal, médio, grande)
let fontePasso = parseInt(localStorage.getItem(FONT_KEY) ?? "0");

function aplicarFonte() {
  document.documentElement.style.fontSize = FONT_PASSOS[fontePasso] + "%";
  // Atualiza estado visual dos botões
  const btns = document.querySelectorAll("[data-acao-fonte]");
  btns.forEach((btn) => {
    const acao = btn.dataset.acaoFonte;
    if (acao === "aumentar") {
      btn.disabled = fontePasso === FONT_PASSOS.length - 1;
      btn.setAttribute("aria-disabled", btn.disabled);
    }
    if (acao === "diminuir") {
      btn.disabled = fontePasso === 0;
      btn.setAttribute("aria-disabled", btn.disabled);
    }
  });
}

function initFonte() {
  const btns = document.querySelectorAll("[data-acao-fonte]");
  if (!btns.length) return;

  aplicarFonte();

  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const acao = btn.dataset.acaoFonte;
      if (acao === "aumentar" && fontePasso < FONT_PASSOS.length - 1) {
        fontePasso++;
      } else if (acao === "diminuir" && fontePasso > 0) {
        fontePasso--;
      }
      localStorage.setItem(FONT_KEY, fontePasso);
      aplicarFonte();
      // Anuncia mudança para leitores de tela
      anunciar(
        `Tamanho do texto: ${["normal", "médio", "grande"][fontePasso]}`
      );
    });
  });
}

// ── 3. ALTO CONTRASTE ────────────────────────────────────────

const CONTRASTE_KEY = "casaArtesao_altoContraste";

function initAltoContraste() {
  const btn = document.querySelector("#btnContraste");
  if (!btn) return;

  // Restaura preferência salva
  const salvo = localStorage.getItem(CONTRASTE_KEY) === "true";
  if (salvo) document.documentElement.classList.add("alto-contraste");
  atualizarBtnContraste(btn);

  btn.addEventListener("click", () => {
    const ativo = document.documentElement.classList.toggle("alto-contraste");
    localStorage.setItem(CONTRASTE_KEY, ativo);
    atualizarBtnContraste(btn);
    anunciar(ativo ? "Alto contraste ativado" : "Alto contraste desativado");
  });
}

function atualizarBtnContraste(btn) {
  const ativo = document.documentElement.classList.contains("alto-contraste");
  btn.setAttribute("aria-pressed", ativo);
  btn.title = ativo ? "Desativar alto contraste" : "Ativar alto contraste";
}

// ── 4. VLIBRAS ───────────────────────────────────────────────

function initVLibras() {
  // Só carrega se ainda não foi adicionado
  if (document.querySelector("[vw]")) return;

  const wrapper = document.createElement("div");
  wrapper.setAttribute("vw", "");
  wrapper.className = "enabled";
  wrapper.innerHTML = `
    <div vw-access-button class="active"></div>
    <div vw-plugin-wrapper>
      <div class="vw-plugin-top-wrapper"></div>
    </div>
  `;
  document.body.appendChild(wrapper);

  const script = document.createElement("script");
  script.src = "https://vlibras.gov.br/app/vlibras-plugin.js";
  script.onload = () => {
    new window.VLibras.Widget("https://vlibras.gov.br/app");
  };
  document.body.appendChild(script);
}

// ── UTILITÁRIO: LIVE REGION (ANÚNCIO PARA LEITORES DE TELA) ──

let liveRegion;

function anunciar(mensagem) {
  if (!liveRegion) {
    liveRegion = document.createElement("div");
    liveRegion.setAttribute("aria-live", "polite");
    liveRegion.setAttribute("aria-atomic", "true");
    liveRegion.className = "sr-only";
    document.body.appendChild(liveRegion);
  }
  liveRegion.textContent = "";
  requestAnimationFrame(() => {
    liveRegion.textContent = mensagem;
  });
}

// ── 5. BOTÃO VOLTAR AO TOPO ──────────────────────────────────

function initBtnTopo() {
  const btn = document.querySelector("#btnTopo");
  if (!btn) return;

  // Mostra o botão após rolar 400px
  const observer = new IntersectionObserver(
    ([entry]) => {
      btn.classList.toggle("visivel", !entry.isIntersecting);
    },
    { threshold: 0 }
  );

  // Observa o hero (primeira section); quando sair da tela, botão aparece
  const hero = document.querySelector("#inicio");
  if (hero) observer.observe(hero);

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    // Devolve foco ao topo para leitores de tela
    const primeiroFocavel = document.querySelector("a, button, [tabindex]");
    primeiroFocavel?.focus({ preventScroll: true });
  });
}

// ── INICIALIZAÇÃO ────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  initMenuSanduiche();
  initFonte();
  initAltoContraste();
  initVLibras();
  initBtnTopo();
});