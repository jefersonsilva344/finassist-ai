def calculate_accuracy(
    correct: int,
    total: int,
) -> float:
    """
    Calcula a acurácia de uma avaliação.

    Retorna um valor entre 0 e 1.
    """

    if total == 0:
        return 0.0

    return correct / total