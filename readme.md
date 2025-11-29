Projeto simples para ler e validar um CSV de usuários.

Resumo
- Entrada: arquivo CSV (obrigatório).
- Saída: diretório com valid.csv (linhas válidas) e report.json (relatório).
- Linguagem: Python 3.11
- Gerenciador de dependências: pip (requirements.txt)

Escolha do grupo e gerenciador
[Grupo Alpha] — escolhemos o gerenciador: pip (requirements.txt)

Dependências reaproveitadas (>=3)
- pandas >=1.5.0     (leitura/transformação de CSV)
- pydantic >=1.10.0  (validação de dados)
- rich >=13.0.0      (exibição amigável no terminal)

Instalação (local)
1. Criar/ativar um virtualenv (recomendado)
2. Instalar dependências:
   pip install -r requirements.txt

Exemplo de uso (local)
python main.py dados/usuarios.csv -o resultado

Outputs (diretório resultado)
- valid.csv    (linhas válidas)
- report.json  (resumo e detalhes de linhas inválidas)

Docker (build local)
# Observação: o Dockerfile no repositório está nomeado 'dockerfile' — use -f se necessário
docker build -t file-processor:latest -f dockerfile .
docker run --rm -v /caminho/para/input:/app/input -v /caminho/para/out:/app/out file-processor:latest input/usuarios.csv -o out

Publicação da imagem no GitHub Container Registry (exemplo)
# substituir <OWNER> e <REPO> pelos valores reais
docker tag file-processor:latest ghcr.io/<OWNER>/<REPO>:v1.0.0
docker push ghcr.io/<OWNER>/<REPO>:v1.0.0

Executar imagem publicada (exemplo)
docker run --rm -v /caminho/para/input:/app/input -v /caminho/para/out:/app/out ghcr.io/<OWNER>/<REPO>:v1.0.0 input/usuarios.csv -o out

Fluxo Git / colaboração (orientações para a entrega)
- Branches: main (produção) e develop (integração). Features em feature/*.
- Criar pelo menos um Pull Request para main; a fusão deve ser feita por Squash & Merge.
- O PR para main deve conter ≥ 3 commits antes do squash.
- Commits: seguir Conventional Commits (ex.: feat:, fix:, chore:).
- Versionamento: SemVer; criar tags (ex.: v1.0.0) e Release no GitHub.
- Antes da apresentação: publicar a imagem no ghcr.io e garantir que um membro do grupo faça o push.

Apresentação
- Data da apresentação: 28/11/2025
- Pontos a apresentar: dependências reaproveitadas, gerenciador de dependências (pip), fluxo Git (branches/PR), e demonstração local + Docker/GHCR.
