"""
Configuração do Gunicorn para Django WSGI.

Configuração otimizada para APIs REST tradicionais (CRUD).
Para outros casos de uso (SSE, streaming, LLM), veja README.md seção "Configurações do Gunicorn".
"""

# Bom equilíbrio para APIs tradicionais (CRUD, REST)
# Requests curtas, pouco processamento pesado
# Workers escalam CPU, threads ajudam em I/O leve (DB, cache)

workers = 4  # Escala bem em máquinas com 2–4 vCPUs
threads = 2  # Pequeno ganho em I/O sem inflar memória
timeout = 30  # Padrão seguro

bind = "0.0.0.0:8003"
chdir = "/app/"
module = "armoreddjango.wsgi:application"
