# FoodLink — Sistema de Doação de Alimentos

Projeto desenvolvido para a disciplina de **Laboratório de Engenharia de Software** da Universidade Presbiteriana Mackenzie, sob a orientação do **Prof. Msc. Luiz Carlos Machi Lozano**.

### Equipe Desenvolvedora

- **Enzo Ponte Gamberi** — RA: 10389931
- **João Guilherme Messias de Oliveira Santos** — RA: 10426110
- **Thiago Ruiz Fernandes Silva** — RA: 10426057

---

## Sobre o Projeto

O **FoodLink** é uma plataforma digital web com forte caráter extensionista. O cenário atual brasileiro apresenta um paradoxo crítico: altos índices de desperdício de alimentos viáveis para consumo por parte do setor de comércio, em contraste com a insegurança alimentar enfrentada por parcelas vulneráveis da população.

A solução atua como uma ponte tecnológica, estabelecendo uma rede de comunicação eficiente e rastreável entre quem deseja doar (pessoas físicas, padarias, mercados) e quem precisa receber (ONGs, abrigos e instituições sociais).

---

## Funcionalidades Implementadas

### Perfil Doador
- Cadastro de conta com endereço (busca automática por CEP)
- Registro de alimentos disponíveis informando nome, quantidade, validade e categoria
- Acompanhamento do ciclo de vida da doação: Disponível > Reservado > Entregue
- Confirmação de entrega e cancelamento de doações

### Perfil Instituição
- Feed interativo com todas as doações disponíveis em tempo real
- Filtro por categoria e busca por nome
- Reserva exclusiva de itens com controle de concorrência (SELECT FOR UPDATE)
- Cancelamento de reserva, devolvendo o item ao feed

---

## Arquitetura

O projeto adota a arquitetura **Client-Server**, separando a interface do usuário da API de negócios.

```
Browser (HTML/CSS/JS)
        |
        | HTTP/REST (JSON)
        v
FastAPI + Uvicorn (Python)
        |
        | SQLAlchemy ORM
        v
   SQLite Database
```

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | HTML5, CSS3, JavaScript Vanilla, Bootstrap 5 |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Banco de dados | SQLite (desenvolvimento) |
| ORM | SQLAlchemy |
| Autenticacao | Token SHA-256 |
| CI/CD | GitHub Actions |
| Cloud (previsto) | AWS EC2 |

---

## Estrutura do Repositorio

```
Lab_Eng_Software/
├── .github/
│   └── workflows/
│       └── ci.yml          — Pipeline de CI/CD (GitHub Actions)
├── backend/
│   ├── main.py             — API FastAPI: endpoints e regras de negocio
│   ├── models.py           — Modelos SQLAlchemy (tabelas do banco)
│   ├── schemas.py          — Schemas Pydantic (validacao de dados)
│   ├── database.py         — Configuracao do banco SQLite
│   └── requirements.txt    — Dependencias Python
├── frontend/
│   ├── index.html          — Tela de Login
│   ├── cadastro.html       — Cadastro de novo usuario
│   ├── doador.html         — Dashboard do Doador
│   └── instituicao.html    — Feed da Instituicao
├── Diagramas/              — Diagramas UML (Casos de Uso, Dominio, Sequencia)
└── TG1.pdf                 — Documento de Especificacao e Modelagem
```

---

## Como Rodar Localmente

### Pre-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

| Ferramenta | Versao minima | Download |
|------------|--------------|---------|
| Python | 3.11 | https://www.python.org/downloads/ |
| VSCode | qualquer | https://code.visualstudio.com/ |
| Extensao Live Server (VSCode) | qualquer | Instalar pela aba de extensoes do VSCode |

> O Python ja inclui o pip. Nao e necessario instalar nada adicional alem do que esta na tabela acima.

### Passo a passo

**1. Clone o repositorio**
```bash
git clone https://github.com/epGamberi/Lab_Eng_Software.git
cd Lab_Eng_Software
```

**2. Instale as dependencias do backend**
```bash
cd backend
pip install -r requirements.txt
```

**3. Inicie a API**
```bash
uvicorn main:app --reload
```

A API estara disponivel em: `http://localhost:8000`

Documentacao interativa (Swagger): `http://localhost:8000/docs`

**4. Abra o frontend**

No VSCode, clique com o botao direito no arquivo `frontend/index.html` e selecione **Open with Live Server**.

O sistema abrira no navegador em: `http://127.0.0.1:5500/frontend/index.html`

> Mantenha o terminal com o `uvicorn` aberto enquanto usa o sistema.

### Verificacao rapida (checklist)

Execute esses comandos para confirmar que tudo esta funcionando antes de apresentar:

```bash
python --version        # deve mostrar Python 3.11 ou superior
pip --version           # deve mostrar a versao do pip
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Se o terminal mostrar `Application startup complete`, o backend esta pronto.

---

## Endpoints da API

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | `/` | Health check |
| POST | `/cadastro` | Cadastrar novo usuario |
| POST | `/login` | Autenticar usuario |
| GET | `/categorias` | Listar categorias de alimentos |
| POST | `/doacoes?doador_id=` | Criar nova doacao |
| GET | `/doacoes` | Listar doacoes disponiveis |
| GET | `/doacoes/usuario/{id}` | Doacoes de um usuario especifico |
| POST | `/doacoes/{id}/reservar?instituicao_id=` | Reservar item |
| POST | `/doacoes/{id}/entregar?doador_id=` | Confirmar entrega |
| POST | `/doacoes/{id}/cancelar?usuario_id=` | Cancelar doacao ou reserva |

---

## Status do Projeto

**Fase 1 (N1) — Concluida:** Definicao do produto, Engenharia de Requisitos, Wireframes e Modelagem UML.

**Fase 2 (N2) — Em andamento:** Backend (FastAPI + SQLite), Frontend (HTML/JS/Bootstrap), CI/CD (GitHub Actions).

**Fase 3 (N3) — Prevista:** Deploy na AWS EC2, Nginx, SSL/TLS, banco PostgreSQL em producao.