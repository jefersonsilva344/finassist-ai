import json
from pathlib import Path

from src.agent.intent import classify_intent


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = (
    BASE_DIR
    / "evaluation"
    / "adversarial_dataset.json"
)


def load_dataset():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_adversarial_intents():
    dataset = load_dataset()

    for item in dataset:
        predicted = classify_intent(
            item["question"]
        )

        assert predicted == item["expected_intent"], (
            f"\nPergunta: {item['question']}"
            f"\nEsperado: {item['expected_intent']}"
            f"\nEncontrado: {predicted}"
        )