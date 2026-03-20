# Sistema de Doação de Alimentos

Projeto desenvolvido para a disciplina de **Laboratório de Engenharia de Software** da Universidade Presbiteriana Mackenzie, sob a orientação do **Prof. Msc. Luiz Carlos Machi Lozano**.

### Equipe Desenvolvedora
* **Enzo Ponte Gamberi** - RA: 10389931
* **João Guilherme Messias de Oliveira Santos** - RA: 10426110
* **Thiago Ruiz Fernandes Silva** - RA: 10426057

---

## Sobre o Projeto
O **Sistema de Doação de Alimentos** é uma plataforma digital web com forte caráter extensionista. O cenário atual brasileiro apresenta um paradoxo crítico: altos índices de desperdício de alimentos viáveis para consumo por parte do setor de comércio, em contraste com a insegurança alimentar enfrentada por parcelas vulneráveis da população. 

A nossa solução atua como uma ponte tecnológica, estabelecendo uma rede de comunicação eficiente e rastreável entre quem deseja doar (pessoas físicas, padarias, mercados) e quem precisa receber (ONGs, abrigos e instituições sociais).

## Principais Funcionalidades

O sistema opera com base em dois perfis principais de usuários:

### Para Doadores:
* **Cadastro Rápido de Alimentos:** Inserção de itens informando nome, quantidade, data de validade e categoria (perecível, não-perecível, etc).
* **Gestão de Status:** Acompanhamento do ciclo de vida da doação (Disponível ➔ Reservado ➔ Entregue).

### Para Instituições (Receptores):
* **Feed Dinâmico:** Visualização em tempo real de todas as doações disponíveis na plataforma.
* **Filtro Inteligente:** Busca otimizada por categorias específicas de alimentos.
* **Sistema de Reserva:** Garantia transacional de que um alimento reservado seja bloqueado para outras instituições, viabilizando a logística de retirada.

---

## Stack Tecnológica e Arquitetura

O projeto adota a arquitetura **Client-Server**, separando a interface do usuário da API de negócios para garantir escalabilidade e facilitar a implantação na nuvem.

**Frontend (Interface Web)**
* HTML5 & CSS3
* JavaScript (Vanilla)
* Bootstrap (Estilização responsiva)

**Backend (API RESTful)**
* Python 
* Microframework (Flask / FastAPI)

**Banco de Dados**
* SQLite (Ambiente de Desenvolvimento)
* PostgreSQL (Ambiente de Produção)

**DevOps & Cloud**
* **Controle de Versão:** Git & GitHub
* **CI/CD:** GitHub Actions (Esteira automatizada de testes e entrega)
* **Hospedagem:** Amazon Web Services - AWS (EC2 para aplicação e RDS para o banco de dados)

---

## Estrutura do Repositório

* `/Diagramas`: Contém os diagramas UML (Casos de Uso, Domínio e Sequência) que modelam as regras de negócio do sistema.
* `Documentação.pdf`: Documento formal detalhando requisitos, wireframes e arquitetura da Fase N1.
* *(As pastas contendo o código fonte do Front-end e Back-end serão adicionadas nas próximas iterações do ciclo de desenvolvimento).*

## Status do Projeto
✅ **Fase 1 (N1):** Definição do produto, Engenharia de Requisitos, Wireframes e Modelagem UML. *(Concluído)*  
⏳ **Fase 2 (N2):** Desenvolvimento da API, Front-end, CI/CD e Implantação na AWS. *(Em andamento)*
