# Configuração para Deploy - Sistema de Gestão de Estoque

## Railway.app

Para fazer deploy no Railway:

1. **Conectar ao GitHub:**
   - Faça push do código para um repositório GitHub
   - Conecte o Railway ao repositório

2. **Variáveis de Ambiente no Railway:**
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   DATABASE_URL=postgresql://user:password@host:port/database (será fornecido automaticamente)
   ALLOWED_HOSTS=your-app.railway.app,railway.app
   ```

3. **Arquivos necessários já criados:**
   - ✅ requirements.txt
   - ✅ .gitignore
   - ✅ settings.py configurado para produção

## Configuração Local

### Para desenvolvimento:
1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv .venv`
3. Ative: `source .venv/bin/activate` (Linux/Mac) ou `.venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Configure o arquivo `.env`
6. Execute migrações: `python manage.py migrate`
7. Crie superusuário: `python manage.py createsuperuser`
8. Execute o servidor: `python manage.py runserver`

### Dados de exemplo:
Execute `python criar_dados_exemplo.py` para popular o banco com dados de teste.

## Funcionalidades Implementadas

### ✅ Sistema Completo de Estoque:
- **Autenticação e Autorização**: Sistema completo de login/logout
- **Gestão de Produtos**: CRUD completo com imagens, categorias e fornecedores
- **Controle de Estoque**: Entrada, saída e ajuste de quantidades
- **Dashboard**: Estatísticas, alertas de estoque baixo, últimas movimentações
- **QR Code Scanner**: Busca rápida de produtos via código QR
- **Interface Responsiva**: Bootstrap 5 com design mobile-first
- **HTMX**: Interatividade moderna sem JavaScript complexo

### 🔧 Tecnologias Utilizadas:
- **Backend**: Django 5.2.6 + PostgreSQL (produção) / SQLite (desenvolvimento)
- **Frontend**: Bootstrap 5 + HTMX + HTML5 QR Code Scanner
- **Autenticação**: Sistema nativo do Django
- **Deploy**: Configurado para Railway.app

### 📱 Mobile-First:
- Interface otimizada para dispositivos móveis
- Scanner QR Code funciona nativamente no celular
- Navigation responsiva
- Cards e layouts adaptáveis

## Como Usar

### 1. Acessar o Sistema:
- Fazer login com suas credenciais
- Dashboard mostra resumo geral do estoque

### 2. Gerenciar Produtos:
- **Criar**: Botão "Novo Produto" no dashboard ou lista
- **Listar**: Visualizar todos os produtos com filtros e busca
- **Editar**: Atualizar informações do produto
- **Movimentar**: Registrar entradas, saídas ou ajustes

### 3. Scanner QR Code:
- Acesse "Scanner QR" no menu
- Permita acesso à câmera
- Aponte para o código QR do produto
- Sistema mostra informações e permite movimentações

### 4. Relatórios:
- **Estoque Baixo**: Produtos que precisam reposição
- **Movimentações**: Histórico completo de entradas/saídas
- **Dashboard**: Estatísticas gerais

### 5. Administração:
- Acesse `/admin/` para gestão avançada
- Criar categorias, fornecedores
- Gerenciar usuários e permissões

## Próximos Passos (Melhorias Futuras)

- [ ] Relatórios em PDF/Excel
- [ ] Gráficos de movimentação
- [ ] Múltiplos depósitos
- [ ] Código de barras
- [ ] API REST
- [ ] Notificações por email
- [ ] Histórico de preços
- [ ] Integração com fornecedores

## Suporte

Sistema desenvolvido com foco na praticidade e eficiência para gestão de estoque.
Interface simples e intuitiva, ideal para pequenas e médias empresas.
# API_Sistema_Estoque_PWA

🚀 **Sistema Completo de Gestão de Estoque com PWA**

Uma aplicação web moderna para gestão de estoque desenvolvida com Django, HTMX, Bootstrap 5 e recursos PWA (Progressive Web App) para funcionar como um aplicativo móvel nativo.

## 📱 Características Principais

### 🎯 **Funcionalidades de Gestão**
- ✅ **Gestão de Produtos** - CRUD completo com imagens e códigos de barras
- ✅ **Controle de Estoque** - Movimentações de entrada/saída em tempo real
- ✅ **Scanner QR/Código de Barras** - Busca rápida usando câmera do dispositivo
- ✅ **Categorias e Fornecedores** - Organização estruturada do inventário
- ✅ **Relatórios e Alertas** - Estoque baixo, movimentações e dashboards
- ✅ **Inventário Físico** - Conferência e ajustes de estoque

### 📲 **PWA (Progressive Web App)**
- ✅ **Instalação como App** - Funciona como aplicativo nativo no celular
- ✅ **Offline Support** - Cache inteligente para uso sem internet
- ✅ **Bottom Navigation** - Interface mobile-first otimizada
- ✅ **Push Notifications** - Alertas de estoque baixo (futuro)
- ✅ **Fast Loading** - Service Worker com cache estratégico

### 🎨 **Interface e UX**
- ✅ **Design Responsivo** - Bootstrap 5 mobile-first
- ✅ **Dark Mode Ready** - Preparado para modo escuro
- ✅ **Touch Optimized** - Botões e gestos otimizados para toque
- ✅ **HTMX Integration** - Interatividade sem JavaScript complexo

## 🛠️ **Stack Tecnológica**

### Backend
- **Django 5.2.6** - Framework web Python robusto
- **SQLite/PostgreSQL** - Banco de dados flexível
- **Python-decouple** - Gerenciamento de configurações
- **Pillow** - Processamento de imagens

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **HTMX** - Interatividade moderna sem SPA complexity
- **Bootstrap Icons** - Ícones consistentes
- **HTML5 APIs** - Camera, Storage, Notifications

### PWA
- **Web App Manifest** - Metadados de instalação
- **Service Worker** - Cache offline e sync
- **Cache Strategies** - Cache-first para estáticos, network-first para dados

## 🚀 **Instalação e Configuração**

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### 1️⃣ **Clone do Repositório**
```bash
git clone https://github.com/hendelsantos/API_Sistema_Estoque_PWA.git
cd API_Sistema_Estoque_PWA
```

### 2️⃣ **Ambiente Virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3️⃣ **Dependências**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Configuração**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite as configurações necessárias
nano .env
```

