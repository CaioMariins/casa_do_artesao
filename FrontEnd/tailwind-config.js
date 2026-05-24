
tailwind.config = {
  // Define que o modo de alto contraste responderá pela classe '.alto-contraste'
  darkMode: ['class', '.alto-contraste'], 
  theme: {
    extend: {
      colors: {
        // Cores padrão do Modo Claro
        customFundo: '#f8fafc',
        customTexto: '#1e293b',
        
        // Cores do Modo Alto Contraste 
        acFundo: '#000000',     // Preto Puro
        acTexto: '#ffffff',     // Branco Puro
        acDestaque: '#ffff00',   // Amarelo para botões/links
      }
    }
  }
};