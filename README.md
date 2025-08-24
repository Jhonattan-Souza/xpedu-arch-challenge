XPEDU Arch Challenge — API REST (FastAPI)

Descrição
- API RESTful para gestão de Clientes, construída em Python com FastAPI, seguindo arquitetura em camadas (MVC orientado a serviços) e persistência em SQLite via SQLAlchemy.
- Inclui endpoints de CRUD, contagem, busca por ID, listagem completa e busca por nome (retorna múltiplos registros).
- Diagrama de arquitetura no formato C4 (PlantUML) disponível em `docs/components.puml`.

Arquitetura (Camadas)
- Controller (Rotas): expõe HTTP e transforma requisições em chamadas de serviço. Arquivos em `app/routers/*`.
- Service (Aplicação): orquestra casos de uso e validações de alto nível. Arquivos em `app/services/*`.
- Domain (Modelo de Negócio): entidades e regras do domínio. Arquivos em `app/domain/*`.
- Infrastructure (Técnica): ORM, repositórios, sessão do banco e integrações. Arquivos em `app/infrastructure/*`.

Estrutura MVC
- Controller: `app/routers/*` — recebe a requisição HTTP, valida a entrada, chama o serviço certo e define status code de resposta.
- Model: duas partes aqui:
  - Domínio: `app/domain/*` — as entidades e regras do negócio (não sabem nada de banco ou web).
  - Persistência: `app/infrastructure/customer_model.py` — o modelo ORM que mapeia a tabela e conversa com o banco.
- View: em API, a “view” é o que a gente devolve em JSON. Aqui são os modelos Pydantic de request/response em `app/routers/*_request.py` e `app/routers/*_response.py` (eles formatam o que entra e o que sai).

Estrutura de Pastas
- `app/main.py`: instancia o FastAPI e registra as rotas; cria as tabelas.
- `app/routers/customers.py`: rotas REST de clientes.
- `app/routers/create_customer_request.py`: schema de entrada (Pydantic) para criação/atualização.
- `app/services/customer_service.py`: casos de uso de clientes.
- `app/domain/customer.py`: entidade de domínio Customer.
- `app/infrastructure/customer_model.py`: modelo ORM (SQLAlchemy) de Customer.
- `app/infrastructure/customer_repository.py`: repositório (CRUD, busca e contagem).
- `app/infrastructure/session.py`: engine e fábrica de sessões; lê `DATABASE_URL`.
- `docs/components.puml`: diagrama C4 (PlantUML) dos componentes.

Pastas
- `app/`: onde vive o código da API.
- `app/routers/`: endpoints HTTP (Controllers) e os modelos Pydantic de request/response (fazem o papel de View na API).
- `app/services/`: regras de aplicação e orquestração dos casos de uso.
- `app/domain/`: modelos do domínio (o “M” de MVC do ponto de vista de negócio).
- `app/infrastructure/`: conversa com o banco (ORM, repositório, sessão) — também parte do “M”, mas focado em persistência.
- `docs/`: diagramas e materiais de arquitetura.
- `Dockerfile`/`.dockerignore`: suporte pra build e container.

Requisitos
- Python 3.13+
- Dependências (instalação com uv/venv/pip): `fastapi[standard]`, `sqlalchemy`

Como Executar (Local)
1) Instalar dependências
   - Com FastAPI CLI (recomendado):
     - `pip install fastapi[standard] sqlalchemy`
   - Ou via projeto (pyproject):
     - `pip install -e .` (ou ferramenta de sua preferência)

2) Rodar a aplicação
   - Com FastAPI CLI (auto-reload):
     - `fastapi dev app/main.py`
   - Ou com Uvicorn:
     - `uvicorn app.main:app --reload`

3) Acessar
   - API: `http://localhost:8000`
   - Documentação (Swagger): `http://localhost:8000/docs`

Configuração do Banco de Dados
- Variável de ambiente: `DATABASE_URL`
  - Padrão (desenvolvimento): `sqlite:///./app.db` (arquivo na raiz do projeto)
  - Exemplo absoluto: `sqlite:////abs/path/para/meu.db`

Endpoints (Clientes)
- POST `/customers`: cria cliente. Body: `{ "name": "...", "email": "..." }`. Retorna o objeto criado.
- GET `/customers`: lista todos os clientes.
- GET `/customers/id/{id}`: retorna cliente pelo ID. 404 se não existir.
- GET `/customers/by-name?name=...`: retorna lista de clientes cujo nome corresponde (ilike `%nome%`). Sempre retorna lista (vazia se nenhum).
- GET `/customers/count`: retorna contagem total de clientes.
- PUT `/customers/id/{id}`: atualiza cliente. Body: `{ "name": "...", "email": "..." }`. 404 se não existir.
- DELETE `/customers/id/{id}`: exclui cliente. 204 se sucesso, 404 se não existir.

Uso com Docker
Observação sobre SQLite sendo compartilhado com a pasta local:
- Se você sobe o container montando o diretório do projeto (ex.: `-v $(pwd):/app`), e a app usa o caminho padrão `sqlite:///./app.db`, o arquivo dentro do container (`/app/app.db`) é o mesmo arquivo montado do host. Resultado: o container “usa o mesmo SQLite da pasta local”.

Soluções
- Opção A — Usar DB dentro do container (não persistente):
  - Configure a variável `DATABASE_URL` para um caminho fora do diretório montado (ou não monte o diretório):
    - `DATABASE_URL=sqlite:////data/app.db`
  - E rode o container sem bind mount do projeto ou com um volume dedicado para `/data`:
    - `docker run -e DATABASE_URL=sqlite:////data/app.db -v xpedu-db:/data -p 8000:8000 <seu-image>`
  - O volume `xpedu-db` armazena o banco separadamente do código.

- Opção B — Evitar montar o projeto na mesma pasta do DB:
  - Se precisar do bind mount do código (desenvolvimento), direcione o DB para outro caminho via `DATABASE_URL` e monte um volume dedicado para esse caminho, como acima.

Exemplos de Execução com Docker
- Build:
  - `docker build -t xpedu-api .`
- Rodar com volume dedicado do DB:
  - `docker run --rm -e DATABASE_URL=sqlite:////data/app.db -v xpedu-db:/data -p 8000:80 xpedu-api`
- Rodar sem persistência (DB efêmero no container):
  - `docker run --rm -e DATABASE_URL=sqlite:////tmp/app.db -p 8000:80 xpedu-api`

Diagrama de Arquitetura
- Arquivo: `docs/components.puml` (C4/PlantUML). Você pode visualizar pelo PlantUML (IDE plugin, CLI) ou importar no draw.io.
