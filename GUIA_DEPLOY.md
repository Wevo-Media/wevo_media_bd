# Guia de Deploy - Wevo Media CRM

## Opções de Hospedagem Gratuita

### Melhor Opção Recomendada: Railway + Supabase

**Por que essa combinação?**
- Railway oferece 500 horas/mês grátis (suficiente para manter online 24/7)
- Deploy automático do Django
- Fácil configuração
- Supabase oferece PostgreSQL grátis com 500MB

---

## OPÇÃO 1: Railway + Supabase (RECOMENDADO) ⭐

### Passo 1: Preparar o Projeto

#### 1.1 Criar arquivo `requirements.txt` atualizado
```bash
pip freeze > requirements.txt
```

Ou crie manualmente:
```txt 
Django==5.1.3
psycopg2-binary==2.9.9
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
```

#### 1.2 Criar arquivo `runtime.txt`
```txt
python-3.12.0
```

#### 1.3 Criar arquivo `Procfile` (Railway usa isso)
```
web: gunicorn wevo_media_project.wsgi --log-file -
```

#### 1.4 Atualizar `settings.py`

Adicione ao final do arquivo:

```python
import os
from decouple import config

# SECURITY
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
SECRET_KEY = config('SECRET_KEY', default='sua-chave-secreta-aqui')

# Database para produção
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

### Passo 2: Configurar Supabase (Banco de Dados)

1. Acesse: https://supabase.com
2. Crie uma conta gratuita
3. Clique em "New Project"
4. Preencha:
   - **Name:** wevo-media-db
   - **Database Password:** (crie uma senha forte)
   - **Region:** São Paulo (mais próximo do Brasil)
5. Aguarde a criação (2-3 minutos)
6. Vá em **Settings > Database**
7. Copie as credenciais:
   - Host
   - Database name
   - Port
   - User
   - Password

8. **IMPORTANTE:** Execute o SQL do seu banco:
   - Vá em **SQL Editor**
   - Copie e cole todo o conteúdo do arquivo SQL da sua estrutura de tabelas
   - Execute

### Passo 3: Deploy no Railway

1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em "New Project"
4. Escolha "Deploy from GitHub repo"
5. Conecte seu repositório GitHub
6. Selecione o repositório `wevo_media_bd`
7. Railway detectará automaticamente que é Django

### Passo 4: Configurar Variáveis de Ambiente no Railway

No dashboard do Railway, vá em **Variables** e adicione:

```env
DEBUG=False
SECRET_KEY=sua-chave-super-secreta-aqui-use-um-gerador
ALLOWED_HOSTS=seu-app.railway.app,*.railway.app

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua-senha-do-supabase
DB_HOST=db.xxx.supabase.co
DB_PORT=5432

DJANGO_SETTINGS_MODULE=wevo_media_project.settings
```

### Passo 5: Deploy

1. Railway fará deploy automático
2. Aguarde o build (2-5 minutos)
3. Acesse a URL gerada: `https://seu-app.railway.app`

### Passo 6: Executar Comandos no Railway

No Railway CLI ou pela interface:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

---

## OPÇÃO 2: Render + Supabase

### Vantagens:
- 750 horas grátis/mês
- PostgreSQL grátis (limitado)
- Deploy automático

### Configuração:

1. Acesse: https://render.com
2. Crie conta
3. **New > Web Service**
4. Conecte GitHub
5. Configure:
   - **Name:** wevo-media
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wevo_media_project.wsgi:application`
   - **Plan:** Free

6. Adicione variáveis de ambiente (igual Railway)

---

## OPÇÃO 3: PythonAnywhere (Mais Simples)

### Vantagens:
- Específico para Python/Django
- Interface mais amigável
- 1 app web grátis

### Desvantagens:
- Menos recursos
- Limite de tráfego

### Configuração:

1. Acesse: https://www.pythonanywhere.com
2. Crie conta gratuita
3. Vá em **Web**
4. **Add a new web app**
5. Escolha Django
6. Faça upload dos arquivos
7. Configure o WSGI file
8. Use MySQL grátis deles OU Supabase

---

## OPÇÃO 4: Fly.io

### Vantagens:
- Generoso no plano grátis
- Boa performance

### Desvantagens:
- Requer cartão de crédito (não cobra se ficar no free)

### Configuração:

1. Instale Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Execute:
```bash
fly launch
fly deploy
```

---

## Comparação Rápida

| Plataforma | Facilidade | Recursos Grátis | Melhor Para |
|------------|-----------|-----------------|-------------|
| **Railway** ⭐ | ⭐⭐⭐⭐⭐ | 500h/mês | Deploy rápido |
| **Render** | ⭐⭐⭐⭐ | 750h/mês | Projetos médios |
| **PythonAnywhere** | ⭐⭐⭐⭐⭐ | 1 app | Iniciantes |
| **Fly.io** | ⭐⭐⭐ | Generoso | Projetos escaláveis |
| **Vercel** | ❌ | Não recomendado para Django | - |

---

## Configurações Importantes para Produção

### 1. Gerar SECRET_KEY segura

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. Arquivos Estáticos

Certifique-se de ter:

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Adicionar middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adicionar
    # ... resto
]
```

### 3. CORS (se necessário)

```bash
pip install django-cors-headers
```

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "https://seu-dominio.com",
]
```

---

## Checklist de Deploy

- [ ] `.gitignore` atualizado com `.claude/`
- [ ] `requirements.txt` criado
- [ ] `runtime.txt` criado
- [ ] `Procfile` criado
- [ ] `settings.py` configurado para produção
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados criado no Supabase
- [ ] Estrutura SQL executada no Supabase
- [ ] Deploy realizado
- [ ] `collectstatic` executado
- [ ] `migrate` executado
- [ ] Usuário admin criado
- [ ] Testado em produção

---

## Estrutura Recomendada para Deploy

```
wevo_media_bd/
├── .gitignore          ✅ (.claude/ adicionado)
├── requirements.txt    ⚠️ Criar
├── runtime.txt         ⚠️ Criar
├── Procfile           ⚠️ Criar
├── manage.py
├── wevo_media_project/
│   ├── settings.py    ⚠️ Atualizar
│   └── wsgi.py
├── core/
├── templates/
└── static/
```

---

## Próximos Passos

1. **Escolha uma plataforma** (Recomendo Railway + Supabase)
2. **Prepare o projeto** (requirements.txt, Procfile, etc)
3. **Configure o banco** no Supabase
4. **Faça o deploy** no Railway
5. **Configure variáveis** de ambiente
6. **Execute migrations**
7. **Teste tudo**

---

## Suporte e Dúvidas

- Railway Docs: https://docs.railway.app/
- Supabase Docs: https://supabase.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

## Custos (após acabar o grátis)

- **Railway:** ~$5-10/mês
- **Render:** ~$7/mês
- **Supabase:** Grátis para sempre (até 500MB) ou $25/mês Pro
- **PythonAnywhere:** $5/mês

---

## Dica Extra: Domínio Personalizado

Após deploy, você pode adicionar domínio personalizado:

1. Compre domínio (.com.br ~R$40/ano)
2. Configure DNS apontando para a plataforma
3. Adicione domínio nas configurações do Railway/Render

**Domínios grátis:**
- Freenom (não recomendado)
- Use o subdomínio da plataforma: `seu-app.railway.app`

---

Boa sorte com o deploy! 🚀
