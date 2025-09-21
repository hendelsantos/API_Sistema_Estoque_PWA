# 🚀 Deploy no Railway - Sistema de Gestão de Estoque PWA

## 📋 Pré-requisitos

1. **Conta no Railway**: Crie sua conta em [railway.app](https://railway.app)
2. **GitHub**: Tenha o projeto pushado no GitHub
3. **Arquivos configurados**: ✅ Já preparados neste projeto

## 🛠️ Arquivos Preparados para Deploy

### ✅ **Configurações já incluídas:**
- `railway.json` - Configuração específica do Railway
- `Procfile` - Comandos de inicialização
- `requirements.txt` - Dependências com Gunicorn e Whitenoise
- `settings.py` - Configurado para produção com Whitenoise
- `.env.example` - Template de variáveis de ambiente

## 🚀 **Passo a Passo para Deploy**

### 1️⃣ **Conectar ao Railway**
```bash
# Instalar Railway CLI (opcional)
npm install -g @railway/cli

# Ou usar a interface web diretamente
```

### 2️⃣ **Criar Projeto no Railway**
1. Acesse [railway.app](https://railway.app)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Escolha o repositório `API_Sistema_Estoque_PWA`

### 3️⃣ **Configurar Variáveis de Ambiente**
No Railway Dashboard, vá em **Variables** e adicione:

```env
SECRET_KEY=sua-chave-super-secreta-de-producao-aqui-com-50-caracteres
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

**⚠️ Importante**: O Railway fornece automaticamente:
- `DATABASE_URL` (PostgreSQL)
- `PORT` (porta do servidor)

### 4️⃣ **Configurar PostgreSQL**
1. No Railway Dashboard, clique em "+ Add Service"
2. Selecione "PostgreSQL"
3. O `DATABASE_URL` será configurado automaticamente

### 5️⃣ **Deploy Automático**
1. O Railway detecta automaticamente o `railway.json`
2. Instala dependências do `requirements.txt`
3. Executa migrações e coleta arquivos estáticos
4. Inicia o servidor com Gunicorn

## 🔧 **Comandos Executados Automaticamente**

```bash
# Build
pip install -r requirements.txt

# Deploy
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn gestao_estoque.wsgi:application
```

## 🌍 **Após o Deploy**

### ✅ **Verificações**
1. **URL gerada**: `https://seu-projeto.railway.app`
2. **SSL automático**: ✅ HTTPS configurado
3. **Database**: PostgreSQL provisionado

### 🔐 **Criar Superusuário**
Execute no Railway Console ou localmente conectado ao DB de produção:
```bash
python manage.py createsuperuser
```

### 📊 **Popular com Dados (opcional)**
```bash
python manage.py shell
# Execute o script de dados exemplo se necessário
```

## 📱 **Testar PWA em Produção**

1. **Acesse a URL de produção**
2. **Teste a instalação**: Botão "Instalar App" deve aparecer
3. **Verifique offline**: Service Worker deve cachear recursos
4. **Mobile friendly**: Bottom navigation deve funcionar

## 🔄 **Updates Automáticos**

Cada push para a branch `main` no GitHub dispara automaticamente:
1. ✅ Build do projeto
2. ✅ Deploy automático
3. ✅ Execução de migrações
4. ✅ Coleta de arquivos estáticos

## 🛡️ **Segurança em Produção**

### ✅ **Configurações já ativadas:**
- HTTPS obrigatório
- Headers de segurança
- Cookies seguros
- HSTS habilitado
- XSS Protection
- Content Type Sniffing protection

## 💰 **Custos Railway**

- **Hobby Plan**: $5/mês (500h de execução)
- **PostgreSQL**: $5/mês
- **Bandwidth**: 100GB incluído

## 🔧 **Comandos úteis Railway CLI**

```bash
# Login
railway login

# Conectar ao projeto
railway link

# Ver logs
railway logs

# Abrir console
railway shell

# Deploy manual
railway up
```

## 🆘 **Troubleshooting**

### ❌ **Problemas comuns:**

**1. Erro de migração:**
```bash
# No Railway Console
python manage.py migrate --run-syncdb
```

**2. Arquivos estáticos não carregam:**
```bash
# Verificar Whitenoise
python manage.py collectstatic --noinput
```

**3. Erro de ALLOWED_HOSTS:**
```env
# Adicionar nas variáveis
ALLOWED_HOSTS=*.railway.app,seudominio.com
```

## 📈 **Monitoramento**

### Railway Dashboard mostra:
- ✅ CPU e Memory usage
- ✅ Database connections
- ✅ Response times
- ✅ Error rates
- ✅ Deployment history

## 🎯 **Próximos Passos Após Deploy**

1. **Custom Domain** (opcional): Configurar domínio próprio
2. **Backup Strategy**: Configurar backups do PostgreSQL  
3. **Monitoring**: Configurar alertas de performance
4. **CDN**: Railway Edge para arquivos estáticos globais

---

## 🏁 **Resumo Final**

✅ **Arquivos configurados**: Todos prontos para deploy
✅ **Settings otimizados**: Produção + desenvolvimento
✅ **Segurança**: Headers e SSL configurados
✅ **PWA ready**: Service Worker e manifest funcionais
✅ **Auto-deploy**: Push to deploy configurado

**🚀 Pronto para deploy no Railway!**
