# FoodLink — Sistema de Doação de Alimentos

Projeto desenvolvido para a disciplina de **Laboratório de Engenharia de Software** da Universidade Presbiteriana Mackenzie, sob a orientação do **Prof. Msc. Luiz Carlos Machi Lozano**.

### Equipe Desenvolvedora

- **Enzo Ponte Gamberi** — RA: 10389931
- **João Guilherme Messias de Oliveira Santos** — RA: 10426110
- **Thiago Ruiz Fernandes Silva** — RA: 10426057

---

## 🌐 Deploy — Sistema em Produção

| Componente | URL |
|---|---|
| **Frontend (Vercel)** | https://lab-eng-software-pied.vercel.app |
| **Backend (Render)** | https://foodlink-backend-m6n0.onrender.com |
| **Documentação da API (Swagger)** | https://foodlink-backend-m6n0.onrender.com/docs |
| **Banco de dados** | PostgreSQL — Render (Oregon) |

> ⚠️ O plano gratuito do Render hiberna após 15 minutos sem uso. A primeira requisição pode levar até 50 segundos para responder — aguarde e tente novamente.

---

## Sobre o Projeto

O **FoodLink** é uma plataforma digital web com forte caráter extensionista. O cenário atual brasileiro apresenta um paradoxo crítico: altos índices de desperdício de alimentos viáveis para consumo por parte do setor de comércio, em contraste com a insegurança alimentar enfrentada por parcelas vulneráveis da população.

A solução atua como uma ponte tecnológica, estabelecendo uma rede de comunicação eficiente e rastreável entre quem deseja doar (pessoas físicas, padarias, mercados) e quem precisa receber (ONGs, abrigos e instituições sociais).

O ciclo de vida de uma doação segue os estados: `DISPONIVEL → RESERVADO → ENTREGUE` (ou `CANCELADO`).

---

## Funcionalidades Implementadas

### Perfil Doador
- Cadastro de conta com endereço (busca automática por CEP via API ViaCEP)
- Registro de alimentos disponíveis informando nome, quantidade, validade e categoria
- Acompanhamento do ciclo de vida da doação: Disponível → Reservado → Entregue
- Confirmação de entrega e cancelamento de doações

### Perfil Instituição
- Feed interativo com todas as doações disponíveis em tempo real
- Filtro por categoria e busca por nome
- Alerta visual para itens com validade próxima (≤ 2 dias)
- Reserva exclusiva de itens com controle de concorrência (SELECT FOR UPDATE)
- Cancelamento de reserva, devolvendo o item ao feed
- Auto-refresh a cada 30 segundos

---

## 🔗 Consumo de APIs

### API Externa — ViaCEP
Na tela de cadastro, ao digitar o CEP, o sistema consulta automaticamente a API pública **ViaCEP** para preencher logradouro, bairro, cidade e UF, sem que o usuário precise digitar manualmente.

```
GET https://viacep.com.br/ws/{cep}/json/
```

### API Própria — FoodLink REST API
O backend expõe uma API REST completa consumida pelo frontend via `fetch()`:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Health check |
| POST | `/cadastro` | Cadastrar novo usuário |
| POST | `/login` | Autenticar usuário |
| GET | `/categorias` | Listar categorias de alimentos |
| POST | `/doacoes?doador_id=` | Criar nova doação |
| GET | `/doacoes` | Listar doações disponíveis |
| GET | `/doacoes/usuario/{id}` | Doações de um usuário específico |
| POST | `/doacoes/{id}/reservar?instituicao_id=` | Reservar item |
| POST | `/doacoes/{id}/entregar?doador_id=` | Confirmar entrega |
| POST | `/doacoes/{id}/cancelar?usuario_id=` | Cancelar doação ou reserva |

---

## Arquitetura

O projeto adota a arquitetura **Client-Server**, separando a interface do usuário da API de negócios.

```
Browser (HTML/CSS/JS) — Vercel
        |
        | HTTP/REST (JSON)
        v
FastAPI + Uvicorn (Python 3.11) — Render
        |
        | SQLAlchemy ORM
        v
   PostgreSQL — Render (produção)
   SQLite (desenvolvimento local)
```

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | HTML5, CSS3, JavaScript Vanilla, Bootstrap 5 |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Banco (produção) | PostgreSQL — Render |
| Banco (local) | SQLite |
| ORM | SQLAlchemy 2.0 |
| Validação | Pydantic 2.10 |
| Autenticação | Token SHA-256 |
| CI/CD | GitHub Actions |
| Hospedagem Frontend | Vercel |
| Hospedagem Backend | Render |
| API Externa | ViaCEP |

---

## Estrutura do Repositório

```
Lab_Eng_Software/
├── .github/
│   └── workflows/
│       └── ci.yml          — Pipeline de CI/CD (GitHub Actions)
├── backend/
│   ├── main.py             — API FastAPI: endpoints e regras de negócio
│   ├── models.py           — Modelos SQLAlchemy (tabelas do banco)
│   ├── schemas.py          — Schemas Pydantic (validação de dados)
│   ├── database.py         — Configuração do banco (SQLite/PostgreSQL)
│   ├── runtime.txt         — Versão do Python para o Render
│   └── requirements.txt    — Dependências Python
├── frontend/
│   ├── index.html          — Tela de Login
│   ├── cadastro.html       — Cadastro de novo usuário (+ integração ViaCEP)
│   ├── doador.html         — Dashboard do Doador
│   └── instituicao.html    — Feed da Instituição
├── Diagramas/              — Diagramas UML (Casos de Uso, Domínio, Sequência)
└── TG1.pdf                 — Documento de Especificação e Modelagem
```

---

## Como Rodar Localmente

### Pré-requisitos

| Ferramenta | Versão mínima |
|------------|--------------|
| Python | 3.11 |
| VSCode + extensão Live Server | qualquer |

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/epGamberi/Lab_Eng_Software.git
cd Lab_Eng_Software
```

**2. Instale as dependências do backend**
```bash
cd backend
pip install -r requirements.txt
```

**3. Inicie a API**
```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000` e o Swagger em `http://localhost:8000/docs`.

**4. Abra o frontend**

No VSCode, clique com o botão direito em `frontend/index.html` e selecione **Open with Live Server**.

> Para rodar localmente, altere `const API` nos HTMLs de `https://foodlink-backend-m6n0.onrender.com` para `http://localhost:8000`.

---

## Status do Projeto

**TG1 — Concluída:** Definição do produto, Engenharia de Requisitos, Wireframes e Modelagem UML.

**TG2 — Concluída:** Estrutura do backend, modelos, testes unitários e CI/CD com GitHub Actions.

**TG3 — Concluída:** Implementação completa do frontend e backend, integração com PostgreSQL, deploy em produção (Vercel + Render), consumo de API externa (ViaCEP).