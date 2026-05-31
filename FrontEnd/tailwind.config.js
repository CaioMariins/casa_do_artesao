/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        /* 60% — cores dominantes */
        base: "#fdfbf7",
        papel: "#f3f1e8",
        creme: "#f3f1e8",
        "creme-escuro": "#e4e1d0",

        /* 30% — cores secundárias */
        madeira: "#886647",
        "madeira-escura": "#6a4e32",
        argila: "#886647",
        "argila-escura": "#6a4e32",

        "azul-casa": "#388fa3",
        "azul-profundo": "#2a6f80",

        "verde-suave": "#889a60",
        "verde-profundo": "#5e6e3e",

        /* 10% — cores de destaque */
        terracota: "#d4a574",
        "terracota-forte": "#b8845a",
        "terracota-texto": "#7a4e28",
        coral: "#e8b871",

        /* texto */
        texto: "#2e2118",
        "texto-suave": "#7a6a54",
      },
      boxShadow: {
        "suave": "0 2px 8px rgba(46, 33, 24, 0.08)",
        "media": "0 4px 20px rgba(46, 33, 24, 0.12)",
      },
    },
  },
  plugins: [],
};