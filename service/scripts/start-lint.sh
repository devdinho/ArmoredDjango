#!/usr/bin/env sh

set -e

# Define src/ como padrão se não houver argumento
TARGET=${1:-src/}

echo "Executando Black"
black -q --check --diff "$TARGET"
echo "Executando Isort"
isort -q --check --diff "$TARGET"
echo "Executando Flake8"
flake8 --ignore=E211,E999,F821,W503,E203 --max-line-length=121 --exclude=migrations,settings,__pycache__,tests "$TARGET"
echo "✅ Verificação concluída"