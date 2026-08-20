# 🤖 FinAssist AI


> **Intelligent Personal Finance Assistant powered by Python, AI, Financial Knowledge and Software Engineering**


O **FinAssist AI** é um assistente financeiro inteligente desenvolvido em Python para interpretar mensagens financeiras em linguagem natural, extrair informações estruturadas, persistir dados financeiros, analisar orçamento e utilizar uma base de conhecimento especializada para fornecer respostas contextualizadas.


O projeto foi desenvolvido com foco em **IA aplicada, arquitetura modular, separação de responsabilidades, persistência de dados, observabilidade, testes automatizados e avaliação sistemática do comportamento do agente**.


---


## 📌 Sobre o projeto


O objetivo do FinAssist AI é transformar interações financeiras em linguagem natural em operações estruturadas.


O usuário pode, por exemplo, informar:


> "Recebo R$ 5.000 por mês e gasto R$ 1.500 com aluguel."


O sistema é capaz de:


1. identificar a intenção da mensagem;
2. analisar o contexto da conversa;
3. verificar se existem informações suficientes;
4. extrair dados financeiros;
5. normalizar categorias;
6. persistir os dados;
7. recuperar informações relevantes;
8. analisar o orçamento;
9. consultar a base de conhecimento quando necessário;
10. produzir uma resposta contextualizada.


A proposta não é apenas criar um chatbot, mas construir uma **aplicação de IA com arquitetura de software estruturada e comportamento testável**.


---


# 🎯 Objetivos


O projeto foi desenvolvido com os seguintes objetivos:


- Construir um agente financeiro baseado em linguagem natural.
- Separar regras de negócio, aplicação, infraestrutura e interface.
- Implementar persistência utilizando SQLAlchemy.
- Criar uma camada de repositórios para acesso aos dados.
- Implementar gerenciamento de usuários e sessões.
- Persistir histórico de conversas.
- Persistir períodos financeiros e despesas.
- Implementar análise de orçamento.
- Criar uma Knowledge Base financeira.
- Implementar avaliação do comportamento do agente.
- Criar testes unitários, integração e API.
- Medir cobertura de código.
- Implementar logging e observabilidade.
- Criar uma arquitetura preparada para evolução.


---


# 🏗️ Arquitetura


O FinAssist AI utiliza uma arquitetura modular organizada por responsabilidades.


