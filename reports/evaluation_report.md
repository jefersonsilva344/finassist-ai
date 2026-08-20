# FinAssist AI — Evaluation Report

## Overview

The FinAssist AI evaluation pipeline measures the accuracy of the
agent's intent classification and knowledge retrieval components.

The evaluation dataset contains representative financial education,
budgeting, investment, financial security and out-of-scope queries.

---

## Evaluation Metrics

### Intent Accuracy

Measures how often the system correctly identifies the primary
intent of the user's message.

Formula:

Accuracy = Correct Predictions / Total Predictions

### Knowledge Retrieval Accuracy

Measures whether the expected knowledge document is retrieved for
queries that require knowledge-base information.

---

## Results

| Metric | Result |
|---|---:|
| Intent Accuracy | 100% |
| Knowledge Retrieval Accuracy | 100% |
| Automated Tests | 21/21 |

---

## Intent Categories

The evaluation covers:

- financial_education
- budget_analysis
- financial_goal
- calculation
- investment_education
- financial_security
- out_of_scope

---

## Knowledge Base Coverage

The evaluation covers:

- fundamentos_financeiros.md
- reserva_emergencia.md
- orcamento_pessoal.md
- investimentos.md
- seguranca_financeira.md

---

## Security Evaluation

The project includes automated tests for:

- phishing detection;
- password requests;
- CVV requests;
- financial security classification.

---

## Limitations

The current retrieval system uses keyword-based matching.

Therefore, semantic variations that do not contain known keywords
may not retrieve the correct document.

The evaluation also does not yet measure the quality of the generated
natural-language response.

---

## Next Evolution

Future evaluation versions may include:

- semantic retrieval evaluation;
- response quality;
- hallucination detection;
- safety evaluation;
- consistency evaluation;
- adversarial prompts;
- LLM-as-a-judge evaluation;
- regression testing;
- evaluation across prompt versions.