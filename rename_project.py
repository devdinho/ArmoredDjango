#!/usr/bin/env python3
"""
Script para renomear o projeto ArmoredDjango para um novo nome.
Este script é útil quando o projeto é usado como template.

Uso:
    python rename_project.py <novo_nome>

Exemplo:
    python rename_project.py myproject
"""

import os
import re
import sys
import shutil
from pathlib import Path


class ProjectRenamer:
    """Renomeia o projeto ArmoredDjango para um novo nome."""

    def __init__(self, new_name: str):
        self.old_name = "armoreddjango"
        self.new_name = new_name.lower().replace("-", "_").replace(" ", "_")
        self.old_name_title = "ArmoredDjango"
        self.new_name_title = self.new_name.title().replace("_", "")
        self.root_dir = Path(__file__).parent
        self.service_dir = self.root_dir / "service"
        
        # Validação do nome
        if not re.match(r'^[a-z][a-z0-9_]*$', self.new_name):
            raise ValueError(
                f"Nome inválido: '{new_name}'. "
                "O nome deve começar com letra minúscula e conter apenas "
                "letras, números e underscores."
            )

    def run(self):
        """Executa o processo de renomeação."""
        print(f"🔄 Renomeando projeto de '{self.old_name}' para '{self.new_name}'...\n")
        
        try:
            self.update_files_content()
            self.rename_directories()
            print(f"\n✅ Projeto renomeado com sucesso para '{self.new_name}'!")
            print(f"\n📝 Próximos passos:")
            print(f"   1. Reconstruir os containers: docker compose build")
            print(f"   2. Iniciar os containers: docker compose up -d")
            print(f"   3. Atualizar o arquivo .env se necessário")
            
        except Exception as e:
            print(f"\n❌ Erro durante a renomeação: {e}")
            sys.exit(1)

    def update_files_content(self):
        """Atualiza o conteúdo dos arquivos."""
        print("📝 Atualizando conteúdo dos arquivos...")
        
        # Arquivos a serem processados
        files_to_update = [
            # Root
            self.root_dir / "docker-compose.yaml",
            self.root_dir / "README.md",
            
            # Service
            self.service_dir / "pyproject.toml",
            
            # Source files
            self.service_dir / "src" / "manage.py",
            self.service_dir / "src" / self.old_name / "asgi.py",
            self.service_dir / "src" / self.old_name / "wsgi.py",
            self.service_dir / "src" / self.old_name / "urls.py",
            self.service_dir / "src" / self.old_name / "settings" / "__init__.py",
            self.service_dir / "src" / self.old_name / "settings" / "base.py",
            self.service_dir / "src" / self.old_name / "settings" / "env.py",
            self.service_dir / "src" / self.old_name / "settings" / "apps.py",
            self.service_dir / "src" / self.old_name / "settings" / "rest_framework.py",
            self.service_dir / "src" / self.old_name / "settings" / "security.py",
            self.service_dir / "src" / self.old_name / "settings" / "static.py",
            self.service_dir / "src" / self.old_name / "settings" / "README.md",
            
            # Scripts
            self.service_dir / "scripts" / "start.sh",
            self.service_dir / "scripts" / "run_unit_tests.sh",
            
            # Gunicorn
            self.service_dir / "src" / "gunicorn_config.py",
            
            # Utils
            self.service_dir / "src" / "utils" / "__init__.py",
            self.service_dir / "src" / "utils" / "emails.py",
        ]
        
        # Processa cada arquivo
        for file_path in files_to_update:
            if file_path.exists():
                self._update_file_content(file_path)
            else:
                print(f"   ⚠️  Arquivo não encontrado: {file_path.relative_to(self.root_dir)}")

    def _update_file_content(self, file_path: Path):
        """Atualiza o conteúdo de um arquivo específico."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Substituições
            replacements = [
                (self.old_name, self.new_name),  # armoreddjango -> newname
                (self.old_name_title, self.new_name_title),  # ArmoredDjango -> NewName
                (self.old_name.upper(), self.new_name.upper()),  # ARMOREDDJANGO -> NEWNAME
            ]
            
            original_content = content
            for old, new in replacements:
                content = content.replace(old, new)
            
            # Só reescreve se houve mudanças
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✓ {file_path.relative_to(self.root_dir)}")
        
        except Exception as e:
            print(f"   ✗ Erro ao processar {file_path.relative_to(self.root_dir)}: {e}")

    def rename_directories(self):
        """Renomeia os diretórios do projeto."""
        print("\n📁 Renomeando diretórios...")
        
        # Diretório principal do app
        old_dir = self.service_dir / "src" / self.old_name
        new_dir = self.service_dir / "src" / self.new_name
        
        if old_dir.exists():
            if new_dir.exists():
                print(f"   ⚠️  Diretório '{self.new_name}' já existe. Pulando...")
            else:
                shutil.move(str(old_dir), str(new_dir))
                print(f"   ✓ {old_dir.relative_to(self.root_dir)} → {new_dir.relative_to(self.root_dir)}")
        else:
            print(f"   ⚠️  Diretório '{self.old_name}' não encontrado")
        
        # Atualiza referências em arquivos que foram movidos
        self._update_moved_directory_references(new_dir)

    def _update_moved_directory_references(self, new_dir: Path):
        """Atualiza referências nos arquivos do diretório renomeado."""
        if not new_dir.exists():
            return
        
        # Procura todos os arquivos Python no novo diretório
        for py_file in new_dir.rglob("*.py"):
            self._update_file_content(py_file)


def main():
    """Função principal."""
    if len(sys.argv) != 2:
        print("Uso: python rename_project.py <novo_nome>")
        print("\nExemplo:")
        print("  python rename_project.py myproject")
        sys.exit(1)
    
    new_name = sys.argv[1]
    
    # Confirmação
    print(f"\n⚠️  ATENÇÃO: Este script irá renomear o projeto para '{new_name}'")
    print("   Esta operação modificará vários arquivos e diretórios.")
    response = input("\n   Deseja continuar? (s/N): ")
    
    if response.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada.")
        sys.exit(0)
    
    try:
        renamer = ProjectRenamer(new_name)
        renamer.run()
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