```text
                         ┌──────────────────────┐
                         │       Client         │
                         │   API / Interface    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │         API          │
                         │      FastAPI         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       Application Layer       │
                    │                               │
                    │  Use Cases                    │
                    │  Application Services        │
                    │  DTOs                         │
                    │  Financial Flow               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          Agent Layer           │
                    │                               │
                    │ Intent                        │
                    │ Context                       │
                    │ Decision                      │
                    │ Sufficiency                   │
                    │ Memory                        │
                    │ Session                       │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
          ┌────────────────────┐          ┌────────────────────┐
                              └───────────┘
🧠 Fluxo do agente

Uma mensagem financeira passa por diferentes etapas antes de gerar uma resposta.

User Message
     │
     ▼
┌──────────────┐
│ Intent       │
│ Detection    │
└──────┬───────┘
       ▼
┌──────────────┐
│ Context      │
│ Analysis     │
└──────┬───────┘
       ▼
┌──────────────┐
│ Sufficiency  │
│ Check        │
└──────┬───────┘
       ▼
┌──────────────┐
│ Decision     │
│ Engine       │
└──────┬───────┘
       │
       ├───────────────► Knowledge Base
       │
       ├───────────────► Financial Tools
       │
       ├───────────────► Persistence
       │
       └───────────────► LLM
                         │
                         ▼
                  Final Response

Essa abordagem evita que todas as decisões sejam delegadas diretamente ao modelo de linguagem.

O agente possui componentes responsáveis por diferentes decisões do fluxo, permitindo maior controle, previsibilidade e testabilidade.

🧩 Principais componentes
Agent

Responsável pela coordenação do comportamento inteligente.

Principais componentes:

src/agent/
├── agent.py
├── category.py
├── context.py
├── decision.py
├── intent.py
├── memory.py
├── session.py
└── sufficiency.py
Intent

Identifica a intenção da mensagem.

Exemplos:

register_income
register_expense
analyze_budget
financial_question
greeting
out_of_scope
Context

Analisa informações disponíveis na conversa e no estado financeiro atual.

Sufficiency

Verifica se existem informações suficientes para executar determinada operação.

Isso evita que o sistema execute operações incompletas quando faltam dados necessários.

Decision

Determina quais recursos devem ser utilizados.

Por exemplo:

requires_knowledge
requires_tool
requires_more_information
Memory

Mantém informações relevantes do fluxo conversacional.

💰 Persistência financeira

A camada de persistência utiliza SQLAlchemy para representar os principais objetos financeiros.

User
 │
 └── Session
      │
      ├── FinancialPeriod
      │      │
      │      └── Expense
      │
      └── ConversationMessage
Modelos
User

Representa o proprietário dos dados financeiros.

Session

Representa uma sessão de utilização do FinAssist AI.

FinancialPeriod

Representa o período financeiro mensal.

Possui:

ano;
mês;
renda;
total de despesas.
Expense

Representa uma despesa individual.

Possui:

categoria;
valor;
descrição;
período financeiro.
ConversationMessage

Representa mensagens persistidas da conversa.

Possui:

sessão;
papel da mensagem;
conteúdo;
timestamp.
🗄️ Repository Pattern

O acesso aos dados é abstraído através de repositories.

src/persistence/repositories/
├── conversation_repository.py
├── expense_repository.py
├── financial_period_repository.py
├── session_repository.py
└── user_repository.py

Essa separação evita que regras de acesso ao banco sejam espalhadas pela aplicação.

Exemplo:

repository = ExpenseRepository(db)


expenses = repository.list_by_period(
    period_id
)

A camada de aplicação trabalha com operações de persistência através dos repositories, mantendo o acesso ao banco isolado.

📊 Análise financeira

O sistema possui componentes para análise financeira e de orçamento.

Entre as funcionalidades estão:

registro de renda;
registro de despesas;
categorização;
análise por categoria;
análise de orçamento;
cálculo de totais;
recuperação de histórico financeiro;
análise contextual.

Exemplo de fluxo:

Income
   │
   ▼
Expenses
   │
   ▼
Category Analysis
   │
   ▼
Budget Analysis
   │
   ▼
Financial Insight
📚 Knowledge Base

O projeto possui uma base de conhecimento financeira localizada em:

data/knowledge/

Atualmente inclui conteúdos sobre:

criptomoedas.md
fundamentos_financeiros.md
investimentos.md
orcamento_pessoal.md
reserva_emergencia.md
seguranca_financeira.md

A camada de conhecimento é dividida em:

src/knowledge/
├── loader.py
└── retriever.py

O objetivo é separar o conhecimento financeiro da lógica do agente.

Isso permite atualizar ou expandir a base de conhecimento sem modificar diretamente a arquitetura do agente.

🛠️ Tools

O projeto possui ferramentas especializadas para operações determinísticas.

src/tools/
├── calculator.py
├── category_analyzer.py
├── category_report.py
├── extractor.py
└── formatters.py
Calculator

Executa cálculos financeiros de forma determinística.

Extractor

Extrai informações estruturadas de mensagens em linguagem natural.

Exemplo:

"gastei R$ 150 no supermercado"

pode ser transformado em:

category = alimentacao
amount = 150.00
Category Analyzer

Analisa e normaliza categorias financeiras.

Category Report

Produz informações agregadas sobre categorias de despesas.

🤖 LLM

A integração com modelo de linguagem está isolada na camada:

src/llm/
├── client.py
└── __init__.py

Essa separação reduz o acoplamento entre o agente e o provedor de LLM.

A aplicação pode utilizar o modelo para tarefas de linguagem enquanto mantém regras críticas, cálculos e persistência sob controle da aplicação.

🌐 API

O projeto utiliza FastAPI para exposição dos serviços.

Estrutura:

src/api/
├── dependencies.py
├── errors/
├── main.py
├── routes/
└── schemas/

Rotas principais:

GET  /health
POST /financial/message

A API possui:

validação de entrada;
schemas;
tratamento de exceções;
middleware;
observabilidade;
correlação de requisições.
🔎 Observabilidade

A aplicação possui uma camada dedicada de observabilidade:

src/observability/
├── logger.py
├── logging.py
└── middleware.py

O objetivo é permitir:

logging estruturado;
rastreamento de requisições;
correlação de operações;
diagnóstico de erros;
observação do fluxo da aplicação.
🧪 Testes

O projeto possui uma suíte automatizada utilizando pytest.

A cobertura inclui:

Agent
API
Application
Persistence
Knowledge
Tools
Observability
Security
Integration
Evaluation

Principais categorias:

tests/
├── test_agent_*
├── test_api_*
├── test_application_*
├── test_persistence_*
├── test_financial_flow_*
├── test_category_*
├── test_context.py
├── test_decision.py
├── test_extractor.py
├── test_knowledge.py
├── test_security.py
└── test_adversarial.py
📈 Qualidade atual

Última execução da suíte:

217 passed

Cobertura:

93%

Execução utilizada:

python -m pytest tests --cov=src --cov-report=term-missing -q

Resultado:

217 passed in 15.97s
TOTAL: 975 statements
COVERAGE: 93%

A cobertura elevada é utilizada como indicador de qualidade, mas não como único critério de validação.

O projeto também utiliza testes de integração, validação de API e cenários adversariais.

🛡️ Testes adversariais

O projeto possui uma suíte específica para avaliar comportamentos potencialmente problemáticos do agente.

Arquivo:

tests/test_adversarial.py

Além disso, existe uma estrutura dedicada de avaliação:

evaluation/
├── adversarial_dataset.json
├── dataset.json
├── metrics.py
└── run_evaluation.py

Isso permite avaliar o agente utilizando datasets controlados em vez de depender apenas de testes unitários.

📊 Evaluation

A avaliação do sistema é organizada separadamente do código principal.

evaluation/
├── dataset.json
├── adversarial_dataset.json
├── metrics.py
└── run_evaluation.py

Os resultados podem ser documentados em:

reports/evaluation_report.md

Essa separação permite evoluir a metodologia de avaliação sem misturar experimentação com código de produção.

🗂️ Estrutura do projeto
finassist-ai/
│
├── data/
│   └── knowledge/
│       ├── criptomoedas.md
│       ├── fundamentos_financeiros.md
│       ├── investimentos.md
│       ├── orcamento_pessoal.md
│       ├── reserva_emergencia.md
│       └── seguranca_financeira.md
│
├── docs/
│   ├── agente.md
│   ├── evaluation.md
│   ├── knowledge-base.md
│   └── prompts.md
│
├── evaluation/
│   ├── adversarial_dataset.json
│   ├── dataset.json
│   ├── metrics.py
│   └── run_evaluation.py
│
├── reports/
│   └── evaluation_report.md
│
├── src/
│   ├── agent/
│   ├── api/
│   ├── application/
│   ├── bootstrap/
│   ├── config/
│   ├── knowledge/
│   ├── llm/
│   ├── observability/
│   ├── persistence/
│   ├── prompts/
│   ├── security/
│   └── tools/
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Stack tecnológica
Linguagem
Python 3.14
Backend
FastAPI
Pydantic
SQLAlchemy
Banco de dados
SQLite
Inteligência Artificial
LLM
Prompt Engineering
Knowledge Base
Retrieval
Agent Architecture
Testes
Pytest
Pytest-Cov
Engenharia de software
Repository Pattern
Dependency Injection
DTO
Service Layer
Use Cases
Separation of Concerns
Modular Architecture
Observabilidade
Python Logging
Request Correlation
Middleware
Versionamento
Git
GitHub
🚀 Como executar
1. Clonar o projeto
git clone <REPOSITORY_URL>
cd finassist-ai
2. Criar ambiente virtual

Windows:

python -m venv .venv

Ativar:

.venv\Scripts\Activate.ps1

Linux/macOS:

python -m venv .venv
source .venv/bin/activate
3. Instalar dependências
pip install -r requirements.txt
4. Configurar variáveis de ambiente

Copie:

.env.example

para:

.env

Configure as variáveis necessárias para execução da aplicação.

Nunca versione credenciais, tokens ou chaves de API.

▶️ Executando os testes

Para executar todos os testes:

python -m pytest tests -q

Com cobertura:

python -m pytest tests --cov=src --cov-report=term-missing

Para gerar relatório HTML:

python -m pytest tests --cov=src --cov-report=html

O relatório será disponibilizado em:

htmlcov/
🔬 Executando a avaliação

A avaliação pode ser executada através de:

python evaluation/run_evaluation.py

Os datasets utilizados ficam em:

evaluation/
🔐 Segurança

O projeto adota algumas práticas básicas de segurança:

credenciais fora do código-fonte;
utilização de .env;
.env protegido pelo .gitignore;
validação de entradas;
tratamento centralizado de exceções;
separação entre camada de API e domínio;
testes de segurança;
testes adversariais.
⚠️ Disclaimer financeiro

O FinAssist AI é um projeto experimental e educacional de IA aplicada a finanças pessoais.

As informações produzidas pelo sistema não constituem:

recomendação de investimento;
consultoria financeira;
recomendação de compra ou venda de ativos;
aconselhamento profissional.

Decisões financeiras devem considerar informações atualizadas e, quando necessário, orientação de profissionais qualificados.

🧭 Roadmap
Concluído
 Arquitetura modular
 Agente financeiro
 Intent detection
 Context management
 Decision engine
 Sufficiency analysis
 Memory/session management
 Persistência com SQLAlchemy
 Repository layer
 Financial services
 Knowledge Base
 Financial tools
 FastAPI
 Error handling
 Observability
 Testes automatizados
 Testes de integração
 Testes adversariais
 Evaluation framework
 93% de cobertura de código
 Git repository
Próximas evoluções
 Dockerização
 CI/CD
 PostgreSQL
 Autenticação e autorização
 Dashboard financeiro
 Métricas de produção
 Retrieval mais avançado
 Avaliação contínua do agente
 Testes de carga
 API documentation aprimorada
 Deploy em cloud
 Interface web
 Integração com canais de atendimento
📚 Documentação

Documentação técnica adicional:

docs/
├── agente.md
├── evaluation.md
├── knowledge-base.md
└── prompts.md

Consulte esses documentos para detalhes sobre:

arquitetura do agente;
fluxo de decisão;
Knowledge Base;
prompts;
avaliação;
metodologia de testes.
🎓 O que este projeto demonstra

O FinAssist AI foi desenvolvido para demonstrar competências práticas em:

Python
programação orientada a objetos;
type hints;
dataclasses;
enums;
tratamento de exceções;
organização modular.
Backend
APIs REST;
FastAPI;
validação de dados;
services;
use cases;
DTOs;
dependency injection.
Banco de dados
modelagem relacional;
SQLAlchemy ORM;
relacionamentos;
constraints;
repositories;
transações.
Inteligência Artificial
integração com LLM;
agentes;
classificação de intenção;
gerenciamento de contexto;
memória;
prompting;
Knowledge Base;
retrieval;
avaliação adversarial.
Engenharia de software
Separation of Concerns;
Repository Pattern;
Service Layer;
Dependency Injection;
testes automatizados;
integração;
observabilidade;
avaliação de qualidade.
📌 Status

Status: 🟢 Em desenvolvimento

Versão: 0.1.0

Testes: 217 passed

Cobertura: 93%

Python: 3.14

👨‍💻 Autor

Jeferson Silva

Desenvolvedor Python com foco em:

Python Backend
APIs REST
Automação
Inteligência Artificial Aplicada
Engenharia de Software
⭐ Objetivo do projeto

O FinAssist AI faz parte de uma iniciativa de construção de projetos práticos voltados para Python Backend e Inteligência Artificial Aplicada, com foco em transformar conceitos de IA em sistemas reais, testáveis e arquiteturalmente organizados.

Se este projeto foi útil ou interessante, considere deixar uma ⭐ no repositório.