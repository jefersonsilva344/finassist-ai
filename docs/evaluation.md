# FinAssist AI — Avaliação e Métricas

## Objetivo

A avaliação do FinAssist AI tem como objetivo verificar se o agente
classifica corretamente as solicitações, recupera informações relevantes,
executa cálculos corretamente e respeita as regras de segurança.

---

## Dataset

A avaliação utiliza um conjunto de perguntas representativas das
principais categorias do agente.

O dataset está localizado em:

evaluation/dataset.json

---

## Métricas

### Intent Accuracy

Mede a proporção de perguntas classificadas corretamente.

```text
Accuracy =
classificações corretas / total de classificações