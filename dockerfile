FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema e PDM
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pdm

# Copia arquivos de configuração
COPY pyproject.toml ./

# Tenta instalar com PDM, se falhar usa pip como fallback
RUN pdm install --prod --no-lock || pip install -r requirements.txt || pip install pandas matplotlib fpdf

# Copia código fonte
COPY src/ ./src/
COPY data/ ./data/

# Comando padrão
CMD ["python", "-m", "csv_analyzer"]
