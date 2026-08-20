# 🧠 FinAssist AI — Prompt Engineering

## Fase 3 — Prompts do Agente

Este documento define os prompts utilizados para orientar o comportamento
do FinAssist AI.

Os prompts são responsáveis por controlar:

- identidade do agente;
- identificação de intenção;
- utilização da base de conhecimento;
- tratamento de informações insuficientes;
- cálculos financeiros;
- planejamento de metas;
- educação sobre investimentos;
- segurança financeira;
- tratamento de solicitações fora do escopo;
- validação das respostas;
- prevenção de alucinações.

---

# 1. Arquitetura de Prompts

O FinAssist AI utiliza diferentes prompts de acordo com a etapa do fluxo.

```text
Usuário
   ↓
Identificação de intenção
   ↓
Verificação de segurança
   ↓
Recuperação de conhecimento
   ↓
Ferramenta de cálculo, quando necessário
   ↓
Geração da resposta
   ↓
Validação
   ↓
Resposta final