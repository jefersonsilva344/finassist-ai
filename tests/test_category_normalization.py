from src.agent.category import normalize_category


def test_normalize_aluguel_to_moradia():
    assert normalize_category("aluguel") == "moradia"


def test_normalize_casa_to_moradia():
    assert normalize_category("casa") == "moradia"


def test_normalize_alimentacao_without_accent():
    assert normalize_category("alimentacao") == "alimentação"


def test_normalize_comida_to_alimentacao():
    assert normalize_category("comida") == "alimentação"


def test_normalize_uber_to_transporte():
    assert normalize_category("uber") == "transporte"


def test_normalize_agua_to_contas():
    assert normalize_category("agua") == "contas"


def test_normalize_unknown_category():
    assert normalize_category("academia") == "academia"


def test_normalize_category_ignores_spaces():
    assert normalize_category("  aluguel  ") == "moradia"


def test_normalize_category_ignores_case():
    assert normalize_category("ALUGUEL") == "moradia"