### 5️⃣ **Banco de Dados**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ **Execução**
```bash
python manage.py runserver 0.0.0.0:8000
```

## 📱 **Como Usar como PWA**

### **Android**
1. Abra a aplicação no Chrome
2. Toque no botão "Instalar App" que aparece
3. OU: Menu → "Adicionar à tela inicial"

### **iOS**
1. Abra a aplicação no Safari
2. Toque em "Compartilhar" 
3. Selecione "Adicionar à Tela de Início"

### **Desktop**
1. Abra no Chrome/Edge
2. Clique no ícone de instalação na barra de endereços
3. OU: Use o botão "Instalar App"

## 🔧 **Configurações de Produção**

### **Variáveis de Ambiente**
```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=seudominio.com,app.railway.app
```

### **Deploy Railway/Heroku**
```bash
# Railway
railway login
railway init
railway add
railway deploy

# Heroku
heroku create your-app-name
git push heroku main
```

## 📊 **Funcionalidades em Destaque**

### **Dashboard**
- Visão geral do estoque
- Produtos com estoque baixo
- Movimentações recentes
- Estatísticas em tempo real

### **Scanner QR**
- Busca instantânea por código de barras
- Interface touch-friendly
- Acesso via bottom navigation
- Shortcut na tela inicial

### **Gestão de Produtos**
- Upload de imagens
- Geração automática de códigos
- Controle de estoque mínimo
- Categorização inteligente

### **Relatórios**
- Estoque baixo com alertas
- Movimentações por período
- Produtos mais movimentados
- Exportação de dados

## 🎨 **Screenshots**

### Mobile (PWA)
- Dashboard responsivo
- Bottom navigation
- Scanner QR integrado
- Interface touch-optimized

### Desktop
- Sidebar navigation
- Dashboards completos
- Formulários otimizados
- Relatórios detalhados

## 🤝 **Contribuições**

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 **Autor**

**Hendel Santos**
- GitHub: [@hendelsantos](https://github.com/hendelsantos)
- LinkedIn: [Hendel Santos](https://linkedin.com/in/hendelsantos)

## 🙏 **Agradecimentos**

- Django Community pela excelente documentação
- Bootstrap Team pelo framework responsivo
- HTMX pela simplicidade e poder
- Contribuidores open-source

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐
