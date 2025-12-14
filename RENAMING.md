# 🔄 Renomear Projeto

Este guia explica como usar os scripts de renomeação incluídos no ArmoredDjango.

## 🎯 Objetivo

Os scripts de renomeação permitem que você transforme o **ArmoredDjango** no seu próprio projeto, alterando automaticamente todos os nomes e referências.

## 📝 Scripts Disponíveis

### 1. Script Python (`rename_project.py`)

**Recomendado para máxima compatibilidade**

```bash
python rename_project.py novo_nome
```

**Características:**

- ✅ Validação rigorosa do nome
- ✅ Mensagens de progresso detalhadas
- ✅ Confirmação antes de executar
- ✅ Tratamento de erros robusto
- ✅ Funciona em Windows, Linux e macOS

### 2. Script Bash (`rename_project.sh`)

**Recomendado para usuários Linux/macOS**

```bash
./rename_project.sh novo_nome
```

**Características:**

- ✅ Mais rápido que Python
- ✅ Usa ferramentas Unix nativas
- ✅ Confirmação antes de executar
- ✅ Apenas Linux/macOS

## 🚀 Como Usar

### Passo 1: Escolha um nome

Regras para o nome do projeto:

- ✅ Deve começar com letra minúscula
- ✅ Pode conter letras, números e underscores
- ✅ Não pode conter espaços ou hífens (serão convertidos)
- ✅ Exemplos válidos: `myproject`, `blog_api`, `ecommerce2024`

### Passo 2: Execute o script

```bash
# Python
python rename_project.py myproject

# Ou Bash
./rename_project.sh myproject
```

### Passo 3: Confirme a operação

O script pedirá confirmação:

```
⚠️  ATENÇÃO: Este script irá renomear o projeto para 'myproject'
   Esta operação modificará vários arquivos e diretórios.

   Deseja continuar? (s/N):
```

Digite `s` ou `y` para continuar.

### Passo 4: Aguarde a conclusão

O script mostrará o progresso:

```
🔄 Renomeando projeto de 'armoreddjango' para 'myproject'...

📝 Atualizando conteúdo dos arquivos...
   ✓ docker-compose.yaml
   ✓ README.md
   ✓ service/pyproject.toml
   ...

📁 Renomeando diretórios...
   ✓ service/src/armoreddjango → service/src/myproject

✅ Projeto renomeado com sucesso para 'myproject'!
```

### Passo 5: Reconstrua os containers

```bash
# Reconstruir as imagens Docker
docker compose build

# Iniciar os containers
docker compose up -d

# Verificar se está funcionando
docker logs myproject_service
```

## 📋 O Que é Renomeado?

### Arquivos Atualizados

- ✅ `docker-compose.yaml` - nomes de containers e serviços
- ✅ `README.md` - referências ao projeto
- ✅ `service/pyproject.toml` - nome do pacote
- ✅ `service/src/manage.py` - configurações Django
- ✅ `service/src/gunicorn_config.py` - configuração do servidor
- ✅ `service/scripts/start.sh` - scripts de inicialização

### Diretórios Renomeados

- ✅ `service/src/armoreddjango/` → `service/src/seu_projeto/`

### Código Python Atualizado

- ✅ Imports: `from armoreddjango.settings` → `from seu_projeto.settings`
- ✅ WSGI: `armoreddjango.wsgi` → `seu_projeto.wsgi`
- ✅ ASGI: `armoreddjango.asgi` → `seu_projeto.asgi`
- ✅ URLs: `armoreddjango.urls` → `seu_projeto.urls`
- ✅ Settings: todos os módulos de configuração

### Variantes do Nome

O script atualiza três variantes do nome:

1. **lowercase**: `armoreddjango` → `seu_projeto`
2. **TitleCase**: `ArmoredDjango` → `SeuProjeto`
3. **UPPERCASE**: `ARMOREDDJANGO` → `SEU_PROJETO`

## 🔍 Verificação

Após renomear, verifique se tudo está funcionando:

```bash
# 1. Verificar sintaxe Python
docker exec seu_projeto_service python src/manage.py check

# 2. Testar import das configurações
docker exec seu_projeto_service python -c "from django.conf import settings; print(settings.SECRET_KEY[:10])"

# 3. Executar testes
docker exec seu_projeto_service bash -c "cd src && pytest"

# 4. Acessar a API
curl http://localhost:8003/api/docs/
```

## ⚠️ Importante

### Antes de Executar

- 🔴 **Faça backup** do projeto antes de renomear
- 🔴 **Pare os containers**: `docker compose down`
- 🔴 **Não execute** com containers rodando

### Após Executar

- 🟢 **Reconstrua as imagens** Docker
- 🟢 **Atualize o `.env`** se necessário
- 🟢 **Verifique os logs** após iniciar

### Git

Se estiver usando Git:

```bash
# Adicionar mudanças
git add -A

# Commit
git commit -m "Renomear projeto para myproject"
```

## 🆘 Problemas Comuns

### "Nome inválido"

- Certifique-se de que o nome começa com letra minúscula
- Use apenas letras, números e underscores

### "Diretório já existe"

- O diretório de destino já existe
- Escolha outro nome ou remova o diretório manualmente

### "Containers ainda rodando"

```bash
# Pare todos os containers
docker compose down
```

### "Imports quebrados"

```bash
# Reconstrua completamente
docker compose build --no-cache
docker compose up -d
```

## 💡 Dicas

1. **Use nomes descritivos**: `blog_api` é melhor que `projeto1`
2. **Mantenha lowercase**: evita problemas de case sensitivity
3. **Teste imediatamente**: após renomear, teste tudo antes de continuar desenvolvendo
4. **Atualize o README**: personalize o README.md com informações do seu projeto

## 📚 Próximos Passos

Após renomear com sucesso:

1. ✅ Atualize o `README.md` com informações do seu projeto
2. ✅ Configure suas variáveis de ambiente no `.env`
3. ✅ Customize os modelos em `authentication/models/`
4. ✅ Adicione seus próprios apps Django
5. ✅ Configure repositório Git se ainda não fez
6. ✅ Comece a desenvolver! 🚀
