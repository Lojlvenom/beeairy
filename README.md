# 🐝 BeeAiry

Sistema de gerenciamento para **meliponários** (abelhas sem ferrão) e **apiários** (abelhas *Apis*).

Este repositório contém o **backend** do BeeAiry, uma API REST construída com **FastAPI**, **SQLAlchemy 2.0** e **SQLite**.

## ✨ Funcionalidades atuais

- CRUD completo de **espécies de abelhas**
  - Nome popular e nome científico (único)
  - Tipo: `stingless` (sem ferrão / meliponíneos) ou `apis`
  - Indicação se a espécie é nativa
  - Descrição livre
- Listagem com paginação (`skip`, `limit`), filtro por tipo (`bee_type`) e busca por nome (`search`)
- Documentação interativa automática (Swagger / ReDoc)
- Testes automatizados com pytest

## 🧱 Stack

| Camada        | Tecnologia            |
|---------------|-----------------------|
| Framework     | FastAPI               |
| ORM           | SQLAlchemy 2.0        |
| Banco         | SQLite                |
| Validação     | Pydantic v2           |
| Servidor      | Uvicorn               |
| Testes        | pytest + TestClient   |

## 📁 Estrutura

```
beeairy/
├── app/
│   ├── main.py          # Instância do FastAPI e registro das rotas
│   ├── config.py        # Configurações (variáveis de ambiente / .env)
│   ├── database.py      # Engine, sessão e Base do SQLAlchemy
│   ├── models/          # Modelos ORM (tabelas)
│   ├── schemas/         # Schemas Pydantic (entrada/saída da API)
│   ├── crud/            # Operações de banco de dados
│   └── routers/         # Endpoints da API
├── tests/               # Testes automatizados
├── requirements.txt
└── requirements-dev.txt
```

## 🚀 Como rodar

```bash
# 1. Clonar o repositório
git clone https://github.com/<seu-usuario>/beeairy.git
cd beeairy

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements-dev.txt

# 4. (Opcional) Configurar variáveis de ambiente
cp .env.example .env

# 5. Subir a API
uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

O arquivo do banco (`beeairy.db`) é criado automaticamente na primeira execução.

## 🧪 Testes

```bash
pytest
```

Os testes usam um banco SQLite em memória, sem afetar o `beeairy.db`.

## 📡 Endpoints

| Método   | Rota            | Descrição                                   |
|----------|-----------------|---------------------------------------------|
| `GET`    | `/health`       | Verifica se a API está no ar                |
| `GET`    | `/bees`         | Lista abelhas (filtros: `bee_type`, `search`, `skip`, `limit`) |
| `POST`   | `/bees`         | Cadastra uma abelha                         |
| `GET`    | `/bees/{id}`    | Busca uma abelha pelo ID                    |
| `PATCH`  | `/bees/{id}`    | Atualiza parcialmente uma abelha            |
| `DELETE` | `/bees/{id}`    | Remove uma abelha                           |

### Exemplo

```bash
curl -X POST http://localhost:8000/bees \
  -H "Content-Type: application/json" \
  -d '{
        "common_name": "Jataí",
        "scientific_name": "Tetragonisca angustula",
        "bee_type": "stingless",
        "native": true,
        "description": "Abelha sem ferrão, dócil e muito comum no Brasil."
      }'
```

## 🔮 Próximas atualizações (Future Updates)

### Frontend
- [ ] **Interface web** para gerenciar o meliponário/apiário (consumindo esta API)
- [ ] Dashboard com visão geral das colmeias, produção e alertas
- [ ] Layout responsivo para uso no campo (celular/tablet)

### Backend
- [ ] Cadastro de **meliponários/apiários** (locais, localização geográfica)
- [ ] Cadastro de **colmeias/caixas** vinculadas a uma espécie e a um local
- [ ] Registro de **inspeções/manejos** (data, força da colônia, observações)
- [ ] Controle de **produção** (mel, própolis, pólen, geoprópolis)
- [ ] Registro de **divisões/multiplicação** de colônias
- [ ] Controle de **alimentação** artificial
- [ ] Autenticação e usuários (JWT)
- [ ] Migrations com **Alembic**
- [ ] Suporte a PostgreSQL para produção
- [ ] Docker / docker-compose
- [ ] CI com GitHub Actions

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
