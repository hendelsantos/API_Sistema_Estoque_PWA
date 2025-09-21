# PWA Configuration - EstoqueApp

## 📱 Progressive Web App (PWA) Setup

Esta aplicação foi configurada como uma PWA (Progressive Web App) para funcionar como um aplicativo móvel nativo no navegador.

### ✨ Recursos PWA Implementados

1. **Web App Manifest** (`/static/manifest.json`)
   - Metadados da aplicação
   - Ícones em múltiplos tamanhos
   - Configuração de exibição
   - Shortcuts de ações rápidas

2. **Service Worker** (`/static/sw.js`)
   - Cache offline
   - Estratégia cache-first para recursos estáticos
   - Background sync para dados
   - Suporte a push notifications

3. **Design Mobile-First**
   - Layout responsivo com Bootstrap 5
   - Bottom navigation para mobile
   - Touch gestures otimizados
   - Viewport configurado para PWA

### 📱 Como Usar

#### Instalação no Mobile (Android/iOS)
1. Abra a aplicação no navegador
2. Toque no botão "Instalar App" que aparece
3. OU use o menu do navegador > "Adicionar à tela inicial"

#### Instalação no Desktop
1. Abra a aplicação no Chrome/Edge
2. Clique no ícone de instalação na barra de endereços
3. OU use o botão "Instalar App" que aparece

### 🎯 Funcionalidades Mobile

- **Bottom Navigation**: Navegação otimizada para toque
- **QR Scanner**: Acesso rápido via shortcut
- **Offline Support**: Cache de recursos essenciais
- **Touch Gestures**: Swipe para esconder barra de endereços
- **Native Feel**: Comportamento similar a app nativo

### 🔧 Arquivos de Configuração

```
static/
├── manifest.json          # Metadados da PWA
├── sw.js                 # Service Worker
├── browserconfig.xml     # Configuração Windows
├── icons/               # Ícones da aplicação
│   ├── icon.svg         # Ícone principal (SVG)
│   └── icon-*x*.html    # Placeholders para PNGs
└── generate_icons.py    # Script para gerar ícones
```

### 📋 Meta Tags PWA no base.html

```html
<!-- PWA Meta Tags -->
<meta name="theme-color" content="#0d6efd">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="EstoqueApp">
<link rel="manifest" href="/static/manifest.json">
```

### 🎨 Customização

#### Cores do Tema
- **Primary**: #0d6efd (Bootstrap Blue)
- **Background**: #f8f9fa (Light Gray)
- **Accent**: #198754 (Success Green)

#### Ícones
Para substituir os ícones placeholder:
1. Crie PNGs nos tamanhos: 16x16, 32x32, 48x48, 72x72, 96x96, 128x128, 144x144, 152x152, 180x180, 192x192, 384x384, 512x512
2. Salve em `/static/icons/`
3. Atualize o manifest.json se necessário

### 🚀 Deploy e Produção

#### Certificado SSL
PWAs exigem HTTPS em produção. Configure SSL no seu servidor.

#### Cache Strategy
O Service Worker usa cache-first para:
- CSS/JS estáticos
- Imagens
- Fontes

Network-first para:
- Dados da API
- HTML dinâmico

#### Performance
- Recursos essenciais são pré-carregados
- Lazy loading para recursos secundários
- Minificação recomendada para produção

### 📊 Auditoria PWA

Use o Lighthouse (Chrome DevTools) para auditar:
- Performance
- Accessibility
- Best Practices
- SEO
- PWA Score

### 🔄 Atualizações

O Service Worker detecta automaticamente atualizações e solicita confirmação do usuário para recarregar.

### 🛠️ Desenvolvimento

Para desenvolvimento local:
```bash
python manage.py runserver 0.0.0.0:8000
```

Para testar PWA em dispositivos móveis na rede local, use o IP do computador.

### 📱 Shortcuts Disponíveis

1. **Scanner QR**: Acesso direto ao scanner
2. **Produtos**: Lista de produtos
3. **Dashboard**: Tela principal
4. **Adicionar Produto**: Criação rápida

### 🔐 Segurança

- CSRF tokens configurados para HTMX
- Headers de segurança recomendados
- Service Worker com escopo limitado

### 📞 Suporte

Para dúvidas sobre a configuração PWA, consulte:
- [MDN PWA Guide](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Google PWA Checklist](https://web.dev/pwa-checklist/)
