FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro (para cache eficiente)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte
COPY src/ ./src/
COPY data/ ./data/

# Define o comando padrão
CMD ["python", "-c", "import src.csv_analyzer; src.csv_analyzer.main()"]
