from src.knowledge.loader import load_knowledge
from src.knowledge.retriever import retrieve_knowledge


def test_knowledge_base_is_loaded():
    documents = load_knowledge()

    assert documents
    assert "fundamentos_financeiros.md" in documents


def test_retrieve_investment_knowledge():
    result = retrieve_knowledge(
        "O que é renda fixa?"
    )

    assert "investimentos.md" in result


def test_retrieve_security_knowledge():
    result = retrieve_knowledge(
        "Como identificar phishing?"
    )

    assert "seguranca_financeira.md" in result