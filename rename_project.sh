#!/bin/bash
# Script para renomear o projeto ArmoredDjango
# Uso: ./rename_project.sh novo_nome

set -e

OLD_NAME="armoreddjango"
NEW_NAME="$1"

# Validação
if [ -z "$NEW_NAME" ]; then
    echo "❌ Erro: Nome do projeto não fornecido"
    echo "Uso: ./rename_project.sh novo_nome"
    echo ""
    echo "Exemplo:"
    echo "  ./rename_project.sh myproject"
    exit 1
fi

# Converte para lowercase e substitui caracteres
NEW_NAME=$(echo "$NEW_NAME" | tr '[:upper:]' '[:lower:]' | tr '-' '_' | tr ' ' '_')

# Validação do nome
if ! [[ "$NEW_NAME" =~ ^[a-z][a-z0-9_]*$ ]]; then
    echo "❌ Nome inválido: '$NEW_NAME'"
    echo "O nome deve começar com letra minúscula e conter apenas letras, números e underscores."
    exit 1
fi

echo "🔄 Renomeando projeto de '$OLD_NAME' para '$NEW_NAME'..."
echo ""

# Confirmação
read -p "⚠️  Esta operação modificará vários arquivos. Deseja continuar? (s/N): " -r
echo ""
if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
    echo "❌ Operação cancelada."
    exit 0
fi

echo "📝 Atualizando conteúdo dos arquivos..."

# Função para substituir em arquivo
replace_in_file() {
    local file="$1"
    if [ -f "$file" ]; then
        sed -i "s/$OLD_NAME/$NEW_NAME/g" "$file"
        sed -i "s/ArmoredDjango/$(echo $NEW_NAME | sed 's/_//g' | sed 's/\b\(.\)/\u\1/g')/g" "$file"
        sed -i "s/ARMOREDDJANGO/$(echo $NEW_NAME | tr '[:lower:]' '[:upper:]')/g" "$file"
        echo "   ✓ $file"
    fi
}

# Atualiza arquivos
replace_in_file "docker-compose.yaml"
replace_in_file "README.md"
replace_in_file "service/pyproject.toml"
replace_in_file "service/src/manage.py"
replace_in_file "service/src/gunicorn_config.py"
replace_in_file "service/scripts/start.sh"
replace_in_file "service/scripts/run_unit_tests.sh"

# Atualiza arquivos do app
for file in service/src/$OLD_NAME/*.py service/src/$OLD_NAME/settings/*.py service/src/$OLD_NAME/settings/*.md; do
    replace_in_file "$file"
done

# Atualiza utils
replace_in_file "service/src/utils/__init__.py"
replace_in_file "service/src/utils/emails.py"

echo ""
echo "📁 Renomeando diretórios..."

# Renomeia diretório principal
if [ -d "service/src/$OLD_NAME" ]; then
    mv "service/src/$OLD_NAME" "service/src/$NEW_NAME"
    echo "   ✓ service/src/$OLD_NAME → service/src/$NEW_NAME"
fi

echo ""
echo "✅ Projeto renomeado com sucesso para '$NEW_NAME'!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Reconstruir os containers: docker compose build"
echo "   2. Iniciar os containers: docker compose up -d"
echo "   3. Atualizar o arquivo .env se necessário"
